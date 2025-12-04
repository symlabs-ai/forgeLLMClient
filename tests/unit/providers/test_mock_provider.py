"""Testes para MockProvider - TDD RED phase."""

import pytest


class TestMockProvider:
    """Testes para MockProvider."""

    def test_mock_provider_implements_provider_port(self):
        """MockProvider deve implementar ProviderPort."""
        from forge_llm.application.ports import ProviderPort
        from forge_llm.providers import MockProvider

        assert issubclass(MockProvider, ProviderPort)

    def test_mock_provider_creation(self):
        """MockProvider deve aceitar configuracao."""
        from forge_llm.providers import MockProvider

        provider = MockProvider()
        assert provider is not None

    def test_mock_provider_name(self):
        """MockProvider deve ter provider_name = 'mock'."""
        from forge_llm.providers import MockProvider

        provider = MockProvider()
        assert provider.provider_name == "mock"

    def test_mock_provider_supports_streaming(self):
        """MockProvider deve suportar streaming."""
        from forge_llm.providers import MockProvider

        provider = MockProvider()
        assert provider.supports_streaming is True

    def test_mock_provider_supports_tool_calling(self):
        """MockProvider deve suportar tool calling."""
        from forge_llm.providers import MockProvider

        provider = MockProvider()
        assert provider.supports_tool_calling is True

    def test_mock_provider_default_model(self):
        """MockProvider deve ter modelo padrao."""
        from forge_llm.providers import MockProvider

        provider = MockProvider()
        assert provider.default_model == "mock-model"

    def test_mock_provider_custom_default_response(self):
        """MockProvider deve aceitar resposta padrao customizada."""
        from forge_llm.providers import MockProvider

        provider = MockProvider(default_response="Custom response")
        assert provider._default_response == "Custom response"

    @pytest.mark.asyncio
    async def test_mock_provider_chat_returns_response(self):
        """MockProvider.chat deve retornar ChatResponse."""
        from forge_llm.domain.entities import ChatResponse
        from forge_llm.domain.value_objects import Message
        from forge_llm.providers import MockProvider

        provider = MockProvider(default_response="Ola!")
        messages = [Message(role="user", content="Oi")]

        response = await provider.chat(messages)

        assert isinstance(response, ChatResponse)
        assert response.content == "Ola!"
        assert response.provider == "mock"

    @pytest.mark.asyncio
    async def test_mock_provider_chat_uses_set_response(self):
        """MockProvider deve usar resposta configurada via set_response."""
        from forge_llm.domain.value_objects import Message
        from forge_llm.providers import MockProvider

        provider = MockProvider()
        provider.set_response("Resposta especifica")
        messages = [Message(role="user", content="Oi")]

        response = await provider.chat(messages)

        assert response.content == "Resposta especifica"

    @pytest.mark.asyncio
    async def test_mock_provider_chat_multiple_responses(self):
        """MockProvider deve usar respostas em sequencia."""
        from forge_llm.domain.value_objects import Message
        from forge_llm.providers import MockProvider

        provider = MockProvider()
        provider.set_responses(["Primeira", "Segunda", "Terceira"])
        messages = [Message(role="user", content="Oi")]

        r1 = await provider.chat(messages)
        r2 = await provider.chat(messages)
        r3 = await provider.chat(messages)

        assert r1.content == "Primeira"
        assert r2.content == "Segunda"
        assert r3.content == "Terceira"

    @pytest.mark.asyncio
    async def test_mock_provider_tracks_call_count(self):
        """MockProvider deve rastrear numero de chamadas."""
        from forge_llm.domain.value_objects import Message
        from forge_llm.providers import MockProvider

        provider = MockProvider()
        messages = [Message(role="user", content="Oi")]

        assert provider.call_count == 0
        await provider.chat(messages)
        assert provider.call_count == 1
        await provider.chat(messages)
        assert provider.call_count == 2

    @pytest.mark.asyncio
    async def test_mock_provider_chat_has_usage(self):
        """MockProvider.chat deve retornar uso de tokens."""
        from forge_llm.domain.value_objects import Message
        from forge_llm.providers import MockProvider

        provider = MockProvider()
        messages = [Message(role="user", content="Oi")]

        response = await provider.chat(messages)

        assert response.usage.prompt_tokens > 0
        assert response.usage.completion_tokens > 0

    @pytest.mark.asyncio
    async def test_mock_provider_chat_uses_provided_model(self):
        """MockProvider deve usar modelo fornecido."""
        from forge_llm.domain.value_objects import Message
        from forge_llm.providers import MockProvider

        provider = MockProvider()
        messages = [Message(role="user", content="Oi")]

        response = await provider.chat(messages, model="custom-model")

        assert response.model == "custom-model"

    @pytest.mark.asyncio
    async def test_mock_provider_stream_yields_chunks(self):
        """MockProvider.chat_stream deve retornar chunks."""
        from forge_llm.domain.value_objects import Message
        from forge_llm.providers import MockProvider

        provider = MockProvider(default_response="Hello world")
        messages = [Message(role="user", content="Oi")]

        chunks = []
        async for chunk in provider.chat_stream(messages):
            chunks.append(chunk)

        assert len(chunks) > 0
        # Ultimo chunk deve ter finish_reason
        assert chunks[-1].get("finish_reason") == "stop"

    @pytest.mark.asyncio
    async def test_mock_provider_stream_increments_call_count(self):
        """MockProvider.chat_stream deve incrementar call_count."""
        from forge_llm.domain.value_objects import Message
        from forge_llm.providers import MockProvider

        provider = MockProvider()
        messages = [Message(role="user", content="Oi")]

        assert provider.call_count == 0
        async for _ in provider.chat_stream(messages):
            pass
        assert provider.call_count == 1
