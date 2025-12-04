"""Testes para AnthropicProvider - usando Messages API."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest


class TestAnthropicProviderBasics:
    """Testes basicos para AnthropicProvider."""

    def test_anthropic_provider_implements_provider_port(self):
        """AnthropicProvider deve implementar ProviderPort."""
        from forge_llm.application.ports import ProviderPort
        from forge_llm.providers import AnthropicProvider

        assert issubclass(AnthropicProvider, ProviderPort)

    def test_anthropic_provider_creation_with_api_key(self):
        """AnthropicProvider deve aceitar api_key."""
        from forge_llm.providers import AnthropicProvider

        provider = AnthropicProvider(api_key="sk-ant-test123")
        assert provider is not None

    def test_anthropic_provider_name(self):
        """AnthropicProvider deve ter provider_name = 'anthropic'."""
        from forge_llm.providers import AnthropicProvider

        provider = AnthropicProvider(api_key="sk-ant-test123")
        assert provider.provider_name == "anthropic"

    def test_anthropic_provider_supports_streaming(self):
        """AnthropicProvider deve suportar streaming."""
        from forge_llm.providers import AnthropicProvider

        provider = AnthropicProvider(api_key="sk-ant-test123")
        assert provider.supports_streaming is True

    def test_anthropic_provider_supports_tool_calling(self):
        """AnthropicProvider deve suportar tool calling."""
        from forge_llm.providers import AnthropicProvider

        provider = AnthropicProvider(api_key="sk-ant-test123")
        assert provider.supports_tool_calling is True

    def test_anthropic_provider_default_model(self):
        """AnthropicProvider deve ter modelo padrao claude-sonnet-4."""
        from forge_llm.providers import AnthropicProvider

        provider = AnthropicProvider(api_key="sk-ant-test123")
        assert "claude" in provider.default_model.lower()
        assert "sonnet" in provider.default_model.lower()

    def test_anthropic_provider_custom_model(self):
        """AnthropicProvider deve aceitar modelo customizado."""
        from forge_llm.providers import AnthropicProvider

        provider = AnthropicProvider(
            api_key="sk-ant-test123", model="claude-3-opus-20240229"
        )
        assert provider.default_model == "claude-3-opus-20240229"


def _create_mock_response(
    content: str = "Hello!",
    model: str = "claude-3-5-sonnet-20241022",
    tool_calls: list | None = None,
    stop_reason: str = "end_turn",
    input_tokens: int = 10,
    output_tokens: int = 5,
):
    """Helper para criar mock response da Messages API."""
    mock_response = MagicMock()
    mock_response.model = model
    mock_response.stop_reason = stop_reason

    # Criar content blocks
    content_blocks = []

    if content:
        text_block = MagicMock()
        text_block.type = "text"
        text_block.text = content
        content_blocks.append(text_block)

    if tool_calls:
        for tc in tool_calls:
            tool_block = MagicMock()
            tool_block.type = "tool_use"
            tool_block.id = tc.get("id", "toolu_123")
            tool_block.name = tc.get("name", "function")
            tool_block.input = tc.get("input", {})
            content_blocks.append(tool_block)

    mock_response.content = content_blocks

    # Usage
    mock_response.usage = MagicMock()
    mock_response.usage.input_tokens = input_tokens
    mock_response.usage.output_tokens = output_tokens

    return mock_response


class TestAnthropicProviderChat:
    """Testes para AnthropicProvider.chat usando Messages API."""

    @pytest.mark.asyncio
    async def test_anthropic_provider_chat_returns_response(self):
        """AnthropicProvider.chat deve retornar ChatResponse."""
        from forge_llm.domain.entities import ChatResponse
        from forge_llm.domain.value_objects import Message
        from forge_llm.providers import AnthropicProvider

        mock_response = _create_mock_response(content="Hello!")

        with patch(
            "forge_llm.providers.anthropic_provider.AsyncAnthropic"
        ) as mock_anthropic_class:
            mock_client = MagicMock()
            mock_client.messages.create = AsyncMock(return_value=mock_response)
            mock_anthropic_class.return_value = mock_client

            provider = AnthropicProvider(api_key="sk-ant-test123")
            messages = [Message(role="user", content="Hi")]
            response = await provider.chat(messages)

            assert isinstance(response, ChatResponse)
            assert response.content == "Hello!"
            assert response.provider == "anthropic"

    @pytest.mark.asyncio
    async def test_anthropic_provider_chat_converts_messages(self):
        """AnthropicProvider deve converter Message para formato Messages API."""
        from forge_llm.domain.value_objects import Message
        from forge_llm.providers import AnthropicProvider

        mock_response = _create_mock_response(content="Response")

        with patch(
            "forge_llm.providers.anthropic_provider.AsyncAnthropic"
        ) as mock_anthropic_class:
            mock_client = MagicMock()
            mock_create = AsyncMock(return_value=mock_response)
            mock_client.messages.create = mock_create
            mock_anthropic_class.return_value = mock_client

            provider = AnthropicProvider(api_key="sk-ant-test123")

            messages = [
                Message(role="system", content="You are helpful"),
                Message(role="user", content="Hello"),
            ]
            await provider.chat(messages)

            mock_create.assert_called_once()
            call_kwargs = mock_create.call_args[1]

            # System message vai para parametro system
            assert call_kwargs["system"] == "You are helpful"

            # User message vai para messages
            assert call_kwargs["messages"] == [
                {"role": "user", "content": "Hello"},
            ]

    @pytest.mark.asyncio
    async def test_anthropic_provider_chat_converts_assistant_messages(self):
        """AnthropicProvider deve converter mensagens de assistant corretamente."""
        from forge_llm.domain.value_objects import Message
        from forge_llm.providers import AnthropicProvider

        mock_response = _create_mock_response(content="Response")

        with patch(
            "forge_llm.providers.anthropic_provider.AsyncAnthropic"
        ) as mock_anthropic_class:
            mock_client = MagicMock()
            mock_create = AsyncMock(return_value=mock_response)
            mock_client.messages.create = mock_create
            mock_anthropic_class.return_value = mock_client

            provider = AnthropicProvider(api_key="sk-ant-test123")

            messages = [
                Message(role="user", content="Hello"),
                Message(role="assistant", content="Hi there!"),
                Message(role="user", content="How are you?"),
            ]
            await provider.chat(messages)

            mock_create.assert_called_once()
            call_kwargs = mock_create.call_args[1]

            assert call_kwargs["messages"] == [
                {"role": "user", "content": "Hello"},
                {"role": "assistant", "content": "Hi there!"},
                {"role": "user", "content": "How are you?"},
            ]

    @pytest.mark.asyncio
    async def test_anthropic_provider_chat_converts_tool_results(self):
        """AnthropicProvider deve converter tool results para formato Anthropic."""
        from forge_llm.domain.value_objects import Message
        from forge_llm.providers import AnthropicProvider

        mock_response = _create_mock_response(content="The weather is sunny.")

        with patch(
            "forge_llm.providers.anthropic_provider.AsyncAnthropic"
        ) as mock_anthropic_class:
            mock_client = MagicMock()
            mock_create = AsyncMock(return_value=mock_response)
            mock_client.messages.create = mock_create
            mock_anthropic_class.return_value = mock_client

            provider = AnthropicProvider(api_key="sk-ant-test123")

            messages = [
                Message(role="user", content="What's the weather?"),
                Message(
                    role="tool",
                    content='{"temp": 25, "condition": "sunny"}',
                    tool_call_id="toolu_123",
                ),
            ]
            await provider.chat(messages)

            mock_create.assert_called_once()
            call_kwargs = mock_create.call_args[1]

            # Tool result deve ser convertido para formato Anthropic
            assert call_kwargs["messages"] == [
                {"role": "user", "content": "What's the weather?"},
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": "toolu_123",
                            "content": '{"temp": 25, "condition": "sunny"}',
                        }
                    ],
                },
            ]

    @pytest.mark.asyncio
    async def test_anthropic_provider_chat_uses_provided_model(self):
        """AnthropicProvider deve usar modelo fornecido."""
        from forge_llm.domain.value_objects import Message
        from forge_llm.providers import AnthropicProvider

        mock_response = _create_mock_response(
            content="Response", model="claude-3-opus-20240229"
        )

        with patch(
            "forge_llm.providers.anthropic_provider.AsyncAnthropic"
        ) as mock_anthropic_class:
            mock_client = MagicMock()
            mock_create = AsyncMock(return_value=mock_response)
            mock_client.messages.create = mock_create
            mock_anthropic_class.return_value = mock_client

            provider = AnthropicProvider(api_key="sk-ant-test123")
            messages = [Message(role="user", content="Hi")]
            response = await provider.chat(messages, model="claude-3-opus-20240229")

            assert response.model == "claude-3-opus-20240229"
            call_kwargs = mock_create.call_args[1]
            assert call_kwargs["model"] == "claude-3-opus-20240229"

    @pytest.mark.asyncio
    async def test_anthropic_provider_chat_with_temperature(self):
        """AnthropicProvider deve passar temperature para API."""
        from forge_llm.domain.value_objects import Message
        from forge_llm.providers import AnthropicProvider

        mock_response = _create_mock_response(content="Response")

        with patch(
            "forge_llm.providers.anthropic_provider.AsyncAnthropic"
        ) as mock_anthropic_class:
            mock_client = MagicMock()
            mock_create = AsyncMock(return_value=mock_response)
            mock_client.messages.create = mock_create
            mock_anthropic_class.return_value = mock_client

            provider = AnthropicProvider(api_key="sk-ant-test123")
            messages = [Message(role="user", content="Hi")]
            await provider.chat(messages, temperature=0.5)

            call_kwargs = mock_create.call_args[1]
            assert call_kwargs["temperature"] == 0.5

    @pytest.mark.asyncio
    async def test_anthropic_provider_chat_with_max_tokens(self):
        """AnthropicProvider deve passar max_tokens para API."""
        from forge_llm.domain.value_objects import Message
        from forge_llm.providers import AnthropicProvider

        mock_response = _create_mock_response(content="Response")

        with patch(
            "forge_llm.providers.anthropic_provider.AsyncAnthropic"
        ) as mock_anthropic_class:
            mock_client = MagicMock()
            mock_create = AsyncMock(return_value=mock_response)
            mock_client.messages.create = mock_create
            mock_anthropic_class.return_value = mock_client

            provider = AnthropicProvider(api_key="sk-ant-test123")
            messages = [Message(role="user", content="Hi")]
            await provider.chat(messages, max_tokens=100)

            call_kwargs = mock_create.call_args[1]
            assert call_kwargs["max_tokens"] == 100

    @pytest.mark.asyncio
    async def test_anthropic_provider_chat_returns_usage(self):
        """AnthropicProvider deve retornar uso de tokens."""
        from forge_llm.domain.value_objects import Message
        from forge_llm.providers import AnthropicProvider

        mock_response = _create_mock_response(
            content="Response", input_tokens=10, output_tokens=5
        )

        with patch(
            "forge_llm.providers.anthropic_provider.AsyncAnthropic"
        ) as mock_anthropic_class:
            mock_client = MagicMock()
            mock_client.messages.create = AsyncMock(return_value=mock_response)
            mock_anthropic_class.return_value = mock_client

            provider = AnthropicProvider(api_key="sk-ant-test123")
            messages = [Message(role="user", content="Hi")]
            response = await provider.chat(messages)

            assert response.usage.prompt_tokens == 10
            assert response.usage.completion_tokens == 5
            assert response.usage.total_tokens == 15


class TestAnthropicProviderToolCalling:
    """Testes para tool calling do AnthropicProvider."""

    @pytest.mark.asyncio
    async def test_anthropic_provider_chat_with_tool_call(self):
        """AnthropicProvider deve retornar tool_calls quando presente."""
        from forge_llm.domain.value_objects import Message
        from forge_llm.providers import AnthropicProvider

        mock_response = _create_mock_response(
            content="",
            tool_calls=[
                {
                    "id": "toolu_123",
                    "name": "get_weather",
                    "input": {"location": "SP"},
                }
            ],
        )

        with patch(
            "forge_llm.providers.anthropic_provider.AsyncAnthropic"
        ) as mock_anthropic_class:
            mock_client = MagicMock()
            mock_client.messages.create = AsyncMock(return_value=mock_response)
            mock_anthropic_class.return_value = mock_client

            provider = AnthropicProvider(api_key="sk-ant-test123")
            messages = [Message(role="user", content="Weather in SP?")]
            response = await provider.chat(messages)

            assert response.has_tool_calls is True
            assert len(response.tool_calls) == 1
            assert response.tool_calls[0].name == "get_weather"
            assert response.tool_calls[0].id == "toolu_123"

    @pytest.mark.asyncio
    async def test_anthropic_provider_chat_passes_tools(self):
        """AnthropicProvider deve passar tools para API no formato Anthropic."""
        from forge_llm.domain.value_objects import Message
        from forge_llm.providers import AnthropicProvider

        mock_response = _create_mock_response(content="Response")

        with patch(
            "forge_llm.providers.anthropic_provider.AsyncAnthropic"
        ) as mock_anthropic_class:
            mock_client = MagicMock()
            mock_create = AsyncMock(return_value=mock_response)
            mock_client.messages.create = mock_create
            mock_anthropic_class.return_value = mock_client

            provider = AnthropicProvider(api_key="sk-ant-test123")
            messages = [Message(role="user", content="Hi")]
            tools = [
                {
                    "type": "function",
                    "function": {
                        "name": "get_weather",
                        "description": "Get weather",
                        "parameters": {"type": "object", "properties": {}},
                    },
                }
            ]
            await provider.chat(messages, tools=tools)

            call_kwargs = mock_create.call_args[1]
            # Tools devem ser convertidas para formato Anthropic
            assert call_kwargs["tools"] == [
                {
                    "name": "get_weather",
                    "description": "Get weather",
                    "input_schema": {"type": "object", "properties": {}},
                }
            ]


class TestAnthropicProviderStreaming:
    """Testes para streaming do AnthropicProvider."""

    @pytest.mark.asyncio
    async def test_anthropic_provider_stream_yields_chunks(self):
        """AnthropicProvider.chat_stream deve retornar chunks."""
        from forge_llm.domain.value_objects import Message
        from forge_llm.providers import AnthropicProvider

        # Simular chunks de streaming da Messages API
        async def mock_stream():
            events = [
                MagicMock(type="content_block_delta", delta=MagicMock(text="Hello")),
                MagicMock(type="content_block_delta", delta=MagicMock(text=" world")),
                MagicMock(type="content_block_delta", delta=MagicMock(text="!")),
                MagicMock(type="message_stop"),
            ]
            for event in events:
                yield event

        with patch(
            "forge_llm.providers.anthropic_provider.AsyncAnthropic"
        ) as mock_anthropic_class:
            mock_client = MagicMock()
            mock_client.messages.stream = MagicMock(
                return_value=MagicMock(__aenter__=AsyncMock(return_value=mock_stream()))
            )
            mock_anthropic_class.return_value = mock_client

            provider = AnthropicProvider(api_key="sk-ant-test123")
            messages = [Message(role="user", content="Hi")]
            chunks = []
            async for chunk in provider.chat_stream(messages):
                chunks.append(chunk)

            assert len(chunks) == 4
            assert chunks[0]["delta"]["content"] == "Hello"
            assert chunks[-1]["finish_reason"] == "stop"


class TestAnthropicProviderErrors:
    """Testes de erro para AnthropicProvider."""

    @pytest.mark.asyncio
    async def test_anthropic_provider_authentication_error(self):
        """AnthropicProvider deve lancar AuthenticationError para API key invalida."""
        from anthropic import AuthenticationError as AnthropicAuthError

        from forge_llm.domain.exceptions import AuthenticationError
        from forge_llm.domain.value_objects import Message
        from forge_llm.providers import AnthropicProvider

        with patch(
            "forge_llm.providers.anthropic_provider.AsyncAnthropic"
        ) as mock_anthropic_class:
            mock_client = MagicMock()
            # Anthropic SDK requires response and body for errors
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

            provider = AnthropicProvider(api_key="sk-ant-invalid")
            messages = [Message(role="user", content="Hi")]

            with pytest.raises(AuthenticationError) as exc_info:
                await provider.chat(messages)

            assert (
                "authentication" in str(exc_info.value).lower()
                or "api_key" in str(exc_info.value).lower()
            )
            assert exc_info.value.provider == "anthropic"

    @pytest.mark.asyncio
    async def test_anthropic_provider_rate_limit_error(self):
        """AnthropicProvider deve lancar RateLimitError."""
        from anthropic import RateLimitError as AnthropicRateLimitError

        from forge_llm.domain.exceptions import RateLimitError
        from forge_llm.domain.value_objects import Message
        from forge_llm.providers import AnthropicProvider

        with patch(
            "forge_llm.providers.anthropic_provider.AsyncAnthropic"
        ) as mock_anthropic_class:
            mock_client = MagicMock()
            # Anthropic SDK requires response and body for errors
            mock_response = MagicMock()
            mock_response.status_code = 429
            mock_client.messages.create = AsyncMock(
                side_effect=AnthropicRateLimitError(
                    "Rate limit exceeded",
                    response=mock_response,
                    body=None,
                )
            )
            mock_anthropic_class.return_value = mock_client

            provider = AnthropicProvider(api_key="sk-ant-test123")
            messages = [Message(role="user", content="Hi")]

            with pytest.raises(RateLimitError) as exc_info:
                await provider.chat(messages)

            assert exc_info.value.provider == "anthropic"


class TestAnthropicProviderMessagesAPI:
    """Testes especificos para verificar uso da Messages API."""

    @pytest.mark.asyncio
    async def test_anthropic_provider_uses_messages_api(self):
        """AnthropicProvider DEVE usar messages.create."""
        from forge_llm.domain.value_objects import Message
        from forge_llm.providers import AnthropicProvider

        mock_response = _create_mock_response(content="Response")

        with patch(
            "forge_llm.providers.anthropic_provider.AsyncAnthropic"
        ) as mock_anthropic_class:
            mock_client = MagicMock()
            mock_client.messages.create = AsyncMock(return_value=mock_response)
            mock_anthropic_class.return_value = mock_client

            provider = AnthropicProvider(api_key="sk-ant-test123")
            messages = [Message(role="user", content="Hi")]
            await provider.chat(messages)

            # DEVE chamar messages.create
            mock_client.messages.create.assert_called_once()


class TestAnthropicProviderStreamingAdvanced:
    """Testes avancados para streaming do AnthropicProvider."""

    @pytest.mark.asyncio
    async def test_anthropic_stream_with_system_message(self):
        """AnthropicProvider.chat_stream deve passar system message."""
        from forge_llm.domain.value_objects import Message
        from forge_llm.providers import AnthropicProvider

        async def mock_stream():
            yield MagicMock(type="message_stop")

        with patch(
            "forge_llm.providers.anthropic_provider.AsyncAnthropic"
        ) as mock_anthropic_class:
            mock_client = MagicMock()
            mock_stream_context = MagicMock(
                __aenter__=AsyncMock(return_value=mock_stream())
            )
            mock_client.messages.stream = MagicMock(return_value=mock_stream_context)
            mock_anthropic_class.return_value = mock_client

            provider = AnthropicProvider(api_key="sk-ant-test123")
            messages = [
                Message(role="system", content="Be helpful"),
                Message(role="user", content="Hi"),
            ]

            async for _ in provider.chat_stream(messages):
                pass

            call_kwargs = mock_client.messages.stream.call_args[1]
            assert call_kwargs["system"] == "Be helpful"

    @pytest.mark.asyncio
    async def test_anthropic_stream_with_tools(self):
        """AnthropicProvider.chat_stream deve passar tools."""
        from forge_llm.domain.value_objects import Message
        from forge_llm.providers import AnthropicProvider

        async def mock_stream():
            yield MagicMock(type="message_stop")

        with patch(
            "forge_llm.providers.anthropic_provider.AsyncAnthropic"
        ) as mock_anthropic_class:
            mock_client = MagicMock()
            mock_stream_context = MagicMock(
                __aenter__=AsyncMock(return_value=mock_stream())
            )
            mock_client.messages.stream = MagicMock(return_value=mock_stream_context)
            mock_anthropic_class.return_value = mock_client

            provider = AnthropicProvider(api_key="sk-ant-test123")
            messages = [Message(role="user", content="Hi")]
            tools = [
                {
                    "type": "function",
                    "function": {
                        "name": "get_weather",
                        "description": "Get weather",
                        "parameters": {"type": "object"},
                    },
                }
            ]

            async for _ in provider.chat_stream(messages, tools=tools):
                pass

            call_kwargs = mock_client.messages.stream.call_args[1]
            assert call_kwargs["tools"] is not None

    @pytest.mark.asyncio
    async def test_anthropic_stream_authentication_error(self):
        """AnthropicProvider.chat_stream deve lancar AuthenticationError."""
        from anthropic import AuthenticationError as AnthropicAuthError

        from forge_llm.domain.exceptions import AuthenticationError
        from forge_llm.domain.value_objects import Message
        from forge_llm.providers import AnthropicProvider

        with patch(
            "forge_llm.providers.anthropic_provider.AsyncAnthropic"
        ) as mock_anthropic_class:
            mock_client = MagicMock()
            mock_response = MagicMock(status_code=401)
            mock_client.messages.stream = MagicMock(
                side_effect=AnthropicAuthError(
                    "Invalid API key", response=mock_response, body=None
                )
            )
            mock_anthropic_class.return_value = mock_client

            provider = AnthropicProvider(api_key="sk-ant-invalid")
            messages = [Message(role="user", content="Hi")]

            with pytest.raises(AuthenticationError) as exc_info:
                async for _ in provider.chat_stream(messages):
                    pass

            assert exc_info.value.provider == "anthropic"

    @pytest.mark.asyncio
    async def test_anthropic_stream_rate_limit_error(self):
        """AnthropicProvider.chat_stream deve lancar RateLimitError."""
        from anthropic import RateLimitError as AnthropicRateLimitError

        from forge_llm.domain.exceptions import RateLimitError
        from forge_llm.domain.value_objects import Message
        from forge_llm.providers import AnthropicProvider

        with patch(
            "forge_llm.providers.anthropic_provider.AsyncAnthropic"
        ) as mock_anthropic_class:
            mock_client = MagicMock()
            mock_response = MagicMock(status_code=429)
            mock_client.messages.stream = MagicMock(
                side_effect=AnthropicRateLimitError(
                    "Rate limit exceeded", response=mock_response, body=None
                )
            )
            mock_anthropic_class.return_value = mock_client

            provider = AnthropicProvider(api_key="sk-ant-test123")
            messages = [Message(role="user", content="Hi")]

            with pytest.raises(RateLimitError) as exc_info:
                async for _ in provider.chat_stream(messages):
                    pass

            assert exc_info.value.provider == "anthropic"


class TestAnthropicProviderToolConversion:
    """Testes para conversao de tools."""

    @pytest.mark.asyncio
    async def test_anthropic_tools_non_function_type_preserved(self):
        """AnthropicProvider deve preservar tools sem type=function."""
        from forge_llm.domain.value_objects import Message
        from forge_llm.providers import AnthropicProvider

        mock_response = _create_mock_response(content="Response")

        with patch(
            "forge_llm.providers.anthropic_provider.AsyncAnthropic"
        ) as mock_anthropic_class:
            mock_client = MagicMock()
            mock_create = AsyncMock(return_value=mock_response)
            mock_client.messages.create = mock_create
            mock_anthropic_class.return_value = mock_client

            provider = AnthropicProvider(api_key="sk-ant-test123")
            messages = [Message(role="user", content="Hi")]
            # Tool sem type=function
            tools = [
                {
                    "name": "custom_tool",
                    "description": "A custom tool",
                    "input_schema": {"type": "object"},
                }
            ]
            await provider.chat(messages, tools=tools)

            call_kwargs = mock_create.call_args[1]
            # Tool deve ser mantida como esta
            assert call_kwargs["tools"] == tools
