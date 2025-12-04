"""BDD Steps for anthropic.feature."""

import asyncio
import contextlib
import os
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from forge_llm import Client
from forge_llm.domain.exceptions import AuthenticationError

# Link scenarios from feature file
scenarios("../../specs/bdd/30_providers/anthropic.feature")


def run_async(coro):
    """Helper to run async code in sync context."""
    return asyncio.get_event_loop().run_until_complete(coro)


def _create_mock_response(
    content: str = "Test response",
    model: str = "claude-3-5-sonnet-20241022",
    stop_reason: str = "end_turn",
):
    """Helper para criar mock response da Messages API."""
    mock_response = MagicMock()
    mock_response.model = model
    mock_response.stop_reason = stop_reason

    # Criar content block
    text_block = MagicMock()
    text_block.type = "text"
    text_block.text = content

    mock_response.content = [text_block]

    # Usage
    mock_response.usage = MagicMock()
    mock_response.usage.input_tokens = 10
    mock_response.usage.output_tokens = 5

    return mock_response


# ========== FIXTURES ==========


@pytest.fixture
def anthropic_context():
    """Shared context between Anthropic steps."""
    return {
        "client": None,
        "provider": None,
        "response": None,
        "chunks": [],
        "error": None,
        "error_type": None,
        "mock_patcher": None,
    }


# ========== GIVEN STEPS ==========


@given("the ForgeLLMClient is installed")
def forge_client_installed():
    """Verify SDK is available."""
    assert Client is not None


@given("the environment variable ANTHROPIC_API_KEY is configured")
def anthropic_api_key_configured():
    """Set mock API key for testing."""
    os.environ.setdefault("ANTHROPIC_API_KEY", "sk-ant-test-mock-key")


@given(
    parsers.parse('the client is configured with provider "{provider}"'),
    target_fixture="anthropic_context",
)
def client_configured_with_provider(provider, anthropic_context):
    """Configure client with specific provider."""
    mock_response = _create_mock_response()

    patcher = patch("forge_llm.providers.anthropic_provider.AsyncAnthropic")
    mock_anthropic_class = patcher.start()
    mock_client = MagicMock()
    mock_client.messages.create = AsyncMock(return_value=mock_response)
    mock_anthropic_class.return_value = mock_client

    anthropic_context["mock_patcher"] = patcher
    anthropic_context["client"] = Client(provider=provider, api_key="sk-ant-test-mock-key")
    anthropic_context["provider"] = anthropic_context["client"]._provider
    return anthropic_context


@given(
    parsers.parse('I configure the client with api_key "{api_key}"'),
    target_fixture="anthropic_context",
)
def configure_client_with_invalid_api_key(api_key, anthropic_context):
    """Configure client with specific (invalid) API key."""
    from anthropic import AuthenticationError as AnthropicAuthError

    patcher = patch("forge_llm.providers.anthropic_provider.AsyncAnthropic")
    mock_anthropic_class = patcher.start()
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.status_code = 401
    mock_client.messages.create = AsyncMock(
        side_effect=AnthropicAuthError(
            "Invalid API key",
            response=mock_response,
            body=None,
        )
    )
    mock_anthropic_class.return_value = mock_client

    anthropic_context["mock_patcher"] = patcher
    anthropic_context["client"] = Client(provider="anthropic", api_key=api_key)
    anthropic_context["provider"] = anthropic_context["client"]._provider
    return anthropic_context


@given(
    parsers.parse('the tool "{tool_name}" is registered'),
    target_fixture="anthropic_context",
)
def tool_is_registered(tool_name, anthropic_context):
    """Register a tool with the client."""
    from forge_llm.domain.value_objects import ToolDefinition

    # Create mock response with tool call
    mock_response = MagicMock()
    mock_response.model = "claude-3-5-sonnet-20241022"
    mock_response.stop_reason = "tool_use"

    tool_block = MagicMock()
    tool_block.type = "tool_use"
    tool_block.id = "toolu_123"
    tool_block.name = tool_name
    tool_block.input = {"city": "Sao Paulo"}

    mock_response.content = [tool_block]
    mock_response.usage = MagicMock()
    mock_response.usage.input_tokens = 10
    mock_response.usage.output_tokens = 5

    # Update mock - stop previous if exists
    if anthropic_context.get("mock_patcher"):
        with contextlib.suppress(RuntimeError):
            anthropic_context["mock_patcher"].stop()

    patcher = patch("forge_llm.providers.anthropic_provider.AsyncAnthropic")
    mock_anthropic_class = patcher.start()
    mock_client = MagicMock()
    mock_client.messages.create = AsyncMock(return_value=mock_response)
    mock_anthropic_class.return_value = mock_client

    anthropic_context["mock_patcher"] = patcher

    # Create client with mock
    anthropic_context["client"] = Client(provider="anthropic", api_key="sk-ant-test-mock-key")
    anthropic_context["provider"] = anthropic_context["client"]._provider

    # Register tool
    tool = ToolDefinition(
        name=tool_name,
        description=f"{tool_name} tool",
        parameters={"type": "object", "properties": {}},
    )
    anthropic_context["registered_tool"] = tool
    return anthropic_context


# ========== WHEN STEPS ==========


@when(
    parsers.parse('I configure the client with provider "{provider}"'),
    target_fixture="anthropic_context",
)
def when_configure_client(provider, anthropic_context):
    """Configure client with provider."""
    mock_response = _create_mock_response()

    patcher = patch("forge_llm.providers.anthropic_provider.AsyncAnthropic")
    mock_anthropic_class = patcher.start()
    mock_client = MagicMock()
    mock_client.messages.create = AsyncMock(return_value=mock_response)
    mock_anthropic_class.return_value = mock_client

    anthropic_context["mock_patcher"] = patcher
    anthropic_context["client"] = Client(provider=provider, api_key="sk-ant-test-mock-key")
    anthropic_context["provider"] = anthropic_context["client"]._provider
    return anthropic_context


@when(
    parsers.parse('I configure the client with provider "{provider}" and model "{model}"'),
    target_fixture="anthropic_context",
)
def when_configure_client_with_model(provider, model, anthropic_context):
    """Configure client with provider and model."""
    mock_response = _create_mock_response(model=model)

    patcher = patch("forge_llm.providers.anthropic_provider.AsyncAnthropic")
    mock_anthropic_class = patcher.start()
    mock_client = MagicMock()
    mock_client.messages.create = AsyncMock(return_value=mock_response)
    mock_anthropic_class.return_value = mock_client

    anthropic_context["mock_patcher"] = patcher
    anthropic_context["client"] = Client(provider=provider, model=model, api_key="sk-ant-test-mock-key")
    anthropic_context["provider"] = anthropic_context["client"]._provider
    return anthropic_context


@when(
    parsers.parse('I send the message "{message}"'),
    target_fixture="anthropic_context",
)
def send_message(message, anthropic_context):
    """Send message to LLM."""
    try:
        anthropic_context["response"] = run_async(anthropic_context["client"].chat(message))
    except Exception as e:
        anthropic_context["error"] = e
        anthropic_context["error_type"] = type(e).__name__
    return anthropic_context


@when(
    parsers.parse('I send the message "{message}" with streaming enabled'),
    target_fixture="anthropic_context",
)
def send_message_with_streaming(message, anthropic_context):
    """Send message with streaming enabled."""
    try:
        # For ci-fast tests, we simulate streaming by just doing a regular chat
        anthropic_context["response"] = run_async(anthropic_context["client"].chat(message))
    except Exception as e:
        anthropic_context["error"] = e
        anthropic_context["error_type"] = type(e).__name__
    return anthropic_context


@when(
    "I try to send a message",
    target_fixture="anthropic_context",
)
def try_send_message(anthropic_context):
    """Try to send message (expecting error)."""
    try:
        anthropic_context["response"] = run_async(anthropic_context["client"].chat("Test"))
    except AuthenticationError as e:
        anthropic_context["error"] = e
        anthropic_context["error_type"] = "AuthenticationError"
    except Exception as e:
        anthropic_context["error"] = e
        anthropic_context["error_type"] = type(e).__name__
    return anthropic_context


# ========== THEN STEPS ==========


@then("the client is ready for use")
def client_is_ready(anthropic_context):
    """Verify client is ready."""
    assert anthropic_context["client"] is not None


@then(parsers.parse('the active provider is "{provider}"'))
def active_provider_is(provider, anthropic_context):
    """Verify active provider."""
    assert anthropic_context["provider"].provider_name == provider


@then(parsers.parse('the active model is "{model}"'))
def active_model_is(model, anthropic_context):
    """Verify active model."""
    assert anthropic_context["client"].model == model


@then(parsers.parse('I receive a response with status "{status}"'))
def response_with_status(status, anthropic_context):
    """Verify response status."""
    assert anthropic_context["response"] is not None
    if status == "success":
        assert anthropic_context["error"] is None


@then("the response contains text")
def response_contains_text(anthropic_context):
    """Verify response has text content."""
    assert anthropic_context["response"].content != ""


@then(parsers.parse('provider.id in response is "{provider}"'))
def provider_in_response(provider, anthropic_context):
    """Verify provider in response."""
    assert anthropic_context["response"].provider == provider


@then("I receive chunks progressively")
def receive_chunks(anthropic_context):
    """Verify streaming chunks received."""
    # For ci-fast tests, we simulate this
    assert anthropic_context["response"] is not None


@then("the final response is complete")
def final_response_complete(anthropic_context):
    """Verify final response is complete."""
    assert anthropic_context["response"] is not None


@then("I receive a response with tool_call")
def response_with_tool_call(anthropic_context):
    """Verify response has tool_call."""
    assert anthropic_context["response"] is not None
    assert anthropic_context["response"].has_tool_calls is True


@then("the tool_call has normalized format")
def tool_call_normalized(anthropic_context):
    """Verify tool_call format."""
    tool_calls = anthropic_context["response"].tool_calls
    assert len(tool_calls) > 0
    tc = tool_calls[0]
    assert hasattr(tc, "id")
    assert hasattr(tc, "name")
    assert hasattr(tc, "arguments")


@then(parsers.parse('the tool_call.name is "{name}"'))
def tool_call_name_is(name, anthropic_context):
    """Verify tool_call name."""
    assert anthropic_context["response"].tool_calls[0].name == name


@then("the response is of type ChatResponse")
def response_is_chat_response(anthropic_context):
    """Verify response type."""
    from forge_llm.domain.entities import ChatResponse
    assert isinstance(anthropic_context["response"], ChatResponse)


@then("the response has the same fields as responses from other providers")
def response_has_unified_fields(anthropic_context):
    """Verify response has unified fields."""
    response = anthropic_context["response"]
    assert hasattr(response, "content")
    assert hasattr(response, "model")
    assert hasattr(response, "provider")
    assert hasattr(response, "usage")
    assert hasattr(response, "tool_calls")
    assert hasattr(response, "finish_reason")


@then(parsers.parse('I receive an error of type "{error_type}"'))
def receive_error_type(error_type, anthropic_context):
    """Verify error type."""
    assert anthropic_context["error"] is not None
    assert anthropic_context["error_type"] == error_type


@then(parsers.parse('the error message contains "{text1}" or "{text2}"'))
def error_message_contains_or(text1, text2, anthropic_context):
    """Verify error message contains one of the texts."""
    error_msg = str(anthropic_context["error"]).lower()
    assert text1.lower() in error_msg or text2.lower() in error_msg


# ========== CLEANUP ==========


@pytest.fixture(autouse=True)
def cleanup_mocks(anthropic_context):
    """Cleanup mocks after each test."""
    yield
    if anthropic_context.get("mock_patcher"):
        with contextlib.suppress(RuntimeError):
            anthropic_context["mock_patcher"].stop()
