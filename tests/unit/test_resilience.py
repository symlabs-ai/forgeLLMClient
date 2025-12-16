"""
Unit tests for resilience utilities.

TDD tests for retry with backoff functionality.
"""
import time
from unittest.mock import MagicMock, patch

import pytest

from forge_llm.infrastructure.resilience import (
    DEFAULT_RETRY_CONFIG,
    RetryConfig,
    retry_on_rate_limit,
    with_retry,
)


class TestWithRetry:
    """Tests for with_retry decorator."""

    def test_succeeds_on_first_try(self):
        """Function succeeds without retries."""
        call_count = 0

        @with_retry(max_attempts=3)
        def succeeds():
            nonlocal call_count
            call_count += 1
            return "success"

        result = succeeds()

        assert result == "success"
        assert call_count == 1

    def test_retries_on_timeout(self):
        """Function retries on TimeoutError."""
        call_count = 0

        @with_retry(max_attempts=3, min_wait=0.01, max_wait=0.1)
        def fails_twice():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise TimeoutError("Timed out")
            return "success"

        result = fails_twice()

        assert result == "success"
        assert call_count == 3

    def test_retries_on_connection_error(self):
        """Function retries on ConnectionError."""
        call_count = 0

        @with_retry(max_attempts=3, min_wait=0.01, max_wait=0.1)
        def fails_once():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise ConnectionError("Connection refused")
            return "success"

        result = fails_once()

        assert result == "success"
        assert call_count == 2

    def test_raises_after_max_attempts(self):
        """Function raises after max retries exhausted."""
        call_count = 0

        @with_retry(max_attempts=3, min_wait=0.01, max_wait=0.1)
        def always_fails():
            nonlocal call_count
            call_count += 1
            raise TimeoutError("Always fails")

        with pytest.raises(TimeoutError):
            always_fails()

        assert call_count == 3

    def test_does_not_retry_on_non_retryable_exception(self):
        """Non-retryable exceptions are raised immediately."""
        call_count = 0

        @with_retry(max_attempts=3)
        def raises_value_error():
            nonlocal call_count
            call_count += 1
            raise ValueError("Not retryable")

        with pytest.raises(ValueError):
            raises_value_error()

        assert call_count == 1

    def test_custom_retryable_exceptions(self):
        """Can specify custom retryable exceptions."""
        call_count = 0

        class CustomError(Exception):
            pass

        @with_retry(
            max_attempts=3,
            min_wait=0.01,
            max_wait=0.1,
            retryable_exceptions=(CustomError,),
        )
        def fails_with_custom():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise CustomError("Custom error")
            return "success"

        result = fails_with_custom()

        assert result == "success"
        assert call_count == 2


class TestRetryOnRateLimit:
    """Tests for retry_on_rate_limit decorator."""

    def test_retries_on_429_error(self):
        """Retries when error contains 429."""
        call_count = 0

        @retry_on_rate_limit(max_attempts=3, min_wait=0.01, max_wait=0.1)
        def rate_limited():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise Exception("Error 429: Too Many Requests")
            return "success"

        result = rate_limited()

        assert result == "success"
        assert call_count == 2

    def test_retries_on_rate_limit_message(self):
        """Retries when error mentions rate limit."""
        call_count = 0

        @retry_on_rate_limit(max_attempts=3, min_wait=0.01, max_wait=0.1)
        def rate_limited():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise Exception("Rate limit exceeded")
            return "success"

        result = rate_limited()

        assert result == "success"
        assert call_count == 2

    def test_does_not_retry_other_errors(self):
        """Does not retry non-rate-limit errors."""
        call_count = 0

        @retry_on_rate_limit(max_attempts=3)
        def raises_other_error():
            nonlocal call_count
            call_count += 1
            raise ValueError("Some other error")

        with pytest.raises(ValueError):
            raises_other_error()

        assert call_count == 1


class TestRetryConfig:
    """Tests for RetryConfig class."""

    def test_default_values(self):
        """RetryConfig has sensible defaults."""
        config = RetryConfig()

        assert config.max_attempts == 3
        assert config.min_wait == 1.0
        assert config.max_wait == 60.0
        assert config.multiplier == 2.0
        assert config.retry_on_timeout is True
        assert config.retry_on_connection_error is True
        assert config.retry_on_rate_limit is True

    def test_custom_values(self):
        """Can customize RetryConfig values."""
        config = RetryConfig(
            max_attempts=5,
            min_wait=2.0,
            max_wait=120.0,
            multiplier=3.0,
            retry_on_timeout=False,
            retry_on_connection_error=True,
            retry_on_rate_limit=False,
        )

        assert config.max_attempts == 5
        assert config.min_wait == 2.0
        assert config.max_wait == 120.0
        assert config.multiplier == 3.0
        assert config.retry_on_timeout is False
        assert config.retry_on_connection_error is True
        assert config.retry_on_rate_limit is False

    def test_should_retry_timeout(self):
        """should_retry returns True for TimeoutError when enabled."""
        config = RetryConfig(retry_on_timeout=True)
        assert config.should_retry(TimeoutError()) is True

        config_disabled = RetryConfig(retry_on_timeout=False)
        assert config_disabled.should_retry(TimeoutError()) is False

    def test_should_retry_connection_error(self):
        """should_retry returns True for ConnectionError when enabled."""
        config = RetryConfig(retry_on_connection_error=True)
        assert config.should_retry(ConnectionError()) is True

        config_disabled = RetryConfig(retry_on_connection_error=False)
        assert config_disabled.should_retry(ConnectionError()) is False

    def test_should_retry_rate_limit(self):
        """should_retry returns True for rate limit errors when enabled."""
        config = RetryConfig(retry_on_rate_limit=True)

        assert config.should_retry(Exception("Rate limit exceeded")) is True
        assert config.should_retry(Exception("Error 429")) is True
        assert config.should_retry(Exception("Too many requests")) is True

        config_disabled = RetryConfig(retry_on_rate_limit=False)
        assert config_disabled.should_retry(Exception("Rate limit exceeded")) is False

    def test_should_retry_non_retryable(self):
        """should_retry returns False for non-retryable exceptions."""
        config = RetryConfig()

        assert config.should_retry(ValueError("Some error")) is False
        assert config.should_retry(TypeError("Type error")) is False

    def test_get_retry_decorator(self):
        """get_retry_decorator returns a working decorator."""
        config = RetryConfig(max_attempts=2, min_wait=0.01, max_wait=0.1)
        decorator = config.get_retry_decorator()

        call_count = 0

        @decorator
        def fails_once():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise TimeoutError()
            return "success"

        result = fails_once()

        assert result == "success"
        assert call_count == 2


class TestDefaultRetryConfig:
    """Tests for DEFAULT_RETRY_CONFIG."""

    def test_default_config_exists(self):
        """DEFAULT_RETRY_CONFIG is a valid RetryConfig."""
        assert isinstance(DEFAULT_RETRY_CONFIG, RetryConfig)
        assert DEFAULT_RETRY_CONFIG.max_attempts == 3
