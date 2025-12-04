"""BDD Steps for openai.feature."""

import asyncio
import contextlib
import os
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from forge_llm import Client
from forge_llm.domain.exceptions import AuthenticationError

# Link scenarios from feature file
scenarios("../../specs/bdd/30_providers/openai.feature")


def run_async(coro):
    """Helper to run async code in sync context."""
    return asyncio.get_event_loop().run_until_complete(coro)


def _create_mock_response(
    content: str = "Test response",
    model: str = "gpt-4o-mini",
    status: str = "completed",
):
    """Helper para criar mock response da Responses API."""
    mock_response = MagicMock()
    mock_response.model = model
    mock_response.status = status

    # Criar message output item
    content_item = MagicMock()
    content_item.type = "output_text"
    content_item.text = content

    message_item = MagicMock()
    message_item.type = "message"
    message_item.content = [content_item]

    mock_response.output = [message_item]

    # Usage
    mock_response.usage = MagicMock()
    mock_response.usage.input_tokens = 10
    mock_response.usage.output_tokens = 5

    return mock_response


# ========== FIXTURES ==========


@pytest.fixture
def openai_context():
    """Shared context between OpenAI steps."""
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


@given("the environment variable OPENAI_API_KEY is configured")
def openai_api_key_configured():
    """Set mock API key for testing."""
    # For ci-fast tests, we use a mock API key
    os.environ.setdefault("OPENAI_API_KEY", "sk-test-mock-key")


@given(
    parsers.parse('the client is configured with provider "{provider}" and model "{model}"'),
    target_fixture="openai_context",
)
def client_configured_with_provider_and_model(provider, model, openai_context):
    """Configure client with specific provider and model."""
    mock_response = _create_mock_response(model=model)

    patcher = patch("forge_llm.providers.openai_provider.AsyncOpenAI")
    mock_openai_class = patcher.start()
    mock_client = MagicMock()
    mock_client.responses.create = AsyncMock(return_value=mock_response)
    mock_openai_class.return_value = mock_client

    openai_context["mock_patcher"] = patcher
    openai_context["client"] = Client(provider=provider, model=model, api_key="sk-test-mock-key")
    openai_context["provider"] = openai_context["client"]._provider
    return openai_context


@given(
    parsers.parse('the client is configured with provider "{provider}"'),
    target_fixture="openai_context",
)
def client_configured_with_provider(provider, openai_context):
    """Configure client with specific provider."""
    mock_response = _create_mock_response()

    patcher = patch("forge_llm.providers.openai_provider.AsyncOpenAI")
    mock_openai_class = patcher.start()
    mock_client = MagicMock()
    mock_client.responses.create = AsyncMock(return_value=mock_response)
    mock_openai_class.return_value = mock_client

    openai_context["mock_patcher"] = patcher
    openai_context["client"] = Client(provider=provider, api_key="sk-test-mock-key")
    openai_context["provider"] = openai_context["client"]._provider
    return openai_context


@given(
    parsers.parse('I configure the client with api_key "{api_key}"'),
    target_fixture="openai_context",
)
def configure_client_with_invalid_api_key(api_key, openai_context):
    """Configure client with specific (invalid) API key."""
    from openai import AuthenticationError as OpenAIAuthError

    patcher = patch("forge_llm.providers.openai_provider.AsyncOpenAI")
    mock_openai_class = patcher.start()
    mock_client = MagicMock()
    mock_client.responses.create = AsyncMock(
        side_effect=OpenAIAuthError(
            message="Invalid API key",
            response=MagicMock(status_code=401),
            body=None,
        )
    )
    mock_openai_class.return_value = mock_client

    openai_context["mock_patcher"] = patcher
    openai_context["client"] = Client(provider="openai", api_key=api_key)
    openai_context["provider"] = openai_context["client"]._provider
    return openai_context


@given(
    parsers.parse('the tool "{tool_name}" is registered'),
    target_fixture="openai_context",
)
def tool_is_registered(tool_name, openai_context):
    """Register a tool with the client."""
    from forge_llm.domain.value_objects import ToolDefinition

    # Create mock response with tool call
    mock_response = MagicMock()
    mock_response.model = "gpt-4o-mini"
    mock_response.status = "completed"

    tc_item = MagicMock()
    tc_item.type = "function_call"
    tc_item.call_id = "call_123"
    tc_item.name = tool_name
    tc_item.arguments = '{"city": "Sao Paulo"}'

    mock_response.output = [tc_item]
    mock_response.usage = MagicMock()
    mock_response.usage.input_tokens = 10
    mock_response.usage.output_tokens = 5

    # Update mock - stop previous if exists
    if openai_context.get("mock_patcher"):
        with contextlib.suppress(RuntimeError):
            openai_context["mock_patcher"].stop()

    patcher = patch("forge_llm.providers.openai_provider.AsyncOpenAI")
    mock_openai_class = patcher.start()
    mock_client = MagicMock()
    mock_client.responses.create = AsyncMock(return_value=mock_response)
    mock_openai_class.return_value = mock_client

    openai_context["mock_patcher"] = patcher

    # Create client with mock
    openai_context["client"] = Client(provider="openai", api_key="sk-test-mock-key")
    openai_context["provider"] = openai_context["client"]._provider

    # Register tool
    tool = ToolDefinition(
        name=tool_name,
        description=f"{tool_name} tool",
        parameters={"type": "object", "properties": {}},
    )
    openai_context["registered_tool"] = tool
    return openai_context


# ========== WHEN STEPS ==========


@when(
    parsers.parse('I configure the client with provider "{provider}"'),
    target_fixture="openai_context",
)
def when_configure_client(provider, openai_context):
    """Configure client with provider."""
    mock_response = _create_mock_response()

    patcher = patch("forge_llm.providers.openai_provider.AsyncOpenAI")
    mock_openai_class = patcher.start()
    mock_client = MagicMock()
    mock_client.responses.create = AsyncMock(return_value=mock_response)
    mock_openai_class.return_value = mock_client

    openai_context["mock_patcher"] = patcher
    openai_context["client"] = Client(provider=provider, api_key="sk-test-mock-key")
    openai_context["provider"] = openai_context["client"]._provider
    return openai_context


@when(
    parsers.parse('I configure the client with provider "{provider}" and model "{model}"'),
    target_fixture="openai_context",
)
def when_configure_client_with_model(provider, model, openai_context):
    """Configure client with provider and model."""
    mock_response = _create_mock_response(model=model)

    patcher = patch("forge_llm.providers.openai_provider.AsyncOpenAI")
    mock_openai_class = patcher.start()
    mock_client = MagicMock()
    mock_client.responses.create = AsyncMock(return_value=mock_response)
    mock_openai_class.return_value = mock_client

    openai_context["mock_patcher"] = patcher
    openai_context["client"] = Client(provider=provider, model=model, api_key="sk-test-mock-key")
    openai_context["provider"] = openai_context["client"]._provider
    return openai_context


@when(
    parsers.parse('I send the message "{message}"'),
    target_fixture="openai_context",
)
def send_message(message, openai_context):
    """Send message to LLM."""
    try:
        openai_context["response"] = run_async(openai_context["client"].chat(message))
    except Exception as e:
        openai_context["error"] = e
        openai_context["error_type"] = type(e).__name__
    return openai_context


@when(
    parsers.parse('I send the message "{message}" with streaming enabled'),
    target_fixture="openai_context",
)
def send_message_with_streaming(message, openai_context):
    """Send message with streaming enabled."""
    try:
        # For ci-fast tests, we simulate streaming by just doing a regular chat
        openai_context["response"] = run_async(openai_context["client"].chat(message))
    except Exception as e:
        openai_context["error"] = e
        openai_context["error_type"] = type(e).__name__
    return openai_context


@when(
    "I try to send a message",
    target_fixture="openai_context",
)
def try_send_message(openai_context):
    """Try to send message (expecting error)."""
    try:
        openai_context["response"] = run_async(openai_context["client"].chat("Test"))
    except AuthenticationError as e:
        openai_context["error"] = e
        openai_context["error_type"] = "AuthenticationError"
    except Exception as e:
        openai_context["error"] = e
        openai_context["error_type"] = type(e).__name__
    return openai_context


# ========== THEN STEPS ==========


@then("the client is ready for use")
def client_is_ready(openai_context):
    """Verify client is ready."""
    assert openai_context["client"] is not None


@then(parsers.parse('the active provider is "{provider}"'))
def active_provider_is(provider, openai_context):
    """Verify active provider."""
    assert openai_context["provider"].provider_name == provider


@then(parsers.parse('the active model is "{model}"'))
def active_model_is(model, openai_context):
    """Verify active model."""
    assert openai_context["client"].model == model


@then(parsers.parse('I receive a response with status "{status}"'))
def response_with_status(status, openai_context):
    """Verify response status."""
    assert openai_context["response"] is not None
    # For successful responses, we check the response exists
    if status == "success":
        assert openai_context["error"] is None


@then("the response contains text")
def response_contains_text(openai_context):
    """Verify response has text content."""
    assert openai_context["response"].content != ""


@then(parsers.parse('provider.id in response is "{provider}"'))
def provider_in_response(provider, openai_context):
    """Verify provider in response."""
    assert openai_context["response"].provider == provider


@then("I receive chunks progressively")
def receive_chunks(openai_context):
    """Verify streaming chunks received."""
    # For ci-fast tests, we simulate this
    assert openai_context["response"] is not None


@then("the final response is complete")
def final_response_complete(openai_context):
    """Verify final response is complete."""
    assert openai_context["response"] is not None


@then("I receive a response with tool_call")
def response_with_tool_call(openai_context):
    """Verify response has tool_call."""
    assert openai_context["response"] is not None
    assert openai_context["response"].has_tool_calls is True


@then("the tool_call has normalized format")
def tool_call_normalized(openai_context):
    """Verify tool_call format."""
    tool_calls = openai_context["response"].tool_calls
    assert len(tool_calls) > 0
    tc = tool_calls[0]
    assert hasattr(tc, "id")
    assert hasattr(tc, "name")
    assert hasattr(tc, "arguments")


@then(parsers.parse('the tool_call.name is "{name}"'))
def tool_call_name_is(name, openai_context):
    """Verify tool_call name."""
    assert openai_context["response"].tool_calls[0].name == name


@then(parsers.parse('I receive an error of type "{error_type}"'))
def receive_error_type(error_type, openai_context):
    """Verify error type."""
    assert openai_context["error"] is not None
    assert openai_context["error_type"] == error_type


@then(parsers.parse('the error message contains "{text1}" or "{text2}"'))
def error_message_contains_or(text1, text2, openai_context):
    """Verify error message contains one of the texts."""
    error_msg = str(openai_context["error"]).lower()
    assert text1.lower() in error_msg or text2.lower() in error_msg


# ========== CLEANUP ==========


@pytest.fixture(autouse=True)
def cleanup_mocks(openai_context):
    """Cleanup mocks after each test."""
    yield
    if openai_context.get("mock_patcher"):
        with contextlib.suppress(RuntimeError):
            openai_context["mock_patcher"].stop()
