"""
Resilience - Retry and fault tolerance utilities.

Provides retry decorators with exponential backoff for API calls.
"""
from __future__ import annotations

import logging
from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, TypeVar

from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

P = ParamSpec("P")
R = TypeVar("R")


# Exceptions that should trigger retry
RETRYABLE_EXCEPTIONS = (
    TimeoutError,
    ConnectionError,
    OSError,
)


def with_retry(
    max_attempts: int = 3,
    min_wait: float = 1.0,
    max_wait: float = 60.0,
    multiplier: float = 2.0,
    retryable_exceptions: tuple[type[Exception], ...] | None = None,
    logger: logging.Logger | None = None,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Decorator that adds retry with exponential backoff.

    Args:
        max_attempts: Maximum number of retry attempts (default: 3)
        min_wait: Minimum wait time between retries in seconds (default: 1.0)
        max_wait: Maximum wait time between retries in seconds (default: 60.0)
        multiplier: Exponential backoff multiplier (default: 2.0)
        retryable_exceptions: Tuple of exception types to retry on
        logger: Optional logger for retry attempts

    Returns:
        Decorated function with retry logic

    Usage:
        @with_retry(max_attempts=5)
        def call_api():
            ...

        # Or with custom exceptions
        @with_retry(retryable_exceptions=(RateLimitError,))
        def rate_limited_call():
            ...
    """
    exceptions = retryable_exceptions or RETRYABLE_EXCEPTIONS

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        retry_decorator = retry(
            stop=stop_after_attempt(max_attempts),
            wait=wait_exponential(
                multiplier=multiplier,
                min=min_wait,
                max=max_wait,
            ),
            retry=retry_if_exception_type(exceptions),
            before_sleep=(
                before_sleep_log(logger, logging.WARNING) if logger else None
            ),
            reraise=True,
        )
        return retry_decorator(func)

    return decorator


def retry_on_rate_limit(
    max_attempts: int = 5,
    min_wait: float = 1.0,
    max_wait: float = 120.0,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Decorator specifically for rate limit errors.

    Uses longer wait times as rate limits often need more time to reset.

    Args:
        max_attempts: Maximum number of retry attempts (default: 5)
        min_wait: Minimum wait time between retries in seconds (default: 1.0)
        max_wait: Maximum wait time between retries in seconds (default: 120.0)

    Returns:
        Decorated function with retry logic for rate limits
    """

    def is_rate_limit_error(exc: BaseException) -> bool:
        """Check if exception is a rate limit error."""
        error_str = str(exc).lower()
        return (
            "rate" in error_str
            and ("limit" in error_str or "exceeded" in error_str)
        ) or "429" in error_str or "too many requests" in error_str

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            last_exception: Exception | None = None
            wait_time = min_wait

            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if is_rate_limit_error(e):
                        last_exception = e
                        if attempt < max_attempts - 1:
                            import time

                            time.sleep(min(wait_time, max_wait))
                            wait_time *= 2
                    else:
                        raise

            if last_exception:
                raise last_exception
            raise RuntimeError("Unexpected state in retry logic")

        return wrapper

    return decorator


class RetryConfig:
    """
    Configuration for retry behavior.

    Usage:
        config = RetryConfig(max_attempts=5, min_wait=2.0)
        adapter = SomeAdapter(retry_config=config)
    """

    def __init__(
        self,
        max_attempts: int = 3,
        min_wait: float = 1.0,
        max_wait: float = 60.0,
        multiplier: float = 2.0,
        retry_on_timeout: bool = True,
        retry_on_connection_error: bool = True,
        retry_on_rate_limit: bool = True,
    ) -> None:
        self.max_attempts = max_attempts
        self.min_wait = min_wait
        self.max_wait = max_wait
        self.multiplier = multiplier
        self.retry_on_timeout = retry_on_timeout
        self.retry_on_connection_error = retry_on_connection_error
        self.retry_on_rate_limit = retry_on_rate_limit

    def should_retry(self, exception: Exception) -> bool:
        """Determine if an exception should trigger a retry."""
        if isinstance(exception, TimeoutError) and self.retry_on_timeout:
            return True
        if isinstance(exception, ConnectionError) and self.retry_on_connection_error:
            return True

        # Check for rate limit in exception message
        error_str = str(exception).lower()
        return self.retry_on_rate_limit and (
            ("rate" in error_str and "limit" in error_str)
            or "429" in error_str
            or "too many requests" in error_str
        )

    def get_retry_decorator(
        self,
        logger: logging.Logger | None = None,
    ) -> Callable[[Callable[P, R]], Callable[P, R]]:
        """Get a retry decorator configured with these settings."""
        exceptions: list[type[Exception]] = []
        if self.retry_on_timeout:
            exceptions.append(TimeoutError)
        if self.retry_on_connection_error:
            exceptions.append(ConnectionError)
            exceptions.append(OSError)

        return with_retry(
            max_attempts=self.max_attempts,
            min_wait=self.min_wait,
            max_wait=self.max_wait,
            multiplier=self.multiplier,
            retryable_exceptions=tuple(exceptions) if exceptions else None,
            logger=logger,
        )


# Default retry configuration
DEFAULT_RETRY_CONFIG = RetryConfig()
