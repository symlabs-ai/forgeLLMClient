"""Testes para MockNoTokensProvider."""

import pytest

from forge_llm.domain.value_objects import Message


class TestMockNoTokensProviderBasics:
    """Testes basicos para MockNoTokensProvider."""

    def test_mock_no_tokens_provider_implements_provider_port(self):
        """MockNoTokensProvider deve implementar ProviderPort."""
        from forge_llm.application.ports import ProviderPort
        from forge_llm.providers import MockNoTokensProvider

        assert issubclass(MockNoTokensProvider, ProviderPort)

    def test_mock_no_tokens_provider_creation(self):
        """MockNoTokensProvider deve ser criado sem argumentos."""
        from forge_llm.providers import MockNoTokensProvider

        provider = MockNoTokensProvider()
        assert provider is not None

    def test_mock_no_tokens_provider_name(self):
        """MockNoTokensProvider deve ter provider_name = 'mock-no-tokens'."""
        from forge_llm.providers import MockNoTokensProvider

        provider = MockNoTokensProvider()
        assert provider.provider_name == "mock-no-tokens"

    def test_mock_no_tokens_provider_supports_streaming(self):
        """MockNoTokensProvider deve suportar streaming."""
        from forge_llm.providers import MockNoTokensProvider

        provider = MockNoTokensProvider()
        assert provider.supports_streaming is True

    def test_mock_no_tokens_provider_not_supports_tool_calling(self):
        """MockNoTokensProvider nao deve suportar tool calling."""
        from forge_llm.providers import MockNoTokensProvider

        provider = MockNoTokensProvider()
        assert provider.supports_tool_calling is False

    def test_mock_no_tokens_provider_default_model(self):
        """MockNoTokensProvider deve ter modelo padrao."""
        from forge_llm.providers import MockNoTokensProvider

        provider = MockNoTokensProvider()
        assert provider.default_model == "mock-no-tokens-model"


class TestMockNoTokensProviderChat:
    """Testes de chat para MockNoTokensProvider."""

    @pytest.mark.asyncio
    async def test_mock_no_tokens_provider_chat_returns_response(self):
        """MockNoTokensProvider.chat deve retornar ChatResponse."""
        from forge_llm.domain.entities import ChatResponse
        from forge_llm.providers import MockNoTokensProvider

        provider = MockNoTokensProvider()
        messages = [Message(role="user", content="Hello")]
        response = await provider.chat(messages)

        assert isinstance(response, ChatResponse)
        assert response.content == "Mock response"

    @pytest.mark.asyncio
    async def test_mock_no_tokens_provider_chat_zero_tokens(self):
        """MockNoTokensProvider.chat deve retornar tokens zerados."""
        from forge_llm.providers import MockNoTokensProvider

        provider = MockNoTokensProvider()
        messages = [Message(role="user", content="Hello")]
        response = await provider.chat(messages)

        assert response.usage.prompt_tokens == 0
        assert response.usage.completion_tokens == 0
        assert response.usage.total_tokens == 0

    @pytest.mark.asyncio
    async def test_mock_no_tokens_provider_chat_custom_response(self):
        """MockNoTokensProvider deve aceitar resposta customizada."""
        from forge_llm.providers import MockNoTokensProvider

        provider = MockNoTokensProvider(default_response="Custom response")
        messages = [Message(role="user", content="Hello")]
        response = await provider.chat(messages)

        assert response.content == "Custom response"


class TestMockNoTokensProviderStream:
    """Testes de streaming para MockNoTokensProvider."""

    @pytest.mark.asyncio
    async def test_mock_no_tokens_provider_stream_returns_chunks(self):
        """MockNoTokensProvider.chat_stream deve retornar chunks."""
        from forge_llm.providers import MockNoTokensProvider

        provider = MockNoTokensProvider(default_response="Hello world")
        messages = [Message(role="user", content="Hello")]

        chunks = []
        async for chunk in provider.chat_stream(messages):
            chunks.append(chunk)

        assert len(chunks) == 2  # "Hello" and "world"
        assert chunks[0]["delta"]["content"] == "Hello "
        assert chunks[1]["delta"]["content"] == "world"

    @pytest.mark.asyncio
    async def test_mock_no_tokens_provider_stream_finish_reason(self):
        """MockNoTokensProvider.chat_stream deve ter finish_reason no ultimo chunk."""
        from forge_llm.providers import MockNoTokensProvider

        provider = MockNoTokensProvider(default_response="Test")
        messages = [Message(role="user", content="Hello")]

        chunks = []
        async for chunk in provider.chat_stream(messages):
            chunks.append(chunk)

        assert chunks[-1]["finish_reason"] == "stop"
