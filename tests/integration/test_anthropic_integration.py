"""Testes de integração com Anthropic API."""

import pytest

from tests.integration.conftest import has_anthropic_key, integration_timeout


@pytest.mark.integration
@pytest.mark.anthropic
class TestAnthropicIntegrationChat:
    """Testes de chat com Anthropic API real."""

    @has_anthropic_key
    @integration_timeout
    @pytest.mark.asyncio
    async def test_anthropic_chat_basic(self, anthropic_api_key, anthropic_model):
        """Chat básico com Anthropic retorna resposta válida."""
        from forge_llm import Client

        client = Client(provider="anthropic", api_key=anthropic_api_key)
        response = await client.chat(
            "Responda apenas 'OK' sem mais nada.",
            model=anthropic_model,
            max_tokens=10,
        )

        assert response is not None
        assert response.content is not None
        assert len(response.content) > 0
        assert response.provider == "anthropic"
        assert "claude" in response.model.lower()

    @has_anthropic_key
    @integration_timeout
    @pytest.mark.asyncio
    async def test_anthropic_chat_with_system_message(
        self, anthropic_api_key, anthropic_model
    ):
        """Chat com system message funciona."""
        from forge_llm import Client
        from forge_llm.domain.value_objects import Message

        client = Client(provider="anthropic", api_key=anthropic_api_key)

        messages = [
            Message(role="system", content="Voce e um assistente que so responde OK."),
            Message(role="user", content="Ola"),
        ]

        response = await client.chat(
            messages,
            model=anthropic_model,
            max_tokens=10,
        )

        assert response is not None
        assert response.content is not None


@pytest.mark.integration
@pytest.mark.anthropic
@pytest.mark.streaming
class TestAnthropicIntegrationStreaming:
    """Testes de streaming com Anthropic API real."""

    @has_anthropic_key
    @integration_timeout
    @pytest.mark.asyncio
    async def test_anthropic_streaming_basic(self, anthropic_api_key, anthropic_model):
        """Streaming com Anthropic retorna chunks válidos."""
        from forge_llm import Client

        client = Client(provider="anthropic", api_key=anthropic_api_key)

        chunks = []
        async for chunk in client.chat_stream(
            "Diga apenas 'ola mundo'",
            model=anthropic_model,
            max_tokens=20,
        ):
            chunks.append(chunk)

        assert len(chunks) > 0
        # Verificar que algum chunk tem conteudo
        content_chunks = [c for c in chunks if c.get("delta", {}).get("content")]
        assert len(content_chunks) > 0


@pytest.mark.integration
@pytest.mark.anthropic
@pytest.mark.tokens
class TestAnthropicIntegrationTokens:
    """Testes de tokens com Anthropic API real."""

    @has_anthropic_key
    @integration_timeout
    @pytest.mark.asyncio
    async def test_anthropic_returns_token_usage(
        self, anthropic_api_key, anthropic_model
    ):
        """Anthropic retorna contagem de tokens."""
        from forge_llm import Client

        client = Client(provider="anthropic", api_key=anthropic_api_key)
        response = await client.chat(
            "Diga OK",
            model=anthropic_model,
            max_tokens=10,
        )

        assert response.usage is not None
        assert response.usage.prompt_tokens > 0
        assert response.usage.completion_tokens > 0
        assert response.usage.total_tokens == (
            response.usage.prompt_tokens + response.usage.completion_tokens
        )


@pytest.mark.integration
@pytest.mark.anthropic
@pytest.mark.tools
class TestAnthropicIntegrationTools:
    """Testes de tool calling com Anthropic API real."""

    @has_anthropic_key
    @integration_timeout
    @pytest.mark.asyncio
    async def test_anthropic_tool_calling(self, anthropic_api_key, anthropic_model):
        """Anthropic tool calling funciona corretamente."""
        from forge_llm import Client

        client = Client(provider="anthropic", api_key=anthropic_api_key)

        tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_weather",
                    "description": "Obter clima de uma cidade",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "city": {
                                "type": "string",
                                "description": "Nome da cidade",
                            },
                        },
                        "required": ["city"],
                    },
                },
            }
        ]

        response = await client.chat(
            "Qual o clima em Paris?",
            model=anthropic_model,
            tools=tools,
            max_tokens=100,
        )

        assert response is not None
        # Pode ter tool_calls ou resposta direta
        if response.has_tool_calls:
            assert len(response.tool_calls) > 0
            assert response.tool_calls[0].name == "get_weather"
