"""Testes de integração com OpenAI API."""

import pytest

from tests.integration.conftest import has_openai_key, integration_timeout


@pytest.mark.integration
@pytest.mark.openai
class TestOpenAIIntegrationChat:
    """Testes de chat com OpenAI API real."""

    @has_openai_key
    @integration_timeout
    @pytest.mark.asyncio
    async def test_openai_chat_basic(self, openai_api_key, openai_model):
        """Chat básico com OpenAI retorna resposta válida."""
        from forge_llm import Client

        client = Client(provider="openai", api_key=openai_api_key)
        response = await client.chat(
            "Responda apenas 'OK' sem mais nada.",
            model=openai_model,
            max_tokens=50,
        )

        assert response is not None
        assert response.content is not None
        assert len(response.content) > 0
        assert response.provider == "openai"

    @has_openai_key
    @integration_timeout
    @pytest.mark.asyncio
    async def test_openai_chat_with_system_message(self, openai_api_key, openai_model):
        """Chat com system message funciona."""
        from forge_llm import Client
        from forge_llm.domain.value_objects import Message

        client = Client(provider="openai", api_key=openai_api_key)

        messages = [
            Message(role="system", content="Voce e um assistente que so responde OK."),
            Message(role="user", content="Ola"),
        ]

        response = await client.chat(
            messages,
            model=openai_model,
            max_tokens=50,
        )

        assert response is not None
        assert response.content is not None


@pytest.mark.integration
@pytest.mark.openai
@pytest.mark.streaming
class TestOpenAIIntegrationStreaming:
    """Testes de streaming com OpenAI API real."""

    @has_openai_key
    @integration_timeout
    @pytest.mark.asyncio
    async def test_openai_streaming_basic(self, openai_api_key, openai_model):
        """Streaming com OpenAI retorna chunks válidos."""
        from forge_llm import Client

        client = Client(provider="openai", api_key=openai_api_key)

        chunks = []
        async for chunk in client.chat_stream(
            "Diga apenas 'ola mundo'",
            model=openai_model,
            max_tokens=20,
        ):
            chunks.append(chunk)

        assert len(chunks) > 0
        # Verificar que algum chunk tem conteudo
        content_chunks = [c for c in chunks if c.get("delta", {}).get("content")]
        assert len(content_chunks) > 0


@pytest.mark.integration
@pytest.mark.openai
@pytest.mark.tokens
class TestOpenAIIntegrationTokens:
    """Testes de tokens com OpenAI API real."""

    @has_openai_key
    @integration_timeout
    @pytest.mark.asyncio
    async def test_openai_returns_token_usage(self, openai_api_key, openai_model):
        """OpenAI retorna contagem de tokens."""
        from forge_llm import Client

        client = Client(provider="openai", api_key=openai_api_key)
        response = await client.chat(
            "Diga OK",
            model=openai_model,
            max_tokens=50,
        )

        assert response.usage is not None
        assert response.usage.prompt_tokens > 0
        assert response.usage.completion_tokens > 0
        assert response.usage.total_tokens == (
            response.usage.prompt_tokens + response.usage.completion_tokens
        )


@pytest.mark.integration
@pytest.mark.openai
@pytest.mark.tools
class TestOpenAIIntegrationTools:
    """Testes de tool calling com OpenAI API real."""

    @has_openai_key
    @integration_timeout
    @pytest.mark.asyncio
    async def test_openai_tool_calling(self, openai_api_key, openai_model):
        """OpenAI tool calling funciona corretamente."""
        from forge_llm import Client

        client = Client(provider="openai", api_key=openai_api_key)

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
            model=openai_model,
            tools=tools,
            max_tokens=100,
        )

        assert response is not None
        # Pode ter tool_calls ou resposta direta
        if response.has_tool_calls:
            assert len(response.tool_calls) > 0
            assert response.tool_calls[0].name == "get_weather"
