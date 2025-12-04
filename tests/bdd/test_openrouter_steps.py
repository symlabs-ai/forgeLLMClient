"""BDD steps for OpenRouter provider tests."""

import asyncio
import os

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from forge_llm.domain.exceptions import AuthenticationError
from forge_llm.domain.value_objects import ImageContent, Message
from forge_llm.providers.openrouter_provider import OpenRouterProvider

# Load scenarios from feature file
scenarios("../../specs/bdd/10_forge_core/openrouter.feature")


def run_async(coro):
    """Run async coroutine in sync context."""
    return asyncio.get_event_loop().run_until_complete(coro)


@pytest.fixture
def context():
    """Shared context for steps."""
    return {}


# Given steps


@given("an OpenRouter provider with API key")
def openrouter_provider_with_key(context):
    """Create provider with real or mock API key."""
    api_key = os.getenv("OPENROUTER_API_KEY", "test-key-for-unit-tests")
    context["provider"] = OpenRouterProvider(api_key=api_key)
    context["has_real_key"] = os.getenv("OPENROUTER_API_KEY") is not None


@given(parsers.parse('an OpenRouter provider with invalid API key "{api_key}"'))
def openrouter_provider_invalid_key(context, api_key):
    """Create provider with invalid API key."""
    context["provider"] = OpenRouterProvider(api_key=api_key)
    context["has_real_key"] = False
    context["expect_auth_error"] = True


@given(
    parsers.parse(
        'a message with text "{text}" and image URL "{url}"'
    )
)
def message_with_image(context, text, url):
    """Create message with text and image."""
    image = ImageContent(url=url)
    context["message"] = Message(role="user", content=[text, image])


@given(parsers.parse('a tool definition for "{tool_name}" with parameter "{param}"'))
def tool_definition(context, tool_name, param):
    """Create tool definition."""
    context["tools"] = [
        {
            "type": "function",
            "function": {
                "name": tool_name,
                "description": f"Get {tool_name.replace('_', ' ')}",
                "parameters": {
                    "type": "object",
                    "properties": {
                        param: {"type": "string", "description": f"The {param}"}
                    },
                    "required": [param],
                },
            },
        }
    ]


# When steps


@when(parsers.parse('I send a message "{text}"'))
def send_message(context, text):
    """Send a simple message."""
    from unittest.mock import AsyncMock, MagicMock

    provider = context["provider"]
    messages = [Message(role="user", content=text)]

    # Skip real API calls if no real key
    if not context.get("has_real_key"):
        # Check if we expect an auth error
        if context.get("expect_auth_error"):
            from openai import AuthenticationError as OpenAIAuthError

            provider._client.chat.completions.create = AsyncMock(
                side_effect=OpenAIAuthError(
                    message="Invalid API key",
                    response=MagicMock(status_code=401),
                    body=None,
                )
            )
        else:
            # Mock the response for testing
            choice = MagicMock()
            choice.message.content = "hello"
            choice.message.tool_calls = None
            choice.finish_reason = "stop"

            usage = MagicMock()
            usage.prompt_tokens = 5
            usage.completion_tokens = 1

            mock_response = MagicMock()
            mock_response.choices = [choice]
            mock_response.model = "openai/gpt-4o-mini"
            mock_response.usage = usage

            provider._client.chat.completions.create = AsyncMock(
                return_value=mock_response
            )

    try:
        context["response"] = run_async(provider.chat(messages))
        context["error"] = None
    except Exception as e:
        context["response"] = None
        context["error"] = e


@when(parsers.parse('I send a message "{text}" with model "{model}"'))
def send_message_with_model(context, text, model):
    """Send message with specific model."""
    provider = context["provider"]
    messages = [Message(role="user", content=text)]

    if not context.get("has_real_key"):
        from unittest.mock import AsyncMock, MagicMock

        choice = MagicMock()
        choice.message.content = "test"
        choice.message.tool_calls = None
        choice.finish_reason = "stop"

        usage = MagicMock()
        usage.prompt_tokens = 5
        usage.completion_tokens = 1

        mock_response = MagicMock()
        mock_response.choices = [choice]
        mock_response.model = model
        mock_response.usage = usage

        provider._client.chat.completions.create = AsyncMock(
            return_value=mock_response
        )

    context["response"] = run_async(provider.chat(messages, model=model))


@when(parsers.parse('I send a streaming message "{text}"'))
def send_streaming_message(context, text):
    """Send a streaming message."""
    provider = context["provider"]
    messages = [Message(role="user", content=text)]

    if not context.get("has_real_key"):
        from unittest.mock import AsyncMock, MagicMock

        async def mock_stream():
            for word in ["1", " ", "2", " ", "3"]:
                chunk = MagicMock()
                chunk.choices = [MagicMock()]
                chunk.choices[0].delta.content = word
                chunk.choices[0].finish_reason = None
                yield chunk

            final = MagicMock()
            final.choices = [MagicMock()]
            final.choices[0].delta.content = ""
            final.choices[0].finish_reason = "stop"
            yield final

        provider._client.chat.completions.create = AsyncMock(
            return_value=mock_stream()
        )

    async def collect_stream():
        chunks = []
        async for chunk in provider.chat_stream(messages):
            chunks.append(chunk)
        return chunks

    context["chunks"] = run_async(collect_stream())


@when("I send the message with images")
def send_message_with_images(context):
    """Send message that has images."""
    provider = context["provider"]
    message = context["message"]
    messages = [message]

    if not context.get("has_real_key"):
        from unittest.mock import AsyncMock, MagicMock

        choice = MagicMock()
        choice.message.content = "This is a cat"
        choice.message.tool_calls = None
        choice.finish_reason = "stop"

        usage = MagicMock()
        usage.prompt_tokens = 50
        usage.completion_tokens = 10

        mock_response = MagicMock()
        mock_response.choices = [choice]
        mock_response.model = "openai/gpt-4o-mini"
        mock_response.usage = usage

        provider._client.chat.completions.create = AsyncMock(
            return_value=mock_response
        )

    context["response"] = run_async(provider.chat(messages))


@when(parsers.parse('I send a message "{text}" with tools'))
def send_message_with_tools(context, text):
    """Send message with tools."""
    provider = context["provider"]
    messages = [Message(role="user", content=text)]
    tools = context.get("tools", [])

    if not context.get("has_real_key"):
        from unittest.mock import AsyncMock, MagicMock

        tool_call = MagicMock()
        tool_call.id = "call_123"
        tool_call.function.name = "get_weather"
        tool_call.function.arguments = '{"location": "Paris"}'

        choice = MagicMock()
        choice.message.content = None
        choice.message.tool_calls = [tool_call]
        choice.finish_reason = "tool_calls"

        usage = MagicMock()
        usage.prompt_tokens = 20
        usage.completion_tokens = 15

        mock_response = MagicMock()
        mock_response.choices = [choice]
        mock_response.model = "openai/gpt-4o-mini"
        mock_response.usage = usage

        provider._client.chat.completions.create = AsyncMock(
            return_value=mock_response
        )

    context["response"] = run_async(provider.chat(messages, tools=tools))


# Then steps


@then("I should receive a response")
def should_receive_response(context):
    """Verify response was received."""
    assert context.get("response") is not None
    assert context.get("error") is None


@then("the response should contain text")
def response_contains_text(context):
    """Verify response has text content."""
    response = context["response"]
    assert response.content is not None
    assert len(response.content) > 0


@then(parsers.parse('the provider name should be "{name}"'))
def provider_name_should_be(context, name):
    """Verify provider name."""
    response = context["response"]
    assert response.provider == name


@then(parsers.parse('the response model should contain "{model_part}"'))
def response_model_contains(context, model_part):
    """Verify model name contains expected part."""
    response = context["response"]
    assert model_part in response.model


@then("I should receive streaming chunks")
def should_receive_chunks(context):
    """Verify streaming chunks were received."""
    chunks = context.get("chunks", [])
    assert len(chunks) > 0


@then("the final response should be complete")
def final_response_complete(context):
    """Verify streaming completed."""
    chunks = context.get("chunks", [])
    # Verify we received multiple chunks with content
    content = "".join(c["delta"]["content"] for c in chunks)
    assert len(content) > 0, "Should have received content"
    # Check that streaming produced some chunks
    assert len(chunks) > 1, "Should have multiple chunks"


@then("I should receive an authentication error")
def should_receive_auth_error(context):
    """Verify authentication error was raised."""
    error = context.get("error")
    assert error is not None
    assert isinstance(error, AuthenticationError)


@then("I should receive a response describing the image")
def response_describes_image(context):
    """Verify response describes the image."""
    response = context["response"]
    assert response.content is not None
    # In mock mode, we just check there's content
    assert len(response.content) > 0


@then(parsers.parse('I should receive a tool call for "{tool_name}"'))
def should_receive_tool_call(context, tool_name):
    """Verify tool call was received."""
    response = context["response"]
    assert len(response.tool_calls) > 0
    tool_names = [tc.name for tc in response.tool_calls]
    assert tool_name in tool_names


@then(parsers.parse('the tool call should have argument "{arg_name}"'))
def tool_call_has_argument(context, arg_name):
    """Verify tool call has expected argument."""
    response = context["response"]
    tool_call = response.tool_calls[0]
    assert arg_name in tool_call.arguments
