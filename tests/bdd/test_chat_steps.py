"""BDD Steps for chat.feature."""

import asyncio

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from forge_llm import ChatResponse, Client, ValidationError

# Link scenarios from feature file
scenarios("../../specs/bdd/10_forge_core/chat.feature")


def run_async(coro):
    """Helper to run async code in sync context."""
    return asyncio.get_event_loop().run_until_complete(coro)


# ========== FIXTURES ==========


@pytest.fixture
def chat_context():
    """Shared context between chat steps."""
    return {
        "client": None,
        "response": None,
        "chunks": [],
        "error": None,
        "error_type": None,
    }


# ========== GIVEN STEPS ==========


@given("the ForgeLLMClient is installed")
def forge_client_installed():
    """Verify SDK is available."""
    assert Client is not None


@given("the test environment is configured")
def test_environment_configured():
    """Verify test environment is ready."""
    # Mock provider is always available for tests
    pass


@given(
    parsers.parse("the client is configured with provider \"{provider}\""),
    target_fixture="chat_context",
)
def client_configured_with_provider(provider, chat_context):
    """Configure client with specific provider."""
    chat_context["client"] = Client(provider=provider)
    return chat_context


@given(
    "the client is NOT configured with any provider",
    target_fixture="chat_context",
)
def client_not_configured(chat_context):
    """Create client without configuration."""
    chat_context["client"] = Client()
    return chat_context


# ========== WHEN STEPS ==========


@when(
    parsers.parse("I send the message \"{message}\""),
    target_fixture="chat_context",
)
def send_message(message, chat_context):
    """Send message to LLM."""
    try:
        chat_context["response"] = run_async(chat_context["client"].chat(message))
    except Exception as e:
        chat_context["error"] = e
        chat_context["error_type"] = type(e).__name__
    return chat_context


@when(
    parsers.parse("I send the message \"{message}\" with temperature {temperature:f}"),
    target_fixture="chat_context",
)
def send_message_with_temperature(message, temperature, chat_context):
    """Send message with custom temperature."""
    try:
        chat_context["response"] = run_async(
            chat_context["client"].chat(message, temperature=temperature)
        )
    except Exception as e:
        chat_context["error"] = e
        chat_context["error_type"] = type(e).__name__
    return chat_context


@when(
    parsers.parse("I send the message \"{message}\" with streaming enabled"),
    target_fixture="chat_context",
)
def send_message_with_streaming(message, chat_context):
    """Send message with streaming."""

    async def collect_chunks():
        chunks = []
        async for chunk in chat_context["client"].chat_stream(message):
            chunks.append(chunk)
        return chunks

    try:
        chat_context["chunks"] = run_async(collect_chunks())
    except Exception as e:
        chat_context["error"] = e
        chat_context["error_type"] = type(e).__name__
    return chat_context


@when(
    "I try to send a message",
    target_fixture="chat_context",
)
def try_send_message(chat_context):
    """Try to send message (may fail)."""
    try:
        chat_context["response"] = run_async(
            chat_context["client"].chat("Test message")
        )
    except RuntimeError as e:
        chat_context["error"] = e
        chat_context["error_type"] = "RuntimeError"
    except Exception as e:
        chat_context["error"] = e
        chat_context["error_type"] = type(e).__name__
    return chat_context


@when(
    "I send an empty message",
    target_fixture="chat_context",
)
def send_empty_message(chat_context):
    """Send empty message (should fail)."""
    try:
        chat_context["response"] = run_async(chat_context["client"].chat(""))
    except ValidationError as e:
        chat_context["error"] = e
        chat_context["error_type"] = "ValidationError"
    except Exception as e:
        chat_context["error"] = e
        chat_context["error_type"] = type(e).__name__
    return chat_context


# ========== THEN STEPS ==========


@then(parsers.parse("I receive a response with status \"{status}\""))
def response_has_status(status, chat_context):
    """Verify response status."""
    if status == "success":
        assert chat_context["response"] is not None
        assert chat_context["error"] is None


@then("the response contains non-empty text")
def response_has_text(chat_context):
    """Verify response has text content."""
    assert chat_context["response"].content
    assert len(chat_context["response"].content) > 0


@then("the response has valid ChatResponse format")
def response_is_chat_response(chat_context):
    """Verify response is ChatResponse instance."""
    assert isinstance(chat_context["response"], ChatResponse)
    assert chat_context["response"].model is not None
    assert chat_context["response"].provider is not None
    assert chat_context["response"].usage is not None


@then("I receive response chunks progressively")
def received_chunks(chat_context):
    """Verify chunks were received."""
    assert len(chat_context["chunks"]) > 0


@then("the last chunk indicates end of stream")
def last_chunk_is_end(chat_context):
    """Verify last chunk has finish_reason."""
    last_chunk = chat_context["chunks"][-1]
    assert last_chunk.get("finish_reason") == "stop"


@then("the final response is complete")
def final_response_complete(chat_context):
    """Verify all chunks form complete response."""
    # Combine all chunk deltas to verify content
    content_parts = []
    for chunk in chat_context["chunks"]:
        if "delta" in chunk and "content" in chunk["delta"]:
            content_parts.append(chunk["delta"]["content"])
    full_content = "".join(content_parts)
    assert len(full_content) > 0


@then(parsers.parse("I receive an error of type \"{error_type}\""))
def received_error_type(error_type, chat_context):
    """Verify error type received."""
    assert chat_context["error"] is not None
    assert chat_context["error_type"] == error_type


@then(parsers.parse("the error message contains \"{text}\""))
def error_message_contains(text, chat_context):
    """Verify error message contains text."""
    error_message = str(chat_context["error"]).lower()
    assert text.lower() in error_message, f"'{text}' not in '{error_message}'"
