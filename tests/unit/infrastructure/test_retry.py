"""Unit tests for retry logic."""

import pytest

from forge_llm.domain.exceptions import (
    APIError,
    APITimeoutError,
    AuthenticationError,
    RateLimitError,
    RetryExhaustedError,
)
from forge_llm.infrastructure.retry import (
    RetryConfig,
    is_retryable_error,
    retry_decorator,
    with_retry,
)


class TestRetryConfig:
    """Tests for RetryConfig."""

    def test_default_values(self):
        """RetryConfig has sensible defaults."""
        config = RetryConfig()

        assert config.max_retries == 3
        assert config.base_delay == 1.0
        assert config.max_delay == 60.0
        assert config.exponential_base == 2.0
        assert config.jitter is True

    def test_custom_values(self):
        """RetryConfig accepts custom values."""
        config = RetryConfig(
            max_retries=5,
            base_delay=0.5,
            max_delay=30.0,
            exponential_base=3.0,
            jitter=False,
        )

        assert config.max_retries == 5
        assert config.base_delay == 0.5
        assert config.max_delay == 30.0
        assert config.exponential_base == 3.0
        assert config.jitter is False

    def test_calculate_delay_exponential(self):
        """calculate_delay uses exponential backoff."""
        config = RetryConfig(base_delay=1.0, exponential_base=2.0, jitter=False)

        assert config.calculate_delay(0) == 1.0  # 1 * 2^0 = 1
        assert config.calculate_delay(1) == 2.0  # 1 * 2^1 = 2
        assert config.calculate_delay(2) == 4.0  # 1 * 2^2 = 4
        assert config.calculate_delay(3) == 8.0  # 1 * 2^3 = 8

    def test_calculate_delay_respects_max_delay(self):
        """calculate_delay respects max_delay."""
        config = RetryConfig(
            base_delay=1.0, max_delay=5.0, exponential_base=2.0, jitter=False
        )

        assert config.calculate_delay(0) == 1.0
        assert config.calculate_delay(1) == 2.0
        assert config.calculate_delay(2) == 4.0
        assert config.calculate_delay(3) == 5.0  # capped at max_delay
        assert config.calculate_delay(10) == 5.0  # still capped

    def test_calculate_delay_with_jitter(self):
        """calculate_delay adds jitter when enabled."""
        config = RetryConfig(base_delay=1.0, exponential_base=2.0, jitter=True)

        # Run multiple times to verify jitter adds variance
        delays = [config.calculate_delay(0) for _ in range(10)]

        # Base delay is 1.0, jitter adds up to 25%
        for delay in delays:
            assert 1.0 <= delay <= 1.25

        # Verify we got some variance (not all the same)
        assert len(set(delays)) > 1


class TestIsRetryableError:
    """Tests for is_retryable_error."""

    def test_rate_limit_error_is_retryable(self):
        """RateLimitError is retryable."""
        config = RetryConfig()
        error = RateLimitError("Rate limited", "openai")

        assert is_retryable_error(error, config) is True

    def test_api_timeout_error_is_retryable(self):
        """APITimeoutError is retryable."""
        config = RetryConfig()
        error = APITimeoutError("Timeout", "openai")

        assert is_retryable_error(error, config) is True

    def test_api_error_with_retryable_flag_is_retryable(self):
        """APIError with retryable=True is retryable."""
        config = RetryConfig()
        error = APIError("Server error", "openai", status_code=500, retryable=True)

        assert is_retryable_error(error, config) is True

    def test_api_error_without_retryable_flag_is_not_retryable(self):
        """APIError with retryable=False is not retryable."""
        config = RetryConfig()
        error = APIError("Bad request", "openai", status_code=400, retryable=False)

        assert is_retryable_error(error, config) is False

    def test_authentication_error_is_not_retryable(self):
        """AuthenticationError is never retryable."""
        config = RetryConfig()
        error = AuthenticationError("Invalid key", "openai")

        assert is_retryable_error(error, config) is False

    def test_generic_exception_is_not_retryable(self):
        """Generic exceptions are not retryable."""
        config = RetryConfig()
        error = ValueError("Some error")

        assert is_retryable_error(error, config) is False

    def test_custom_retryable_exceptions(self):
        """Custom retryable_exceptions are respected."""
        config = RetryConfig(retryable_exceptions=(ValueError,))
        error = ValueError("Custom retryable")

        assert is_retryable_error(error, config) is True


class TestWithRetry:
    """Tests for with_retry function."""

    @pytest.mark.asyncio
    async def test_success_on_first_attempt(self):
        """Successful call returns immediately."""
        call_count = 0

        async def success_func():
            nonlocal call_count
            call_count += 1
            return "success"

        config = RetryConfig(max_retries=3)
        result = await with_retry(success_func, config, "test")

        assert result == "success"
        assert call_count == 1

    @pytest.mark.asyncio
    async def test_success_after_retries(self):
        """Success after retryable failures returns result."""
        call_count = 0

        async def eventual_success():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise RateLimitError("Rate limited", "test")
            return "success"

        config = RetryConfig(max_retries=3, base_delay=0.01)
        result = await with_retry(eventual_success, config, "test")

        assert result == "success"
        assert call_count == 3

    @pytest.mark.asyncio
    async def test_exhausted_retries_raises_retry_exhausted_error(self):
        """Exhausted retries raise RetryExhaustedError."""
        call_count = 0

        async def always_fails():
            nonlocal call_count
            call_count += 1
            raise RateLimitError("Rate limited", "test")

        config = RetryConfig(max_retries=2, base_delay=0.01)

        with pytest.raises(RetryExhaustedError) as exc_info:
            await with_retry(always_fails, config, "test")

        assert exc_info.value.attempts == 3  # max_retries + 1
        assert exc_info.value.provider == "test"
        assert isinstance(exc_info.value.last_error, RateLimitError)
        assert call_count == 3

    @pytest.mark.asyncio
    async def test_non_retryable_error_raises_immediately(self):
        """Non-retryable errors are raised immediately."""
        call_count = 0

        async def auth_fails():
            nonlocal call_count
            call_count += 1
            raise AuthenticationError("Invalid key", "test")

        config = RetryConfig(max_retries=3, base_delay=0.01)

        with pytest.raises(AuthenticationError):
            await with_retry(auth_fails, config, "test")

        # Should only be called once - no retries
        assert call_count == 1

    @pytest.mark.asyncio
    async def test_respects_retry_after_header(self):
        """RateLimitError.retry_after is respected."""
        import time

        call_count = 0
        start_time = None

        async def rate_limited_with_retry_after():
            nonlocal call_count, start_time
            call_count += 1
            if call_count == 1:
                start_time = time.time()
                raise RateLimitError("Rate limited", "test", retry_after=1)
            return "success"

        config = RetryConfig(max_retries=3, base_delay=0.01)
        result = await with_retry(rate_limited_with_retry_after, config, "test")

        assert result == "success"
        assert call_count == 2
        # Should have waited at least 1 second (the retry_after value)
        elapsed = time.time() - start_time
        assert elapsed >= 1.0


class TestRetryDecorator:
    """Tests for retry_decorator."""

    @pytest.mark.asyncio
    async def test_decorator_wraps_function(self):
        """Decorator wraps function with retry logic."""
        call_count = 0

        @retry_decorator(config=RetryConfig(max_retries=2, base_delay=0.01))
        async def decorated_func():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise RateLimitError("Rate limited", "test")
            return "success"

        result = await decorated_func()

        assert result == "success"
        assert call_count == 2

    @pytest.mark.asyncio
    async def test_decorator_preserves_function_name(self):
        """Decorator preserves function metadata."""

        @retry_decorator()
        async def my_named_function():
            """My docstring."""
            return "value"

        assert my_named_function.__name__ == "my_named_function"
        assert my_named_function.__doc__ == "My docstring."

    @pytest.mark.asyncio
    async def test_decorator_with_default_config(self):
        """Decorator works with default config."""
        call_count = 0

        @retry_decorator()
        async def func_with_defaults():
            nonlocal call_count
            call_count += 1
            return "success"

        result = await func_with_defaults()

        assert result == "success"
        assert call_count == 1
