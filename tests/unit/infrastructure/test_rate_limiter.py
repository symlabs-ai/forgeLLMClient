"""Tests for the rate limiting infrastructure."""

import asyncio

import pytest

from forge_llm.infrastructure.rate_limiter import (
    CompositeRateLimiter,
    NoOpRateLimiter,
    RateLimitConfig,
    RateLimitExceededError,
    RateLimitStats,
    TokenBucketRateLimiter,
    create_rate_limiter,
)


class TestRateLimitConfig:
    """Tests for RateLimitConfig."""

    def test_defaults(self) -> None:
        """Test default configuration."""
        config = RateLimitConfig()

        assert config.requests_per_minute == 60
        assert config.tokens_per_minute is None
        assert config.burst_allowance == 5
        assert config.wait_on_limit is True
        assert config.max_wait_seconds == 60.0

    def test_custom_values(self) -> None:
        """Test custom configuration."""
        config = RateLimitConfig(
            requests_per_minute=100,
            tokens_per_minute=50000,
            burst_allowance=10,
            wait_on_limit=False,
        )

        assert config.requests_per_minute == 100
        assert config.tokens_per_minute == 50000
        assert config.burst_allowance == 10
        assert config.wait_on_limit is False


class TestRateLimitStats:
    """Tests for RateLimitStats."""

    def test_avg_wait_time_no_waits(self) -> None:
        """Test avg wait time with no waits."""
        stats = RateLimitStats()
        assert stats.avg_wait_time_ms == 0.0

    def test_avg_wait_time_calculation(self) -> None:
        """Test avg wait time calculation."""
        stats = RateLimitStats(
            waits_triggered=2,
            total_wait_time_ms=1000.0,
        )
        assert stats.avg_wait_time_ms == 500.0


class TestTokenBucketRateLimiter:
    """Tests for TokenBucketRateLimiter."""

    @pytest.fixture
    def limiter(self) -> TokenBucketRateLimiter:
        """Create a rate limiter with high limits."""
        return TokenBucketRateLimiter(
            provider="test",
            config=RateLimitConfig(requests_per_minute=1000),
        )

    @pytest.mark.asyncio
    async def test_acquire_within_limit(self, limiter: TokenBucketRateLimiter) -> None:
        """Test acquiring within rate limit."""
        await limiter.acquire()
        stats = limiter.stats()
        assert stats.requests_this_minute == 1

    @pytest.mark.asyncio
    async def test_multiple_acquires(self, limiter: TokenBucketRateLimiter) -> None:
        """Test multiple acquires."""
        for _ in range(5):
            await limiter.acquire()

        stats = limiter.stats()
        assert stats.requests_this_minute == 5

    @pytest.mark.asyncio
    async def test_acquire_with_tokens(self, limiter: TokenBucketRateLimiter) -> None:
        """Test acquiring with token count."""
        await limiter.acquire(tokens=100)
        stats = limiter.stats()
        assert stats.tokens_this_minute == 100

    @pytest.mark.asyncio
    async def test_rate_limit_exceeded_raises(self) -> None:
        """Test that exceeding rate limit raises error when wait_on_limit=False."""
        limiter = TokenBucketRateLimiter(
            provider="test",
            config=RateLimitConfig(
                requests_per_minute=2,
                burst_allowance=0,
                wait_on_limit=False,
            ),
        )

        await limiter.acquire()
        await limiter.acquire()

        with pytest.raises(RateLimitExceededError) as exc_info:
            await limiter.acquire()

        assert exc_info.value.provider == "test"
        assert exc_info.value.limit_type == "requests_per_minute"
        assert exc_info.value.current == 2
        assert exc_info.value.limit == 2

    @pytest.mark.asyncio
    async def test_rate_limit_waits(self) -> None:
        """Test that rate limit waits when wait_on_limit=True."""
        limiter = TokenBucketRateLimiter(
            provider="test",
            config=RateLimitConfig(
                requests_per_minute=1,
                burst_allowance=0,
                wait_on_limit=True,
                max_wait_seconds=0.1,  # Short wait for test
            ),
        )

        await limiter.acquire()

        start = asyncio.get_event_loop().time()
        await limiter.acquire()  # Should wait and reset window
        elapsed = asyncio.get_event_loop().time() - start

        assert elapsed >= 0.1
        stats = limiter.stats()
        assert stats.waits_triggered >= 1

    @pytest.mark.asyncio
    async def test_token_limit_exceeded(self) -> None:
        """Test token per minute limit."""
        limiter = TokenBucketRateLimiter(
            provider="test",
            config=RateLimitConfig(
                requests_per_minute=1000,
                tokens_per_minute=100,
                burst_allowance=0,
                wait_on_limit=False,
            ),
        )

        await limiter.acquire(tokens=50)

        with pytest.raises(RateLimitExceededError) as exc_info:
            await limiter.acquire(tokens=60)  # Would exceed 100 TPM

        assert exc_info.value.limit_type == "tokens_per_minute"

    @pytest.mark.asyncio
    async def test_reset(self, limiter: TokenBucketRateLimiter) -> None:
        """Test resetting the limiter."""
        await limiter.acquire()
        await limiter.acquire()

        limiter.reset()
        stats = limiter.stats()

        assert stats.requests_this_minute == 0
        assert stats.waits_triggered == 0

    @pytest.mark.asyncio
    async def test_burst_allowance(self) -> None:
        """Test burst allowance."""
        limiter = TokenBucketRateLimiter(
            provider="test",
            config=RateLimitConfig(
                requests_per_minute=2,
                burst_allowance=1,
                wait_on_limit=False,
            ),
        )

        # Should allow 3 requests (2 + 1 burst)
        await limiter.acquire()
        await limiter.acquire()
        await limiter.acquire()

        # 4th should fail
        with pytest.raises(RateLimitExceededError):
            await limiter.acquire()


class TestNoOpRateLimiter:
    """Tests for NoOpRateLimiter."""

    @pytest.fixture
    def limiter(self) -> NoOpRateLimiter:
        """Create a no-op limiter."""
        return NoOpRateLimiter()

    @pytest.mark.asyncio
    async def test_acquire_always_succeeds(self, limiter: NoOpRateLimiter) -> None:
        """Test that acquire always succeeds."""
        for _ in range(1000):
            await limiter.acquire()

    @pytest.mark.asyncio
    async def test_stats_always_empty(self, limiter: NoOpRateLimiter) -> None:
        """Test that stats are always empty."""
        await limiter.acquire()
        stats = limiter.stats()
        assert stats.requests_this_minute == 0


class TestCompositeRateLimiter:
    """Tests for CompositeRateLimiter."""

    @pytest.fixture
    def composite(self) -> CompositeRateLimiter:
        """Create a composite limiter."""
        limiter = CompositeRateLimiter()
        limiter.configure_provider(
            "openai",
            RateLimitConfig(requests_per_minute=60),
        )
        limiter.configure_provider(
            "anthropic",
            RateLimitConfig(requests_per_minute=100),
        )
        return limiter

    @pytest.mark.asyncio
    async def test_get_configured_limiter(self, composite: CompositeRateLimiter) -> None:
        """Test getting a configured limiter."""
        limiter = composite.get_limiter("openai")
        assert isinstance(limiter, TokenBucketRateLimiter)

    @pytest.mark.asyncio
    async def test_get_unconfigured_returns_noop(
        self, composite: CompositeRateLimiter
    ) -> None:
        """Test getting an unconfigured provider returns NoOpRateLimiter."""
        limiter = composite.get_limiter("unknown")
        assert isinstance(limiter, NoOpRateLimiter)

    @pytest.mark.asyncio
    async def test_independent_limits(self, composite: CompositeRateLimiter) -> None:
        """Test that providers have independent limits."""
        openai_limiter = composite.get_limiter("openai")
        anthropic_limiter = composite.get_limiter("anthropic")

        await openai_limiter.acquire()
        await anthropic_limiter.acquire()

        openai_stats = openai_limiter.stats()
        anthropic_stats = anthropic_limiter.stats()

        assert openai_stats.requests_this_minute == 1
        assert anthropic_stats.requests_this_minute == 1

    @pytest.mark.asyncio
    async def test_stats_by_provider(self, composite: CompositeRateLimiter) -> None:
        """Test getting stats by provider."""
        await composite.get_limiter("openai").acquire()
        await composite.get_limiter("openai").acquire()
        await composite.get_limiter("anthropic").acquire()

        stats = composite.stats_by_provider()

        assert stats["openai"].requests_this_minute == 2
        assert stats["anthropic"].requests_this_minute == 1

    @pytest.mark.asyncio
    async def test_aggregate_stats(self, composite: CompositeRateLimiter) -> None:
        """Test aggregated stats."""
        await composite.get_limiter("openai").acquire()
        await composite.get_limiter("anthropic").acquire()

        stats = composite.stats()
        assert stats.requests_this_minute == 2

    @pytest.mark.asyncio
    async def test_reset_all(self, composite: CompositeRateLimiter) -> None:
        """Test resetting all limiters."""
        await composite.get_limiter("openai").acquire()
        await composite.get_limiter("anthropic").acquire()

        composite.reset()

        stats = composite.stats()
        assert stats.requests_this_minute == 0


class TestCreateRateLimiter:
    """Tests for create_rate_limiter helper."""

    def test_creates_limiter_with_defaults(self) -> None:
        """Test creating a limiter with default config."""
        limiter = create_rate_limiter("openai")
        assert isinstance(limiter, TokenBucketRateLimiter)

    def test_creates_limiter_with_custom_config(self) -> None:
        """Test creating a limiter with custom config."""
        config = RateLimitConfig(requests_per_minute=42)
        limiter = create_rate_limiter("custom", config)
        assert isinstance(limiter, TokenBucketRateLimiter)

    def test_uses_default_for_known_provider(self) -> None:
        """Test that known providers use their defaults."""
        limiter = create_rate_limiter("openai")
        # Just verify it was created successfully
        assert isinstance(limiter, TokenBucketRateLimiter)
