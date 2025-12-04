"""Testes para OpenAIProvider - usando Responses API."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest


class TestOpenAIProviderBasics:
    """Testes basicos para OpenAIProvider."""

    def test_openai_provider_implements_provider_port(self):
        """OpenAIProvider deve implementar ProviderPort."""
        from forge_llm.application.ports import ProviderPort
        from forge_llm.providers import OpenAIProvider

        assert issubclass(OpenAIProvider, ProviderPort)

    def test_openai_provider_creation_with_api_key(self):
        """OpenAIProvider deve aceitar api_key."""
        from forge_llm.providers import OpenAIProvider

        provider = OpenAIProvider(api_key="sk-test123")
        assert provider is not None

    def test_openai_provider_name(self):
        """OpenAIProvider deve ter provider_name = 'openai'."""
        from forge_llm.providers import OpenAIProvider

        provider = OpenAIProvider(api_key="sk-test123")
        assert provider.provider_name == "openai"

    def test_openai_provider_supports_streaming(self):
        """OpenAIProvider deve suportar streaming."""
        from forge_llm.providers import OpenAIProvider

        provider = OpenAIProvider(api_key="sk-test123")
        assert provider.supports_streaming is True

    def test_openai_provider_supports_tool_calling(self):
        """OpenAIProvider deve suportar tool calling."""
        from forge_llm.providers import OpenAIProvider

        provider = OpenAIProvider(api_key="sk-test123")
        assert provider.supports_tool_calling is True

    def test_openai_provider_default_model(self):
        """OpenAIProvider deve ter modelo padrao gpt-4o-mini."""
        from forge_llm.providers import OpenAIProvider

        provider = OpenAIProvider(api_key="sk-test123")
        assert provider.default_model == "gpt-4o-mini"

    def test_openai_provider_custom_model(self):
        """OpenAIProvider deve aceitar modelo customizado."""
        from forge_llm.providers import OpenAIProvider

        provider = OpenAIProvider(api_key="sk-test123", model="gpt-4")
        assert provider.default_model == "gpt-4"


def _create_mock_response(
    content: str = "Hello!",
    model: str = "gpt-4o-mini",
    tool_calls: list | None = None,
    status: str = "completed",
    input_tokens: int = 10,
    output_tokens: int = 5,
):
    """Helper para criar mock response da Responses API."""
    mock_response = MagicMock()
    mock_response.model = model
    mock_response.status = status

    # Criar output items
    output = []

    if content:
        # Criar message output item
        content_item = MagicMock()
        content_item.type = "output_text"
        content_item.text = content

        message_item = MagicMock()
        message_item.type = "message"
        message_item.content = [content_item]
        output.append(message_item)

    if tool_calls:
        for tc in tool_calls:
            tc_item = MagicMock()
            tc_item.type = "function_call"
            tc_item.call_id = tc.get("id", "call_123")
            tc_item.name = tc.get("name", "function")
            tc_item.arguments = tc.get("arguments", "{}")
            output.append(tc_item)

    mock_response.output = output

    # Usage
    mock_response.usage = MagicMock()
    mock_response.usage.input_tokens = input_tokens
    mock_response.usage.output_tokens = output_tokens

    return mock_response


class TestOpenAIProviderChat:
    """Testes para OpenAIProvider.chat usando Responses API."""

    @pytest.mark.asyncio
    async def test_openai_provider_chat_returns_response(self):
        """OpenAIProvider.chat deve retornar ChatResponse."""
        from forge_llm.domain.entities import ChatResponse
        from forge_llm.domain.value_objects import Message
        from forge_llm.providers import OpenAIProvider

        mock_response = _create_mock_response(content="Hello!")

        with patch(
            "forge_llm.providers.openai_provider.AsyncOpenAI"
        ) as mock_openai_class:
            mock_client = MagicMock()
            mock_client.responses.create = AsyncMock(return_value=mock_response)
            mock_openai_class.return_value = mock_client

            provider = OpenAIProvider(api_key="sk-test123")
            messages = [Message(role="user", content="Hi")]
            response = await provider.chat(messages)

            assert isinstance(response, ChatResponse)
            assert response.content == "Hello!"
            assert response.provider == "openai"

    @pytest.mark.asyncio
    async def test_openai_provider_chat_converts_messages(self):
        """OpenAIProvider deve converter Message para formato Responses API."""
        from forge_llm.domain.value_objects import Message
        from forge_llm.providers import OpenAIProvider

        mock_response = _create_mock_response(content="Response")

        with patch(
            "forge_llm.providers.openai_provider.AsyncOpenAI"
        ) as mock_openai_class:
            mock_client = MagicMock()
            mock_create = AsyncMock(return_value=mock_response)
            mock_client.responses.create = mock_create
            mock_openai_class.return_value = mock_client

            provider = OpenAIProvider(api_key="sk-test123")

            messages = [
                Message(role="system", content="You are helpful"),
                Message(role="user", content="Hello"),
            ]
            await provider.chat(messages)

            mock_create.assert_called_once()
            call_kwargs = mock_create.call_args[1]

            # System message vai para instructions
            assert call_kwargs["instructions"] == "You are helpful"

            # User message vai para input
            assert call_kwargs["input"] == [
                {"type": "message", "role": "user", "content": "Hello"},
            ]

    @pytest.mark.asyncio
    async def test_openai_provider_chat_converts_assistant_messages(self):
        """OpenAIProvider deve converter mensagens de assistant corretamente."""
        from forge_llm.domain.value_objects import Message
        from forge_llm.providers import OpenAIProvider

        mock_response = _create_mock_response(content="Response")

        with patch(
            "forge_llm.providers.openai_provider.AsyncOpenAI"
        ) as mock_openai_class:
            mock_client = MagicMock()
            mock_create = AsyncMock(return_value=mock_response)
            mock_client.responses.create = mock_create
            mock_openai_class.return_value = mock_client

            provider = OpenAIProvider(api_key="sk-test123")

            messages = [
                Message(role="user", content="Hello"),
                Message(role="assistant", content="Hi there!"),
                Message(role="user", content="How are you?"),
            ]
            await provider.chat(messages)

            mock_create.assert_called_once()
            call_kwargs = mock_create.call_args[1]

            # Assistant message deve ser convertido corretamente
            assert call_kwargs["input"] == [
                {"type": "message", "role": "user", "content": "Hello"},
                {"type": "message", "role": "assistant", "content": "Hi there!"},
                {"type": "message", "role": "user", "content": "How are you?"},
            ]

    @pytest.mark.asyncio
    async def test_openai_provider_chat_converts_tool_messages(self):
        """OpenAIProvider deve converter mensagens de tool corretamente."""
        from forge_llm.domain.value_objects import Message
        from forge_llm.providers import OpenAIProvider

        mock_response = _create_mock_response(content="The weather is sunny.")

        with patch(
            "forge_llm.providers.openai_provider.AsyncOpenAI"
        ) as mock_openai_class:
            mock_client = MagicMock()
            mock_create = AsyncMock(return_value=mock_response)
            mock_client.responses.create = mock_create
            mock_openai_class.return_value = mock_client

            provider = OpenAIProvider(api_key="sk-test123")

            messages = [
                Message(role="user", content="What's the weather?"),
                Message(
                    role="tool",
                    content='{"temp": 25, "condition": "sunny"}',
                    tool_call_id="call_123",
                ),
            ]
            await provider.chat(messages)

            mock_create.assert_called_once()
            call_kwargs = mock_create.call_args[1]

            # Tool message deve ser convertido para function_call_output
            assert call_kwargs["input"] == [
                {"type": "message", "role": "user", "content": "What's the weather?"},
                {
                    "type": "function_call_output",
                    "call_id": "call_123",
                    "output": '{"temp": 25, "condition": "sunny"}',
                },
            ]

    @pytest.mark.asyncio
    async def test_openai_provider_chat_uses_provided_model(self):
        """OpenAIProvider deve usar modelo fornecido."""
        from forge_llm.domain.value_objects import Message
        from forge_llm.providers import OpenAIProvider

        mock_response = _create_mock_response(content="Response", model="gpt-4")

        with patch(
            "forge_llm.providers.openai_provider.AsyncOpenAI"
        ) as mock_openai_class:
            mock_client = MagicMock()
            mock_create = AsyncMock(return_value=mock_response)
            mock_client.responses.create = mock_create
            mock_openai_class.return_value = mock_client

            provider = OpenAIProvider(api_key="sk-test123")
            messages = [Message(role="user", content="Hi")]
            response = await provider.chat(messages, model="gpt-4")

            assert response.model == "gpt-4"
            call_kwargs = mock_create.call_args[1]
            assert call_kwargs["model"] == "gpt-4"

    @pytest.mark.asyncio
    async def test_openai_provider_chat_with_temperature(self):
        """OpenAIProvider deve passar temperature para API."""
        from forge_llm.domain.value_objects import Message
        from forge_llm.providers import OpenAIProvider

        mock_response = _create_mock_response(content="Response")

        with patch(
            "forge_llm.providers.openai_provider.AsyncOpenAI"
        ) as mock_openai_class:
            mock_client = MagicMock()
            mock_create = AsyncMock(return_value=mock_response)
            mock_client.responses.create = mock_create
            mock_openai_class.return_value = mock_client

            provider = OpenAIProvider(api_key="sk-test123")
            messages = [Message(role="user", content="Hi")]
            await provider.chat(messages, temperature=0.5)

            call_kwargs = mock_create.call_args[1]
            assert call_kwargs["temperature"] == 0.5

    @pytest.mark.asyncio
    async def test_openai_provider_chat_with_max_tokens(self):
        """OpenAIProvider deve passar max_output_tokens para API."""
        from forge_llm.domain.value_objects import Message
        from forge_llm.providers import OpenAIProvider

        mock_response = _create_mock_response(content="Response")

        with patch(
            "forge_llm.providers.openai_provider.AsyncOpenAI"
        ) as mock_openai_class:
            mock_client = MagicMock()
            mock_create = AsyncMock(return_value=mock_response)
            mock_client.responses.create = mock_create
            mock_openai_class.return_value = mock_client

            provider = OpenAIProvider(api_key="sk-test123")
            messages = [Message(role="user", content="Hi")]
            await provider.chat(messages, max_tokens=100)

            call_kwargs = mock_create.call_args[1]
            assert call_kwargs["max_output_tokens"] == 100

    @pytest.mark.asyncio
    async def test_openai_provider_chat_returns_usage(self):
        """OpenAIProvider deve retornar uso de tokens."""
        from forge_llm.domain.value_objects import Message
        from forge_llm.providers import OpenAIProvider

        mock_response = _create_mock_response(
            content="Response", input_tokens=10, output_tokens=5
        )

        with patch(
            "forge_llm.providers.openai_provider.AsyncOpenAI"
        ) as mock_openai_class:
            mock_client = MagicMock()
            mock_client.responses.create = AsyncMock(return_value=mock_response)
            mock_openai_class.return_value = mock_client

            provider = OpenAIProvider(api_key="sk-test123")
            messages = [Message(role="user", content="Hi")]
            response = await provider.chat(messages)

            assert response.usage.prompt_tokens == 10
            assert response.usage.completion_tokens == 5
            assert response.usage.total_tokens == 15


class TestOpenAIProviderToolCalling:
    """Testes para tool calling do OpenAIProvider."""

    @pytest.mark.asyncio
    async def test_openai_provider_chat_with_tool_call(self):
        """OpenAIProvider deve retornar tool_calls quando presente."""
        from forge_llm.domain.value_objects import Message
        from forge_llm.providers import OpenAIProvider

        mock_response = _create_mock_response(
            content="",
            tool_calls=[
                {
                    "id": "call_123",
                    "name": "get_weather",
                    "arguments": '{"location": "SP"}',
                }
            ],
        )

        with patch(
            "forge_llm.providers.openai_provider.AsyncOpenAI"
        ) as mock_openai_class:
            mock_client = MagicMock()
            mock_client.responses.create = AsyncMock(return_value=mock_response)
            mock_openai_class.return_value = mock_client

            provider = OpenAIProvider(api_key="sk-test123")
            messages = [Message(role="user", content="Weather in SP?")]
            response = await provider.chat(messages)

            assert response.has_tool_calls is True
            assert len(response.tool_calls) == 1
            assert response.tool_calls[0].name == "get_weather"
            assert response.tool_calls[0].id == "call_123"

    @pytest.mark.asyncio
    async def test_openai_provider_chat_passes_tools(self):
        """OpenAIProvider deve passar tools para API no formato Responses."""
        from forge_llm.domain.value_objects import Message
        from forge_llm.providers import OpenAIProvider

        mock_response = _create_mock_response(content="Response")

        with patch(
            "forge_llm.providers.openai_provider.AsyncOpenAI"
        ) as mock_openai_class:
            mock_client = MagicMock()
            mock_create = AsyncMock(return_value=mock_response)
            mock_client.responses.create = mock_create
            mock_openai_class.return_value = mock_client

            provider = OpenAIProvider(api_key="sk-test123")
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
            # Tools devem ser convertidas para formato Responses API
            assert call_kwargs["tools"] == [
                {
                    "type": "function",
                    "name": "get_weather",
                    "description": "Get weather",
                    "parameters": {"type": "object", "properties": {}},
                }
            ]


class TestOpenAIProviderStreaming:
    """Testes para streaming do OpenAIProvider."""

    @pytest.mark.asyncio
    async def test_openai_provider_stream_yields_chunks(self):
        """OpenAIProvider.chat_stream deve retornar chunks."""
        from forge_llm.domain.value_objects import Message
        from forge_llm.providers import OpenAIProvider

        # Simular chunks de streaming da Responses API
        async def mock_stream():
            events = [
                MagicMock(type="response.output_text.delta", delta="Hello"),
                MagicMock(type="response.output_text.delta", delta=" world"),
                MagicMock(type="response.output_text.delta", delta="!"),
                MagicMock(type="response.completed"),
            ]
            for event in events:
                yield event

        with patch(
            "forge_llm.providers.openai_provider.AsyncOpenAI"
        ) as mock_openai_class:
            mock_client = MagicMock()
            mock_client.responses.create = AsyncMock(return_value=mock_stream())
            mock_openai_class.return_value = mock_client

            provider = OpenAIProvider(api_key="sk-test123")
            messages = [Message(role="user", content="Hi")]
            chunks = []
            async for chunk in provider.chat_stream(messages):
                chunks.append(chunk)

            assert len(chunks) == 4
            assert chunks[0]["delta"]["content"] == "Hello"
            assert chunks[-1]["finish_reason"] == "stop"


class TestOpenAIProviderErrors:
    """Testes de erro para OpenAIProvider."""

    @pytest.mark.asyncio
    async def test_openai_provider_authentication_error(self):
        """OpenAIProvider deve lancar AuthenticationError para API key invalida."""
        from openai import AuthenticationError as OpenAIAuthError

        from forge_llm.domain.exceptions import AuthenticationError
        from forge_llm.domain.value_objects import Message
        from forge_llm.providers import OpenAIProvider

        with patch(
            "forge_llm.providers.openai_provider.AsyncOpenAI"
        ) as mock_openai_class:
            mock_client = MagicMock()
            mock_client.responses.create = AsyncMock(
                side_effect=OpenAIAuthError(
                    message="Invalid API key",
                    response=MagicMock(status_code=401),
                    body=None,
                )
            )
            mock_openai_class.return_value = mock_client

            provider = OpenAIProvider(api_key="sk-invalid")
            messages = [Message(role="user", content="Hi")]

            with pytest.raises(AuthenticationError) as exc_info:
                await provider.chat(messages)

            assert (
                "authentication" in str(exc_info.value).lower()
                or "api_key" in str(exc_info.value).lower()
            )
            assert exc_info.value.provider == "openai"

    @pytest.mark.asyncio
    async def test_openai_provider_rate_limit_error(self):
        """OpenAIProvider deve lancar RateLimitError."""
        from openai import RateLimitError as OpenAIRateLimitError

        from forge_llm.domain.exceptions import RateLimitError
        from forge_llm.domain.value_objects import Message
        from forge_llm.providers import OpenAIProvider

        with patch(
            "forge_llm.providers.openai_provider.AsyncOpenAI"
        ) as mock_openai_class:
            mock_client = MagicMock()
            mock_client.responses.create = AsyncMock(
                side_effect=OpenAIRateLimitError(
                    message="Rate limit exceeded",
                    response=MagicMock(status_code=429),
                    body=None,
                )
            )
            mock_openai_class.return_value = mock_client

            provider = OpenAIProvider(api_key="sk-test123")
            messages = [Message(role="user", content="Hi")]

            with pytest.raises(RateLimitError) as exc_info:
                await provider.chat(messages)

            assert exc_info.value.provider == "openai"


class TestOpenAIProviderResponsesAPI:
    """Testes especificos para verificar uso da Responses API."""

    @pytest.mark.asyncio
    async def test_openai_provider_uses_responses_api_not_chat_completions(self):
        """OpenAIProvider DEVE usar responses.create, NAO chat.completions.create."""
        from forge_llm.domain.value_objects import Message
        from forge_llm.providers import OpenAIProvider

        mock_response = _create_mock_response(content="Response")

        with patch(
            "forge_llm.providers.openai_provider.AsyncOpenAI"
        ) as mock_openai_class:
            mock_client = MagicMock()
            mock_client.responses.create = AsyncMock(return_value=mock_response)
            mock_client.chat.completions.create = AsyncMock()
            mock_openai_class.return_value = mock_client

            provider = OpenAIProvider(api_key="sk-test123")
            messages = [Message(role="user", content="Hi")]
            await provider.chat(messages)

            # DEVE chamar responses.create
            mock_client.responses.create.assert_called_once()

            # NAO deve chamar chat.completions.create
            mock_client.chat.completions.create.assert_not_called()

    @pytest.mark.asyncio
    async def test_openai_provider_stream_uses_responses_api(self):
        """OpenAIProvider.chat_stream DEVE usar responses.create com stream=True."""
        from forge_llm.domain.value_objects import Message
        from forge_llm.providers import OpenAIProvider

        async def mock_stream():
            yield MagicMock(type="response.completed")

        with patch(
            "forge_llm.providers.openai_provider.AsyncOpenAI"
        ) as mock_openai_class:
            mock_client = MagicMock()
            mock_client.responses.create = AsyncMock(return_value=mock_stream())
            mock_client.chat.completions.create = AsyncMock()
            mock_openai_class.return_value = mock_client

            provider = OpenAIProvider(api_key="sk-test123")
            messages = [Message(role="user", content="Hi")]

            async for _ in provider.chat_stream(messages):
                pass

            # Verificar que responses.create foi chamado com stream=True
            mock_client.responses.create.assert_called_once()
            call_kwargs = mock_client.responses.create.call_args[1]
            assert call_kwargs["stream"] is True

            # NAO deve chamar chat.completions.create
            mock_client.chat.completions.create.assert_not_called()


class TestOpenAIProviderStreamingAdvanced:
    """Testes avancados para streaming do OpenAIProvider."""

    @pytest.mark.asyncio
    async def test_openai_stream_with_system_message(self):
        """OpenAIProvider.chat_stream deve passar instructions."""
        from forge_llm.domain.value_objects import Message
        from forge_llm.providers import OpenAIProvider

        async def mock_stream():
            yield MagicMock(type="response.completed")

        with patch(
            "forge_llm.providers.openai_provider.AsyncOpenAI"
        ) as mock_openai_class:
            mock_client = MagicMock()
            mock_client.responses.create = AsyncMock(return_value=mock_stream())
            mock_openai_class.return_value = mock_client

            provider = OpenAIProvider(api_key="sk-test123")
            messages = [
                Message(role="system", content="Be helpful"),
                Message(role="user", content="Hi"),
            ]

            async for _ in provider.chat_stream(messages):
                pass

            call_kwargs = mock_client.responses.create.call_args[1]
            assert call_kwargs["instructions"] == "Be helpful"

    @pytest.mark.asyncio
    async def test_openai_stream_with_tools(self):
        """OpenAIProvider.chat_stream deve passar tools."""
        from forge_llm.domain.value_objects import Message
        from forge_llm.providers import OpenAIProvider

        async def mock_stream():
            yield MagicMock(type="response.completed")

        with patch(
            "forge_llm.providers.openai_provider.AsyncOpenAI"
        ) as mock_openai_class:
            mock_client = MagicMock()
            mock_client.responses.create = AsyncMock(return_value=mock_stream())
            mock_openai_class.return_value = mock_client

            provider = OpenAIProvider(api_key="sk-test123")
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

            call_kwargs = mock_client.responses.create.call_args[1]
            assert call_kwargs["tools"] is not None

    @pytest.mark.asyncio
    async def test_openai_stream_authentication_error(self):
        """OpenAIProvider.chat_stream deve lancar AuthenticationError."""
        from openai import AuthenticationError as OpenAIAuthError

        from forge_llm.domain.exceptions import AuthenticationError
        from forge_llm.domain.value_objects import Message
        from forge_llm.providers import OpenAIProvider

        async def mock_stream(**kwargs):
            raise OpenAIAuthError(
                message="Invalid API key",
                response=MagicMock(status_code=401),
                body=None,
            )

        with patch(
            "forge_llm.providers.openai_provider.AsyncOpenAI"
        ) as mock_openai_class:
            mock_client = MagicMock()
            mock_client.responses.create = AsyncMock(side_effect=mock_stream)
            mock_openai_class.return_value = mock_client

            provider = OpenAIProvider(api_key="sk-invalid")
            messages = [Message(role="user", content="Hi")]

            with pytest.raises(AuthenticationError) as exc_info:
                async for _ in provider.chat_stream(messages):
                    pass

            assert exc_info.value.provider == "openai"

    @pytest.mark.asyncio
    async def test_openai_stream_rate_limit_error(self):
        """OpenAIProvider.chat_stream deve lancar RateLimitError."""
        from openai import RateLimitError as OpenAIRateLimitError

        from forge_llm.domain.exceptions import RateLimitError
        from forge_llm.domain.value_objects import Message
        from forge_llm.providers import OpenAIProvider

        async def mock_stream(**kwargs):
            raise OpenAIRateLimitError(
                message="Rate limit exceeded",
                response=MagicMock(status_code=429),
                body=None,
            )

        with patch(
            "forge_llm.providers.openai_provider.AsyncOpenAI"
        ) as mock_openai_class:
            mock_client = MagicMock()
            mock_client.responses.create = AsyncMock(side_effect=mock_stream)
            mock_openai_class.return_value = mock_client

            provider = OpenAIProvider(api_key="sk-test123")
            messages = [Message(role="user", content="Hi")]

            with pytest.raises(RateLimitError) as exc_info:
                async for _ in provider.chat_stream(messages):
                    pass

            assert exc_info.value.provider == "openai"


class TestOpenAIProviderToolConversion:
    """Testes para conversao de tools."""

    @pytest.mark.asyncio
    async def test_openai_tools_non_function_type_preserved(self):
        """OpenAIProvider deve preservar tools sem type=function."""
        from forge_llm.domain.value_objects import Message
        from forge_llm.providers import OpenAIProvider

        mock_response = _create_mock_response(content="Response")

        with patch(
            "forge_llm.providers.openai_provider.AsyncOpenAI"
        ) as mock_openai_class:
            mock_client = MagicMock()
            mock_create = AsyncMock(return_value=mock_response)
            mock_client.responses.create = mock_create
            mock_openai_class.return_value = mock_client

            provider = OpenAIProvider(api_key="sk-test123")
            messages = [Message(role="user", content="Hi")]
            # Tool sem type=function (formato nativo)
            tools = [
                {
                    "type": "code_interpreter",
                    "name": "code_tool",
                }
            ]
            await provider.chat(messages, tools=tools)

            call_kwargs = mock_create.call_args[1]
            # Tool deve ser mantida como esta
            assert call_kwargs["tools"] == tools
