"""Rate limiting for LLM API calls."""

from __future__ import annotations

import asyncio
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from forge_llm.domain.exceptions import ForgeError


@dataclass
class RateLimitConfig:
    """Configuration for rate limiting per provider."""

    # Requests per minute (RPM)
    requests_per_minute: int = 60
    # Tokens per minute (TPM) - optional
    tokens_per_minute: int | None = None
    # Requests per day (RPD) - optional
    requests_per_day: int | None = None
    # Burst allowance (extra requests allowed in short bursts)
    burst_allowance: int = 5
    # Whether to wait or raise error when limit reached
    wait_on_limit: bool = True
    # Maximum wait time in seconds
    max_wait_seconds: float = 60.0


@dataclass
class RateLimitStats:
    """Statistics about rate limiting."""

    requests_this_minute: int = 0
    requests_this_day: int = 0
    tokens_this_minute: int = 0
    waits_triggered: int = 0
    total_wait_time_ms: float = 0.0
    limits_exceeded: int = 0

    @property
    def avg_wait_time_ms(self) -> float:
        """Average wait time when rate limited."""
        return self.total_wait_time_ms / self.waits_triggered if self.waits_triggered > 0 else 0.0


class RateLimitExceededError(ForgeError):
    """Raised when rate limit is exceeded and waiting is disabled."""

    def __init__(
        self,
        message: str,
        provider: str,
        limit_type: str,
        current: int,
        limit: int,
        retry_after_seconds: float | None = None,
    ) -> None:
        super().__init__(message)
        self.provider = provider
        self.limit_type = limit_type
        self.current = current
        self.limit = limit
        self.retry_after_seconds = retry_after_seconds


class RateLimiterPort(ABC):
    """Abstract interface for rate limiting."""

    @abstractmethod
    async def acquire(self, tokens: int = 0) -> None:
        """
        Acquire permission to make a request.

        Args:
            tokens: Number of tokens for this request (for TPM limits)

        Raises:
            RateLimitExceededError: If limit exceeded and wait_on_limit=False
        """
        ...

    @abstractmethod
    async def release(self, tokens_used: int = 0) -> None:
        """
        Report actual tokens used after a request.

        Args:
            tokens_used: Actual tokens consumed
        """
        ...

    @abstractmethod
    def stats(self) -> RateLimitStats:
        """Get rate limiting statistics."""
        ...

    @abstractmethod
    def reset(self) -> None:
        """Reset all counters and stats."""
        ...


@dataclass
class _RequestWindow:
    """Sliding window for tracking requests/tokens."""

    window_start: float = field(default_factory=time.time)
    count: int = 0
    tokens: int = 0


class TokenBucketRateLimiter(RateLimiterPort):
    """
    Token bucket rate limiter implementation.

    Uses a sliding window approach to track requests per minute.
    """

    def __init__(
        self,
        provider: str,
        config: RateLimitConfig | None = None,
    ) -> None:
        self._provider = provider
        self._config = config or RateLimitConfig()
        self._minute_window = _RequestWindow()
        self._day_window = _RequestWindow()
        self._stats = RateLimitStats()
        self._lock = asyncio.Lock()

    async def acquire(self, tokens: int = 0) -> None:
        """Acquire permission to make a request."""
        async with self._lock:
            now = time.time()

            # Refresh minute window (60 second sliding window)
            if now - self._minute_window.window_start >= 60.0:
                self._minute_window = _RequestWindow(window_start=now)

            # Refresh day window (24 hour sliding window)
            if now - self._day_window.window_start >= 86400.0:
                self._day_window = _RequestWindow(window_start=now)

            # Check RPM limit
            effective_rpm = self._config.requests_per_minute + self._config.burst_allowance
            if self._minute_window.count >= effective_rpm:
                wait_time = 60.0 - (now - self._minute_window.window_start)
                await self._handle_limit_exceeded(
                    "requests_per_minute",
                    self._minute_window.count,
                    self._config.requests_per_minute,
                    wait_time,
                )
                # After waiting, reset window
                self._minute_window = _RequestWindow(window_start=time.time())

            # Check TPM limit if configured
            if (
                self._config.tokens_per_minute is not None
                and self._minute_window.tokens + tokens > self._config.tokens_per_minute
            ):
                wait_time = 60.0 - (now - self._minute_window.window_start)
                await self._handle_limit_exceeded(
                    "tokens_per_minute",
                    self._minute_window.tokens,
                    self._config.tokens_per_minute,
                    wait_time,
                )
                self._minute_window = _RequestWindow(window_start=time.time())

            # Check RPD limit if configured
            if (
                self._config.requests_per_day is not None
                and self._day_window.count >= self._config.requests_per_day
            ):
                wait_time = 86400.0 - (now - self._day_window.window_start)
                await self._handle_limit_exceeded(
                    "requests_per_day",
                    self._day_window.count,
                    self._config.requests_per_day,
                    wait_time,
                )
                self._day_window = _RequestWindow(window_start=time.time())

            # Increment counters
            self._minute_window.count += 1
            self._minute_window.tokens += tokens
            self._day_window.count += 1
            self._stats.requests_this_minute = self._minute_window.count
            self._stats.requests_this_day = self._day_window.count
            self._stats.tokens_this_minute = self._minute_window.tokens

    async def _handle_limit_exceeded(
        self,
        limit_type: str,
        current: int,
        limit: int,
        wait_time: float,
    ) -> None:
        """Handle when a rate limit is exceeded."""
        self._stats.limits_exceeded += 1

        if not self._config.wait_on_limit:
            raise RateLimitExceededError(
                message=f"Rate limit exceeded: {limit_type}",
                provider=self._provider,
                limit_type=limit_type,
                current=current,
                limit=limit,
                retry_after_seconds=wait_time,
            )

        # Cap wait time
        wait_time = min(wait_time, self._config.max_wait_seconds)

        if wait_time > 0:
            self._stats.waits_triggered += 1
            self._stats.total_wait_time_ms += wait_time * 1000
            await asyncio.sleep(wait_time)

    async def release(self, tokens_used: int = 0) -> None:
        """Report actual tokens used (for correction after request)."""
        # In this implementation, we pre-count tokens in acquire()
        # This method can be used to adjust if actual usage differs
        pass

    def stats(self) -> RateLimitStats:
        """Get rate limiting statistics."""
        return RateLimitStats(
            requests_this_minute=self._stats.requests_this_minute,
            requests_this_day=self._stats.requests_this_day,
            tokens_this_minute=self._stats.tokens_this_minute,
            waits_triggered=self._stats.waits_triggered,
            total_wait_time_ms=self._stats.total_wait_time_ms,
            limits_exceeded=self._stats.limits_exceeded,
        )

    def reset(self) -> None:
        """Reset all counters and stats."""
        self._minute_window = _RequestWindow()
        self._day_window = _RequestWindow()
        self._stats = RateLimitStats()


class NoOpRateLimiter(RateLimiterPort):
    """A rate limiter that does nothing (for disabled rate limiting)."""

    async def acquire(self, tokens: int = 0) -> None:
        """Always allows the request."""
        pass

    async def release(self, tokens_used: int = 0) -> None:
        """Does nothing."""
        pass

    def stats(self) -> RateLimitStats:
        """Returns empty stats."""
        return RateLimitStats()

    def reset(self) -> None:
        """Does nothing."""
        pass


class CompositeRateLimiter(RateLimiterPort):
    """Rate limiter that manages multiple provider-specific limiters."""

    def __init__(self) -> None:
        self._limiters: dict[str, RateLimiterPort] = {}
        self._configs: dict[str, RateLimitConfig] = {}

    def configure_provider(
        self,
        provider: str,
        config: RateLimitConfig,
    ) -> None:
        """Configure rate limiting for a specific provider."""
        self._configs[provider] = config
        self._limiters[provider] = TokenBucketRateLimiter(provider, config)

    def get_limiter(self, provider: str) -> RateLimiterPort:
        """Get the rate limiter for a specific provider."""
        if provider not in self._limiters:
            # Return no-op limiter for unconfigured providers
            return NoOpRateLimiter()
        return self._limiters[provider]

    async def acquire(self, tokens: int = 0) -> None:
        """Not used directly - use get_limiter(provider).acquire()."""
        raise NotImplementedError("Use get_limiter(provider).acquire() instead")

    async def release(self, tokens_used: int = 0) -> None:
        """Not used directly - use get_limiter(provider).release()."""
        raise NotImplementedError("Use get_limiter(provider).release() instead")

    def stats(self) -> RateLimitStats:
        """Get aggregated stats across all providers."""
        total = RateLimitStats()
        for limiter in self._limiters.values():
            s = limiter.stats()
            total.requests_this_minute += s.requests_this_minute
            total.requests_this_day += s.requests_this_day
            total.tokens_this_minute += s.tokens_this_minute
            total.waits_triggered += s.waits_triggered
            total.total_wait_time_ms += s.total_wait_time_ms
            total.limits_exceeded += s.limits_exceeded
        return total

    def stats_by_provider(self) -> dict[str, RateLimitStats]:
        """Get stats for each provider."""
        return {
            provider: limiter.stats()
            for provider, limiter in self._limiters.items()
        }

    def reset(self) -> None:
        """Reset all limiters."""
        for limiter in self._limiters.values():
            limiter.reset()


# Default rate limits for common providers
DEFAULT_RATE_LIMITS: dict[str, RateLimitConfig] = {
    "openai": RateLimitConfig(
        requests_per_minute=60,
        tokens_per_minute=90000,
        burst_allowance=10,
    ),
    "anthropic": RateLimitConfig(
        requests_per_minute=60,
        tokens_per_minute=100000,
        burst_allowance=10,
    ),
    "openrouter": RateLimitConfig(
        requests_per_minute=200,  # OpenRouter has higher limits
        burst_allowance=20,
    ),
}


def create_rate_limiter(
    provider: str,
    config: RateLimitConfig | None = None,
) -> RateLimiterPort:
    """
    Create a rate limiter for a provider.

    Uses default limits if no config provided.
    """
    if config is None:
        config = DEFAULT_RATE_LIMITS.get(provider, RateLimitConfig())
    return TokenBucketRateLimiter(provider, config)
