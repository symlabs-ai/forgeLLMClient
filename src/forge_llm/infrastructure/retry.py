"""Retry logic with exponential backoff for API calls."""

import asyncio
import random
from collections.abc import Callable
from dataclasses import dataclass, field
from functools import wraps
from typing import Any, TypeVar

from forge_llm.domain.exceptions import (
    APIError,
    APITimeoutError,
    AuthenticationError,
    RateLimitError,
    RetryExhaustedError,
)

T = TypeVar("T")


@dataclass
class RetryConfig:
    """Configuration for retry behavior."""

    max_retries: int = 3
    base_delay: float = 1.0
    max_delay: float = 60.0
    exponential_base: float = 2.0
    jitter: bool = True

    # Retry on these exception types
    retryable_exceptions: tuple[type[Exception], ...] = field(
        default_factory=lambda: (RateLimitError, APITimeoutError)
    )

    def calculate_delay(self, attempt: int) -> float:
        """Calculate delay for a given attempt number (0-indexed)."""
        delay = self.base_delay * (self.exponential_base**attempt)
        delay = min(delay, self.max_delay)

        if self.jitter:
            # Add random jitter between 0 and 25% of delay
            jitter_amount = delay * 0.25 * random.random()
            delay = delay + jitter_amount

        return delay


def is_retryable_error(error: Exception, config: RetryConfig) -> bool:
    """Check if an error should trigger a retry."""
    # Check explicit retryable exceptions
    if isinstance(error, config.retryable_exceptions):
        return True

    # APIError with retryable flag
    if isinstance(error, APIError) and error.retryable:
        return True

    # Never retry authentication errors
    if isinstance(error, AuthenticationError):
        return False

    return False


async def with_retry(
    func: Callable[..., Any],
    config: RetryConfig,
    provider: str,
    *args: Any,
    **kwargs: Any,
) -> Any:
    """Execute an async function with retry logic.

    Args:
        func: Async function to execute
        config: Retry configuration
        provider: Provider name for error messages
        *args: Positional arguments for func
        **kwargs: Keyword arguments for func

    Returns:
        Result of func

    Raises:
        RetryExhaustedError: When all retries are exhausted
        Exception: Non-retryable errors are raised immediately
    """
    last_error: Exception | None = None

    for attempt in range(config.max_retries + 1):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            last_error = e

            # Check if we should retry
            if not is_retryable_error(e, config):
                raise

            # Check if we have retries left
            if attempt >= config.max_retries:
                raise RetryExhaustedError(
                    message=f"All {config.max_retries + 1} attempts failed",
                    provider=provider,
                    attempts=config.max_retries + 1,
                    last_error=last_error,
                ) from e

            # Calculate delay and wait
            delay = config.calculate_delay(attempt)

            # If RateLimitError has retry_after, use that instead
            if isinstance(e, RateLimitError) and e.retry_after:
                delay = max(delay, float(e.retry_after))

            await asyncio.sleep(delay)

    # Should never reach here, but just in case
    raise RetryExhaustedError(
        message=f"All {config.max_retries + 1} attempts failed",
        provider=provider,
        attempts=config.max_retries + 1,
        last_error=last_error,
    )


def retry_decorator(
    config: RetryConfig | None = None,
    provider: str = "unknown",
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Decorator to add retry logic to an async function.

    Args:
        config: Retry configuration (uses defaults if None)
        provider: Provider name for error messages

    Returns:
        Decorated function with retry logic
    """
    if config is None:
        config = RetryConfig()

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> T:
            return await with_retry(func, config, provider, *args, **kwargs)

        return wrapper  # type: ignore[return-value]

    return decorator
