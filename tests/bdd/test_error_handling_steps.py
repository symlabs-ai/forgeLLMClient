"""BDD steps for error handling and retry feature."""

import asyncio
import time

import pytest
from pytest_bdd import given, parsers, scenario, then, when

from forge_llm.domain.entities import ChatResponse, TokenUsage
from forge_llm.domain.exceptions import (
    APITimeoutError,
    AuthenticationError,
    RateLimitError,
    RetryExhaustedError,
)
from forge_llm.infrastructure.retry import RetryConfig, with_retry


def run_async(coro):
    """Helper to run async code in sync context."""
    return asyncio.get_event_loop().run_until_complete(coro)


@scenario(
    "../../specs/bdd/10_forge_core/error_handling.feature",
    "Successful request without retry",
)
def test_successful_request_without_retry():
    """Test successful request without retry."""
    pass


@scenario(
    "../../specs/bdd/10_forge_core/error_handling.feature",
    "Retry on rate limit error",
)
def test_retry_on_rate_limit_error():
    """Test retry on rate limit error."""
    pass


@scenario(
    "../../specs/bdd/10_forge_core/error_handling.feature",
    "Retry on timeout error",
)
def test_retry_on_timeout_error():
    """Test retry on timeout error."""
    pass


@scenario(
    "../../specs/bdd/10_forge_core/error_handling.feature",
    "No retry on authentication error",
)
def test_no_retry_on_authentication_error():
    """Test no retry on authentication error."""
    pass


@scenario(
    "../../specs/bdd/10_forge_core/error_handling.feature",
    "Exhaust all retries",
)
def test_exhaust_all_retries():
    """Test exhaust all retries."""
    pass


@scenario(
    "../../specs/bdd/10_forge_core/error_handling.feature",
    "Respect retry-after header",
)
def test_respect_retry_after_header():
    """Test respect retry-after header."""
    pass


@pytest.fixture
def error_context():
    """Fixture for error handling context."""
    return {
        "config": None,
        "mock_func": None,
        "call_count": 0,
        "result": None,
        "error": None,
        "start_time": None,
        "end_time": None,
    }


@given(
    parsers.parse(
        "a retry configuration with max_retries {max_retries:d} and base_delay {base_delay:f}"
    )
)
def given_retry_config(error_context, max_retries, base_delay):
    """Create retry configuration."""
    error_context["config"] = RetryConfig(
        max_retries=max_retries, base_delay=base_delay, jitter=False
    )


@given("a mock provider that succeeds immediately")
def given_mock_succeeds(error_context):
    """Create mock that succeeds immediately."""

    async def mock_func():
        error_context["call_count"] += 1
        return ChatResponse(
            content="OK",
            model="mock",
            provider="mock",
            usage=TokenUsage(prompt_tokens=1, completion_tokens=1, total_tokens=2),
        )

    error_context["mock_func"] = mock_func


@given(
    parsers.parse(
        "a mock provider that fails with rate limit {fail_count:d} times then succeeds"
    )
)
def given_mock_rate_limit_then_succeeds(error_context, fail_count):
    """Create mock that fails with rate limit then succeeds."""

    async def mock_func():
        error_context["call_count"] += 1
        if error_context["call_count"] <= fail_count:
            raise RateLimitError("Rate limited", "mock")
        return ChatResponse(
            content="OK",
            model="mock",
            provider="mock",
            usage=TokenUsage(prompt_tokens=1, completion_tokens=1, total_tokens=2),
        )

    error_context["mock_func"] = mock_func


@given(
    parsers.parse(
        "a mock provider that fails with timeout {fail_count:d} time then succeeds"
    )
)
def given_mock_timeout_then_succeeds(error_context, fail_count):
    """Create mock that fails with timeout then succeeds."""

    async def mock_func():
        error_context["call_count"] += 1
        if error_context["call_count"] <= fail_count:
            raise APITimeoutError("Timeout", "mock")
        return ChatResponse(
            content="OK",
            model="mock",
            provider="mock",
            usage=TokenUsage(prompt_tokens=1, completion_tokens=1, total_tokens=2),
        )

    error_context["mock_func"] = mock_func


@given("a mock provider that fails with authentication error")
def given_mock_auth_error(error_context):
    """Create mock that fails with authentication error."""

    async def mock_func():
        error_context["call_count"] += 1
        raise AuthenticationError("Invalid key", "mock")

    error_context["mock_func"] = mock_func


@given("a mock provider that always fails with rate limit")
def given_mock_always_rate_limit(error_context):
    """Create mock that always fails with rate limit."""

    async def mock_func():
        error_context["call_count"] += 1
        raise RateLimitError("Rate limited", "mock")

    error_context["mock_func"] = mock_func


@given(
    parsers.parse(
        "a mock provider that fails with rate limit and retry_after {seconds:d} second"
    )
)
def given_mock_rate_limit_with_retry_after(error_context, seconds):
    """Create mock that fails with rate limit and retry_after."""

    async def mock_func():
        error_context["call_count"] += 1
        if error_context["call_count"] == 1:
            raise RateLimitError("Rate limited", "mock", retry_after=seconds)
        return ChatResponse(
            content="OK",
            model="mock",
            provider="mock",
            usage=TokenUsage(prompt_tokens=1, completion_tokens=1, total_tokens=2),
        )

    error_context["mock_func"] = mock_func


@when("I make a chat request with retry enabled")
def when_make_request_with_retry(error_context):
    """Make a request with retry enabled."""
    error_context["start_time"] = time.time()
    try:
        error_context["result"] = run_async(
            with_retry(
                error_context["mock_func"],
                error_context["config"],
                "mock",
            )
        )
    except Exception as e:
        error_context["error"] = e
    error_context["end_time"] = time.time()


@then("the request should succeed")
def then_request_succeeds(error_context):
    """Verify request succeeded."""
    assert error_context["error"] is None
    assert error_context["result"] is not None


@then(parsers.parse("the provider should be called {count:d} time"))
@then(parsers.parse("the provider should be called {count:d} times"))
def then_provider_called_times(error_context, count):
    """Verify provider call count."""
    assert error_context["call_count"] == count


@then(parsers.parse("the request should fail with {error_type}"))
def then_request_fails_with(error_context, error_type):
    """Verify request failed with specific error type."""
    assert error_context["error"] is not None
    error_classes = {
        "AuthenticationError": AuthenticationError,
        "RetryExhaustedError": RetryExhaustedError,
    }
    assert isinstance(error_context["error"], error_classes[error_type])


@then("the error should contain the original rate limit error")
def then_error_contains_original(error_context):
    """Verify RetryExhaustedError contains original error."""
    assert isinstance(error_context["error"], RetryExhaustedError)
    assert isinstance(error_context["error"].last_error, RateLimitError)


@then(parsers.parse("the retry should wait at least {seconds:d} second"))
def then_retry_waits(error_context, seconds):
    """Verify retry waited the expected time."""
    elapsed = error_context["end_time"] - error_context["start_time"]
    assert elapsed >= seconds
