"""Testes para MockAltProvider."""

import pytest

from forge_llm.domain.value_objects import Message


class TestMockAltProviderBasics:
    """Testes basicos para MockAltProvider."""

    def test_mock_alt_provider_implements_provider_port(self):
        """MockAltProvider deve implementar ProviderPort."""
        from forge_llm.application.ports import ProviderPort
        from forge_llm.providers import MockAltProvider

        assert issubclass(MockAltProvider, ProviderPort)

    def test_mock_alt_provider_creation(self):
        """MockAltProvider deve ser criado sem argumentos."""
        from forge_llm.providers import MockAltProvider

        provider = MockAltProvider()
        assert provider is not None

    def test_mock_alt_provider_name(self):
        """MockAltProvider deve ter provider_name = 'mock-alt'."""
        from forge_llm.providers import MockAltProvider

        provider = MockAltProvider()
        assert provider.provider_name == "mock-alt"

    def test_mock_alt_provider_supports_streaming(self):
        """MockAltProvider deve suportar streaming."""
        from forge_llm.providers import MockAltProvider

        provider = MockAltProvider()
        assert provider.supports_streaming is True

    def test_mock_alt_provider_supports_tool_calling(self):
        """MockAltProvider deve suportar tool calling."""
        from forge_llm.providers import MockAltProvider

        provider = MockAltProvider()
        assert provider.supports_tool_calling is True

    def test_mock_alt_provider_default_model(self):
        """MockAltProvider deve ter modelo padrao."""
        from forge_llm.providers import MockAltProvider

        provider = MockAltProvider()
        assert provider.default_model == "mock-alt-model"


class TestMockAltProviderChat:
    """Testes de chat para MockAltProvider."""

    @pytest.mark.asyncio
    async def test_mock_alt_provider_chat_returns_response(self):
        """MockAltProvider.chat deve retornar ChatResponse."""
        from forge_llm.domain.entities import ChatResponse
        from forge_llm.providers import MockAltProvider

        provider = MockAltProvider()
        messages = [Message(role="user", content="Hello")]
        response = await provider.chat(messages)

        assert isinstance(response, ChatResponse)
        assert response.content == "Mock Alt response"

    @pytest.mark.asyncio
    async def test_mock_alt_provider_chat_has_tokens(self):
        """MockAltProvider.chat deve retornar tokens."""
        from forge_llm.providers import MockAltProvider

        provider = MockAltProvider()
        messages = [Message(role="user", content="Hello")]
        response = await provider.chat(messages)

        assert response.usage.prompt_tokens == 15
        assert response.usage.completion_tokens == 25
        assert response.usage.total_tokens == 40

    @pytest.mark.asyncio
    async def test_mock_alt_provider_chat_custom_response(self):
        """MockAltProvider deve aceitar resposta customizada."""
        from forge_llm.providers import MockAltProvider

        provider = MockAltProvider(default_response="Custom alt response")
        messages = [Message(role="user", content="Hello")]
        response = await provider.chat(messages)

        assert response.content == "Custom alt response"


class TestMockAltProviderStream:
    """Testes de streaming para MockAltProvider."""

    @pytest.mark.asyncio
    async def test_mock_alt_provider_stream_returns_chunks(self):
        """MockAltProvider.chat_stream deve retornar chunks."""
        from forge_llm.providers import MockAltProvider

        provider = MockAltProvider(default_response="Hello world")
        messages = [Message(role="user", content="Hello")]

        chunks = []
        async for chunk in provider.chat_stream(messages):
            chunks.append(chunk)

        assert len(chunks) == 2  # "Hello" and "world"
        assert chunks[0]["delta"]["content"] == "Hello "
        assert chunks[1]["delta"]["content"] == "world"

    @pytest.mark.asyncio
    async def test_mock_alt_provider_stream_has_index(self):
        """MockAltProvider.chat_stream deve ter index em cada chunk."""
        from forge_llm.providers import MockAltProvider

        provider = MockAltProvider(default_response="One two three")
        messages = [Message(role="user", content="Hello")]

        chunks = []
        async for chunk in provider.chat_stream(messages):
            chunks.append(chunk)

        for i, chunk in enumerate(chunks):
            assert chunk["index"] == i

    @pytest.mark.asyncio
    async def test_mock_alt_provider_stream_finish_reason(self):
        """MockAltProvider.chat_stream deve ter finish_reason no ultimo chunk."""
        from forge_llm.providers import MockAltProvider

        provider = MockAltProvider(default_response="Test")
        messages = [Message(role="user", content="Hello")]

        chunks = []
        async for chunk in provider.chat_stream(messages):
            chunks.append(chunk)

        assert chunks[-1]["finish_reason"] == "stop"
        # Outros chunks nao tem finish_reason
        for chunk in chunks[:-1]:
            assert chunk.get("finish_reason") is None
