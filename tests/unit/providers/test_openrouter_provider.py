"""Unit tests for OpenRouterProvider."""

import warnings
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from forge_llm.domain.exceptions import AuthenticationError, RateLimitError
from forge_llm.domain.value_objects import ImageContent, Message
from forge_llm.providers.openrouter_provider import (
    DEFAULT_MODEL,
    OPENROUTER_BASE_URL,
    OpenRouterProvider,
)


class TestOpenRouterProviderProperties:
    """Tests for OpenRouterProvider properties."""

    @pytest.fixture
    def provider(self):
        """Create provider instance."""
        return OpenRouterProvider(api_key="test-key")

    def test_provider_name(self, provider):
        """Provider name should be 'openrouter'."""
        assert provider.provider_name == "openrouter"

    def test_supports_streaming(self, provider):
        """Provider should support streaming."""
        assert provider.supports_streaming is True

    def test_supports_tool_calling(self, provider):
        """Provider should support tool calling."""
        assert provider.supports_tool_calling is True

    def test_default_model(self, provider):
        """Default model should be openai/gpt-4o-mini."""
        assert provider.default_model == "openai/gpt-4o-mini"
        assert provider.default_model == DEFAULT_MODEL

    def test_custom_model(self):
        """Provider should accept custom model."""
        provider = OpenRouterProvider(
            api_key="test-key",
            model="anthropic/claude-3-opus",
        )
        assert provider.default_model == "anthropic/claude-3-opus"


class TestOpenRouterProviderInit:
    """Tests for OpenRouterProvider initialization."""

    def test_init_with_api_key(self):
        """Provider should initialize with API key."""
        provider = OpenRouterProvider(api_key="test-key")
        assert provider._api_key == "test-key"

    def test_init_with_site_url(self):
        """Provider should accept site_url."""
        provider = OpenRouterProvider(
            api_key="test-key",
            site_url="https://myapp.com",
        )
        assert provider._site_url == "https://myapp.com"

    def test_init_with_site_name(self):
        """Provider should accept site_name."""
        provider = OpenRouterProvider(
            api_key="test-key",
            site_name="My App",
        )
        assert provider._site_name == "My App"

    def test_base_url_is_openrouter(self):
        """Client should use OpenRouter base URL."""
        provider = OpenRouterProvider(api_key="test-key")
        assert provider._client.base_url.host == "openrouter.ai"


class TestOpenRouterMessageConversion:
    """Tests for message conversion."""

    @pytest.fixture
    def provider(self):
        """Create provider instance."""
        return OpenRouterProvider(api_key="test-key")

    def test_convert_simple_message(self, provider):
        """Convert simple text message."""
        messages = [Message(role="user", content="Hello")]
        result = provider._convert_messages(messages)

        assert len(result) == 1
        assert result[0]["role"] == "user"
        assert result[0]["content"] == "Hello"

    def test_convert_system_message(self, provider):
        """Convert system message."""
        messages = [Message(role="system", content="You are helpful")]
        result = provider._convert_messages(messages)

        assert len(result) == 1
        assert result[0]["role"] == "system"
        assert result[0]["content"] == "You are helpful"

    def test_convert_assistant_message(self, provider):
        """Convert assistant message."""
        messages = [Message(role="assistant", content="Hi there")]
        result = provider._convert_messages(messages)

        assert len(result) == 1
        assert result[0]["role"] == "assistant"
        assert result[0]["content"] == "Hi there"

    def test_convert_tool_message(self, provider):
        """Convert tool message with tool_call_id."""
        messages = [
            Message(
                role="tool",
                content='{"result": "sunny"}',
                tool_call_id="call_123",
            )
        ]
        result = provider._convert_messages(messages)

        assert len(result) == 1
        assert result[0]["role"] == "tool"
        assert result[0]["tool_call_id"] == "call_123"

    def test_convert_multiple_messages(self, provider):
        """Convert conversation with multiple messages."""
        messages = [
            Message(role="system", content="Be helpful"),
            Message(role="user", content="Hello"),
            Message(role="assistant", content="Hi!"),
        ]
        result = provider._convert_messages(messages)

        assert len(result) == 3
        assert result[0]["role"] == "system"
        assert result[1]["role"] == "user"
        assert result[2]["role"] == "assistant"


class TestOpenRouterImageFormatting:
    """Tests for image formatting."""

    @pytest.fixture
    def provider(self):
        """Create provider instance."""
        return OpenRouterProvider(api_key="test-key")

    def test_format_image_url(self, provider):
        """Format image with URL."""
        image = ImageContent(url="https://example.com/img.jpg")
        result = provider._format_image(image)

        assert result["type"] == "image_url"
        assert result["image_url"]["url"] == "https://example.com/img.jpg"

    def test_format_image_base64(self, provider):
        """Format image with base64."""
        image = ImageContent(base64_data="abc123", media_type="image/png")
        result = provider._format_image(image)

        assert result["type"] == "image_url"
        assert result["image_url"]["url"] == "data:image/png;base64,abc123"

    def test_convert_message_with_image(self, provider):
        """Convert message with image content."""
        image = ImageContent(url="https://example.com/img.jpg")
        messages = [Message(role="user", content=["Describe this", image])]
        result = provider._convert_messages(messages)

        assert len(result) == 1
        content = result[0]["content"]
        assert len(content) == 2
        assert content[0]["type"] == "text"
        assert content[0]["text"] == "Describe this"
        assert content[1]["type"] == "image_url"


class TestOpenRouterChat:
    """Tests for chat method."""

    @pytest.fixture
    def provider(self):
        """Create provider instance."""
        return OpenRouterProvider(api_key="test-key")

    @pytest.fixture
    def mock_response(self):
        """Create mock API response."""
        choice = MagicMock()
        choice.message.content = "Hello there!"
        choice.message.tool_calls = None
        choice.finish_reason = "stop"

        usage = MagicMock()
        usage.prompt_tokens = 10
        usage.completion_tokens = 5

        response = MagicMock()
        response.choices = [choice]
        response.model = "openai/gpt-4o-mini"
        response.usage = usage

        return response

    @pytest.mark.asyncio
    async def test_chat_basic(self, provider, mock_response):
        """Test basic chat call."""
        provider._client.chat.completions.create = AsyncMock(
            return_value=mock_response
        )

        messages = [Message(role="user", content="Hello")]
        response = await provider.chat(messages)

        assert response.content == "Hello there!"
        assert response.provider == "openrouter"
        assert response.model == "openai/gpt-4o-mini"
        assert response.usage.prompt_tokens == 10
        assert response.usage.completion_tokens == 5

    @pytest.mark.asyncio
    async def test_chat_with_custom_model(self, provider, mock_response):
        """Test chat with custom model."""
        provider._client.chat.completions.create = AsyncMock(
            return_value=mock_response
        )

        messages = [Message(role="user", content="Hello")]
        await provider.chat(messages, model="anthropic/claude-3-opus")

        call_kwargs = provider._client.chat.completions.create.call_args.kwargs
        assert call_kwargs["model"] == "anthropic/claude-3-opus"

    @pytest.mark.asyncio
    async def test_chat_with_temperature(self, provider, mock_response):
        """Test chat with custom temperature."""
        provider._client.chat.completions.create = AsyncMock(
            return_value=mock_response
        )

        messages = [Message(role="user", content="Hello")]
        await provider.chat(messages, temperature=0.5)

        call_kwargs = provider._client.chat.completions.create.call_args.kwargs
        assert call_kwargs["temperature"] == 0.5

    @pytest.mark.asyncio
    async def test_chat_with_max_tokens(self, provider, mock_response):
        """Test chat with max_tokens."""
        provider._client.chat.completions.create = AsyncMock(
            return_value=mock_response
        )

        messages = [Message(role="user", content="Hello")]
        await provider.chat(messages, max_tokens=100)

        call_kwargs = provider._client.chat.completions.create.call_args.kwargs
        assert call_kwargs["max_tokens"] == 100

    @pytest.mark.asyncio
    async def test_chat_authentication_error(self, provider):
        """Test authentication error handling."""
        from openai import AuthenticationError as OpenAIAuthError

        provider._client.chat.completions.create = AsyncMock(
            side_effect=OpenAIAuthError(
                message="Invalid API key",
                response=MagicMock(status_code=401),
                body=None,
            )
        )

        messages = [Message(role="user", content="Hello")]

        with pytest.raises(AuthenticationError) as exc_info:
            await provider.chat(messages)

        assert exc_info.value.provider == "openrouter"

    @pytest.mark.asyncio
    async def test_chat_rate_limit_error(self, provider):
        """Test rate limit error handling."""
        from openai import RateLimitError as OpenAIRateLimitError

        provider._client.chat.completions.create = AsyncMock(
            side_effect=OpenAIRateLimitError(
                message="Rate limit exceeded",
                response=MagicMock(status_code=429),
                body=None,
            )
        )

        messages = [Message(role="user", content="Hello")]

        with pytest.raises(RateLimitError) as exc_info:
            await provider.chat(messages)

        assert exc_info.value.provider == "openrouter"


class TestOpenRouterToolCalling:
    """Tests for tool calling."""

    @pytest.fixture
    def provider(self):
        """Create provider instance."""
        return OpenRouterProvider(api_key="test-key")

    @pytest.fixture
    def mock_tool_response(self):
        """Create mock response with tool calls."""
        tool_call = MagicMock()
        tool_call.id = "call_123"
        tool_call.function.name = "get_weather"
        tool_call.function.arguments = '{"location": "Paris"}'

        choice = MagicMock()
        choice.message.content = None
        choice.message.tool_calls = [tool_call]
        choice.finish_reason = "tool_calls"

        usage = MagicMock()
        usage.prompt_tokens = 15
        usage.completion_tokens = 10

        response = MagicMock()
        response.choices = [choice]
        response.model = "openai/gpt-4o-mini"
        response.usage = usage

        return response

    @pytest.mark.asyncio
    async def test_chat_with_tools(self, provider, mock_tool_response):
        """Test chat with tool calling."""
        provider._client.chat.completions.create = AsyncMock(
            return_value=mock_tool_response
        )

        messages = [Message(role="user", content="Weather in Paris?")]
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_weather",
                    "description": "Get weather",
                    "parameters": {
                        "type": "object",
                        "properties": {"location": {"type": "string"}},
                    },
                },
            }
        ]

        response = await provider.chat(messages, tools=tools)

        assert len(response.tool_calls) == 1
        assert response.tool_calls[0].name == "get_weather"
        assert response.tool_calls[0].arguments == {"location": "Paris"}
        assert response.tool_calls[0].id == "call_123"


class TestOpenRouterStreaming:
    """Tests for streaming."""

    @pytest.fixture
    def provider(self):
        """Create provider instance."""
        return OpenRouterProvider(api_key="test-key")

    @pytest.mark.asyncio
    async def test_chat_stream(self, provider):
        """Test streaming response."""

        async def mock_stream():
            for text in ["Hello", " ", "World"]:
                chunk = MagicMock()
                chunk.choices = [MagicMock()]
                chunk.choices[0].delta.content = text
                chunk.choices[0].finish_reason = None
                yield chunk

            # Final chunk
            final = MagicMock()
            final.choices = [MagicMock()]
            final.choices[0].delta.content = ""
            final.choices[0].finish_reason = "stop"
            yield final

        provider._client.chat.completions.create = AsyncMock(
            return_value=mock_stream()
        )

        messages = [Message(role="user", content="Hello")]
        chunks = []
        async for chunk in provider.chat_stream(messages):
            chunks.append(chunk)

        assert len(chunks) == 4
        assert chunks[0]["delta"]["content"] == "Hello"
        assert chunks[1]["delta"]["content"] == " "
        assert chunks[2]["delta"]["content"] == "World"
        assert chunks[3]["finish_reason"] == "stop"

    @pytest.mark.asyncio
    async def test_chat_stream_with_max_tokens(self, provider):
        """Test streaming with max_tokens parameter."""

        async def mock_stream():
            chunk = MagicMock()
            chunk.choices = [MagicMock()]
            chunk.choices[0].delta.content = "Test"
            chunk.choices[0].finish_reason = "stop"
            yield chunk

        provider._client.chat.completions.create = AsyncMock(
            return_value=mock_stream()
        )

        messages = [Message(role="user", content="Hello")]
        chunks = []
        async for chunk in provider.chat_stream(messages, max_tokens=50):
            chunks.append(chunk)

        assert len(chunks) == 1
        # Verify max_tokens was passed
        call_kwargs = provider._client.chat.completions.create.call_args.kwargs
        assert call_kwargs["max_tokens"] == 50

    @pytest.mark.asyncio
    async def test_chat_stream_with_tools(self, provider):
        """Test streaming with tools parameter."""

        async def mock_stream():
            chunk = MagicMock()
            chunk.choices = [MagicMock()]
            chunk.choices[0].delta.content = "Test"
            chunk.choices[0].finish_reason = "stop"
            yield chunk

        provider._client.chat.completions.create = AsyncMock(
            return_value=mock_stream()
        )

        messages = [Message(role="user", content="Weather?")]
        tools = [{"type": "function", "function": {"name": "test"}}]
        chunks = []
        async for chunk in provider.chat_stream(messages, tools=tools):
            chunks.append(chunk)

        assert len(chunks) == 1
        # Verify tools was passed
        call_kwargs = provider._client.chat.completions.create.call_args.kwargs
        assert call_kwargs["tools"] == tools

    @pytest.mark.asyncio
    async def test_chat_stream_authentication_error(self, provider):
        """Test streaming authentication error handling."""
        from openai import AuthenticationError as OpenAIAuthError

        async def mock_stream(**kwargs):
            raise OpenAIAuthError(
                message="Invalid API key",
                response=MagicMock(status_code=401),
                body=None,
            )

        provider._client.chat.completions.create = AsyncMock(
            side_effect=mock_stream
        )

        messages = [Message(role="user", content="Hello")]

        with pytest.raises(AuthenticationError) as exc_info:
            async for _ in provider.chat_stream(messages):
                pass

        assert exc_info.value.provider == "openrouter"

    @pytest.mark.asyncio
    async def test_chat_stream_rate_limit_error(self, provider):
        """Test streaming rate limit error handling."""
        from openai import RateLimitError as OpenAIRateLimitError

        async def mock_stream(**kwargs):
            raise OpenAIRateLimitError(
                message="Rate limit exceeded",
                response=MagicMock(status_code=429),
                body=None,
            )

        provider._client.chat.completions.create = AsyncMock(
            side_effect=mock_stream
        )

        messages = [Message(role="user", content="Hello")]

        with pytest.raises(RateLimitError) as exc_info:
            async for _ in provider.chat_stream(messages):
                pass

        assert exc_info.value.provider == "openrouter"


class TestOpenRouterModelValidation:
    """Tests for model format validation."""

    def test_valid_model_format_no_warning(self):
        """Valid model format should not emit warning."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            OpenRouterProvider(api_key="test-key", model="openai/gpt-4o")
            assert len(w) == 0

    def test_invalid_model_format_emits_warning(self):
        """Invalid model format should emit warning."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            OpenRouterProvider(api_key="test-key", model="gpt-4o")
            assert len(w) == 1
            assert "nao segue formato OpenRouter" in str(w[0].message)
            assert issubclass(w[0].category, UserWarning)


class TestOpenRouterToolCallParsing:
    """Tests for tool call parsing edge cases."""

    @pytest.fixture
    def provider(self):
        """Create provider instance."""
        return OpenRouterProvider(api_key="test-key")

    def test_parse_tool_calls_with_invalid_json(self, provider):
        """Tool calls with invalid JSON arguments should return empty dict."""
        tool_call = MagicMock()
        tool_call.id = "call_123"
        tool_call.function.name = "test_func"
        tool_call.function.arguments = "invalid json {"

        result = provider._parse_tool_calls([tool_call])

        assert len(result) == 1
        assert result[0].name == "test_func"
        assert result[0].arguments == {}  # Falls back to empty dict

    def test_parse_tool_calls_with_attribute_error(self, provider):
        """Tool calls with missing attributes should return empty dict."""
        tool_call = MagicMock()
        tool_call.id = "call_123"
        tool_call.function.name = "test_func"
        tool_call.function.arguments = None  # Will cause AttributeError

        result = provider._parse_tool_calls([tool_call])

        assert len(result) == 1
        assert result[0].arguments == {}
