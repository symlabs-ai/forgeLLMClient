"""
Unit tests for AsyncChatAgent and async adapters.

Tests async chat() and stream_chat() with mocked providers.
"""
import json
from unittest.mock import AsyncMock, MagicMock

import pytest

from forge_llm.application.agents import AsyncChatAgent
from forge_llm.application.tools import ToolRegistry
from forge_llm.domain import InvalidMessageError, ProviderNotConfiguredError
from forge_llm.domain.entities import ProviderConfig


class TestAsyncChatAgentInit:
    """Tests for AsyncChatAgent initialization."""

    def test_init_with_provider_and_key(self):
        """Should initialize with provider and api_key."""
        agent = AsyncChatAgent(provider="openai", api_key="test-key")

        assert agent.provider_name == "openai"

    def test_init_with_model(self):
        """Should accept model parameter."""
        agent = AsyncChatAgent(provider="openai", api_key="test-key", model="gpt-4")

        assert agent._model == "gpt-4"

    def test_init_without_api_key(self):
        """Should initialize without api_key (may be env var)."""
        agent = AsyncChatAgent(provider="openai")

        assert agent.provider_name == "openai"


class TestAsyncChatAgentChat:
    """Tests for AsyncChatAgent.chat()."""

    @pytest.mark.asyncio
    async def test_chat_returns_response(self):
        """chat() should return ChatResponse."""
        mock_provider = AsyncMock()
        mock_provider.send.return_value = {
            "content": "Hello!",
            "role": "assistant",
            "model": "gpt-4",
            "provider": "openai",
            "usage": {"prompt_tokens": 5, "completion_tokens": 3, "total_tokens": 8},
        }

        agent = AsyncChatAgent(provider="openai", api_key="test-key")
        agent._provider = mock_provider

        response = await agent.chat("Hi")

        assert response.content == "Hello!"
        assert response.metadata.model == "gpt-4"

    @pytest.mark.asyncio
    async def test_chat_with_message_string(self):
        """chat() should accept string message."""
        mock_provider = AsyncMock()
        mock_provider.send.return_value = {
            "content": "Response",
            "role": "assistant",
            "model": "gpt-4",
            "provider": "openai",
            "usage": {},
        }

        agent = AsyncChatAgent(provider="openai", api_key="test-key")
        agent._provider = mock_provider

        await agent.chat("Hello world")

        call_args = mock_provider.send.call_args[0][0]
        assert call_args[0]["role"] == "user"
        assert call_args[0]["content"] == "Hello world"

    @pytest.mark.asyncio
    async def test_chat_raises_on_empty_message(self):
        """chat() should raise InvalidMessageError for empty message."""
        agent = AsyncChatAgent(provider="openai", api_key="test-key")

        with pytest.raises(InvalidMessageError):
            await agent.chat("")

    @pytest.mark.asyncio
    async def test_chat_raises_without_api_key(self):
        """chat() should raise ProviderNotConfiguredError without api_key."""
        agent = AsyncChatAgent(provider="openai")

        with pytest.raises(ProviderNotConfiguredError):
            await agent.chat("Hello")


class TestAsyncChatAgentStreamChat:
    """Tests for AsyncChatAgent.stream_chat()."""

    @pytest.mark.asyncio
    async def test_stream_chat_yields_chunks(self):
        """stream_chat() should yield ChatChunk objects."""
        mock_provider = AsyncMock()

        async def mock_stream(*args, **kwargs):
            yield {"content": "Hello", "provider": "openai"}
            yield {"content": " World", "provider": "openai"}
            yield {"content": "", "finish_reason": "stop", "provider": "openai"}

        mock_provider.stream = mock_stream

        agent = AsyncChatAgent(provider="openai", api_key="test-key")
        agent._provider = mock_provider

        chunks = []
        async for chunk in agent.stream_chat("Hi"):
            chunks.append(chunk)

        assert len(chunks) == 3
        assert chunks[0].content == "Hello"
        assert chunks[1].content == " World"
        assert chunks[2].finish_reason == "stop"

    @pytest.mark.asyncio
    async def test_stream_chat_with_tools(self):
        """stream_chat() should handle tool calls."""
        mock_provider = AsyncMock()

        tool_call_data = [
            {
                "id": "call_123",
                "type": "function",
                "function": {"name": "get_value", "arguments": json.dumps({"key": "test"})},
            }
        ]

        async def mock_stream_first_call(*args, **kwargs):
            yield {
                "content": "",
                "finish_reason": "tool_calls",
                "tool_calls": tool_call_data,
                "provider": "openai",
            }

        async def mock_stream_second_call(*args, **kwargs):
            yield {"content": "The value is 42", "provider": "openai"}
            yield {"content": "", "finish_reason": "stop", "provider": "openai"}

        call_count = [0]

        def mock_stream_side_effect(*args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                return mock_stream_first_call(*args, **kwargs)
            return mock_stream_second_call(*args, **kwargs)

        mock_provider.stream = mock_stream_side_effect

        registry = ToolRegistry()

        @registry.tool
        def get_value(key: str) -> str:
            """Get a value."""
            return "42"

        agent = AsyncChatAgent(provider="openai", api_key="test-key", tools=registry)
        agent._provider = mock_provider

        chunks = []
        async for chunk in agent.stream_chat("Get test value", auto_execute_tools=True):
            chunks.append(chunk)

        # Should have: tool_calls chunk, tool result chunk, final chunks
        tool_calls_chunk = next((c for c in chunks if c.finish_reason == "tool_calls"), None)
        assert tool_calls_chunk is not None

        tool_result_chunk = next((c for c in chunks if c.role == "tool"), None)
        assert tool_result_chunk is not None
        assert "42" in tool_result_chunk.content


class TestAsyncOpenAIAdapter:
    """Tests for AsyncOpenAIAdapter."""

    def test_adapter_name(self):
        """Should return 'openai' as name."""
        from forge_llm.infrastructure.providers import AsyncOpenAIAdapter

        config = ProviderConfig(provider="openai", api_key="test-key")
        adapter = AsyncOpenAIAdapter(config)

        assert adapter.name == "openai"

    def test_validate_without_key_raises(self):
        """validate() should raise without api_key."""
        from forge_llm.infrastructure.providers import AsyncOpenAIAdapter

        config = ProviderConfig(provider="openai")
        adapter = AsyncOpenAIAdapter(config)

        with pytest.raises(ProviderNotConfiguredError):
            adapter.validate()

    @pytest.mark.asyncio
    async def test_send_returns_response(self):
        """send() should return response dict."""
        from forge_llm.infrastructure.providers import AsyncOpenAIAdapter

        mock_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Hello!"
        mock_response.choices[0].message.role = "assistant"
        mock_response.model = "gpt-4"
        mock_response.usage.prompt_tokens = 5
        mock_response.usage.completion_tokens = 3
        mock_response.usage.total_tokens = 8
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

        config = ProviderConfig(provider="openai", api_key="test-key")
        adapter = AsyncOpenAIAdapter(config)
        adapter._client = mock_client

        result = await adapter.send([{"role": "user", "content": "Hi"}])

        assert result["content"] == "Hello!"
        assert result["role"] == "assistant"
        assert result["usage"]["total_tokens"] == 8


class TestAsyncAnthropicAdapter:
    """Tests for AsyncAnthropicAdapter."""

    def test_adapter_name(self):
        """Should return 'anthropic' as name."""
        from forge_llm.infrastructure.providers import AsyncAnthropicAdapter

        config = ProviderConfig(provider="anthropic", api_key="test-key")
        adapter = AsyncAnthropicAdapter(config)

        assert adapter.name == "anthropic"

    def test_validate_without_key_raises(self):
        """validate() should raise without api_key."""
        from forge_llm.infrastructure.providers import AsyncAnthropicAdapter

        config = ProviderConfig(provider="anthropic")
        adapter = AsyncAnthropicAdapter(config)

        with pytest.raises(ProviderNotConfiguredError):
            adapter.validate()

    @pytest.mark.asyncio
    async def test_send_returns_response(self):
        """send() should return response dict."""
        from forge_llm.infrastructure.providers import AsyncAnthropicAdapter

        mock_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.content = [MagicMock()]
        mock_response.content[0].text = "Hello!"
        mock_response.role = "assistant"
        mock_response.model = "claude-3-sonnet"
        mock_response.usage.input_tokens = 5
        mock_response.usage.output_tokens = 3
        mock_client.messages.create = AsyncMock(return_value=mock_response)

        config = ProviderConfig(provider="anthropic", api_key="test-key")
        adapter = AsyncAnthropicAdapter(config)
        adapter._client = mock_client

        result = await adapter.send([{"role": "user", "content": "Hi"}])

        assert result["content"] == "Hello!"
        assert result["role"] == "assistant"
        assert result["usage"]["total_tokens"] == 8


class TestAsyncOpenAIAdapterStream:
    """Tests for AsyncOpenAIAdapter.stream()."""

    @pytest.mark.asyncio
    async def test_stream_yields_content_chunks(self):
        """stream() should yield content chunks."""
        from forge_llm.infrastructure.providers import AsyncOpenAIAdapter

        mock_client = AsyncMock()

        # Create mock chunks
        chunk1 = MagicMock()
        chunk1.choices = [MagicMock()]
        chunk1.choices[0].delta.content = "Hello"
        chunk1.choices[0].delta.tool_calls = None
        chunk1.choices[0].finish_reason = None

        chunk2 = MagicMock()
        chunk2.choices = [MagicMock()]
        chunk2.choices[0].delta.content = " World"
        chunk2.choices[0].delta.tool_calls = None
        chunk2.choices[0].finish_reason = None

        chunk3 = MagicMock()
        chunk3.choices = [MagicMock()]
        chunk3.choices[0].delta.content = None
        chunk3.choices[0].delta.tool_calls = None
        chunk3.choices[0].finish_reason = "stop"

        async def mock_stream_iter():
            for chunk in [chunk1, chunk2, chunk3]:
                yield chunk

        mock_client.chat.completions.create = AsyncMock(return_value=mock_stream_iter())

        config = ProviderConfig(provider="openai", api_key="test-key")
        adapter = AsyncOpenAIAdapter(config)
        adapter._client = mock_client

        chunks = []
        async for chunk in adapter.stream([{"role": "user", "content": "Hi"}]):
            chunks.append(chunk)

        assert len(chunks) == 3
        assert chunks[0]["content"] == "Hello"
        assert chunks[1]["content"] == " World"
        assert chunks[2]["finish_reason"] == "stop"

    @pytest.mark.asyncio
    async def test_stream_handles_tool_calls(self):
        """stream() should handle tool call chunks."""
        from forge_llm.infrastructure.providers import AsyncOpenAIAdapter

        mock_client = AsyncMock()

        # Create mock tool call chunk
        tool_call_mock = MagicMock()
        tool_call_mock.index = 0
        tool_call_mock.id = "call_123"
        tool_call_mock.function.name = "get_weather"
        tool_call_mock.function.arguments = '{"loc": "NYC"}'

        chunk1 = MagicMock()
        chunk1.choices = [MagicMock()]
        chunk1.choices[0].delta.content = None
        chunk1.choices[0].delta.tool_calls = [tool_call_mock]
        chunk1.choices[0].finish_reason = None

        chunk2 = MagicMock()
        chunk2.choices = [MagicMock()]
        chunk2.choices[0].delta.content = None
        chunk2.choices[0].delta.tool_calls = None
        chunk2.choices[0].finish_reason = "tool_calls"

        async def mock_stream_iter():
            for chunk in [chunk1, chunk2]:
                yield chunk

        mock_client.chat.completions.create = AsyncMock(return_value=mock_stream_iter())

        config = ProviderConfig(provider="openai", api_key="test-key")
        adapter = AsyncOpenAIAdapter(config)
        adapter._client = mock_client

        chunks = []
        async for chunk in adapter.stream(
            [{"role": "user", "content": "Weather?"}],
            config={"tools": [{"type": "function", "function": {"name": "get_weather"}}]},
        ):
            chunks.append(chunk)

        # Should have tool_calls in final chunk
        tool_chunk = next((c for c in chunks if c.get("finish_reason") == "tool_calls"), None)
        assert tool_chunk is not None
        assert "tool_calls" in tool_chunk


class TestAsyncAnthropicAdapterStream:
    """Tests for AsyncAnthropicAdapter.stream()."""

    @pytest.mark.asyncio
    async def test_stream_yields_content_chunks(self):
        """stream() should yield content chunks."""
        from forge_llm.infrastructure.providers import AsyncAnthropicAdapter

        mock_client = AsyncMock()

        # Create mock events
        event1 = MagicMock()
        event1.type = "content_block_delta"
        event1.delta.text = "Hello"

        event2 = MagicMock()
        event2.type = "content_block_delta"
        event2.delta.text = " World"

        event3 = MagicMock()
        event3.type = "message_stop"

        class MockStream:
            async def __aenter__(self):
                return self

            async def __aexit__(self, *args):
                pass

            def __aiter__(self):
                return self

            async def __anext__(self):
                if not hasattr(self, "_events"):
                    self._events = iter([event1, event2, event3])
                try:
                    return next(self._events)
                except StopIteration:
                    raise StopAsyncIteration from None

        mock_client.messages.stream = MagicMock(return_value=MockStream())

        config = ProviderConfig(provider="anthropic", api_key="test-key")
        adapter = AsyncAnthropicAdapter(config)
        adapter._client = mock_client

        chunks = []
        async for chunk in adapter.stream([{"role": "user", "content": "Hi"}]):
            chunks.append(chunk)

        assert len(chunks) >= 2
        content_chunks = [c for c in chunks if c.get("content")]
        assert any("Hello" in c["content"] for c in content_chunks)

    @pytest.mark.asyncio
    async def test_stream_handles_tool_use(self):
        """stream() should handle tool use events."""
        from forge_llm.infrastructure.providers import AsyncAnthropicAdapter

        mock_client = AsyncMock()

        # Create mock events for tool use
        event1 = MagicMock()
        event1.type = "content_block_start"
        event1.content_block.type = "tool_use"
        event1.content_block.id = "tool_123"
        event1.content_block.name = "get_weather"

        event2 = MagicMock()
        event2.type = "content_block_delta"
        event2.delta.partial_json = '{"location": "NYC"}'
        delattr(event2.delta, "text")  # Remove text attribute

        event3 = MagicMock()
        event3.type = "content_block_stop"

        event4 = MagicMock()
        event4.type = "message_stop"

        class MockStream:
            async def __aenter__(self):
                return self

            async def __aexit__(self, *args):
                pass

            def __aiter__(self):
                return self

            async def __anext__(self):
                if not hasattr(self, "_events"):
                    self._events = iter([event1, event2, event3, event4])
                try:
                    return next(self._events)
                except StopIteration:
                    raise StopAsyncIteration from None

        mock_client.messages.stream = MagicMock(return_value=MockStream())

        config = ProviderConfig(provider="anthropic", api_key="test-key")
        adapter = AsyncAnthropicAdapter(config)
        adapter._client = mock_client

        chunks = []
        async for chunk in adapter.stream(
            [{"role": "user", "content": "Weather?"}],
            config={"tools": [{"type": "function", "function": {"name": "get_weather"}}]},
        ):
            chunks.append(chunk)

        # Should have tool_calls in final chunk
        tool_chunk = next((c for c in chunks if c.get("finish_reason") == "tool_calls"), None)
        assert tool_chunk is not None


class TestAsyncProviderPort:
    """Tests for IAsyncLLMProviderPort protocol."""

    def test_protocol_is_runtime_checkable(self):
        """IAsyncLLMProviderPort should be runtime checkable."""
        from forge_llm.application.ports import IAsyncLLMProviderPort

        # Check that it can be used with isinstance
        # Runtime checkable protocols have _is_runtime_protocol attribute
        assert getattr(IAsyncLLMProviderPort, "_is_runtime_protocol", False)

    def test_async_openai_adapter_implements_protocol(self):
        """AsyncOpenAIAdapter should implement IAsyncLLMProviderPort."""
        from forge_llm.infrastructure.providers import AsyncOpenAIAdapter

        config = ProviderConfig(provider="openai", api_key="test-key")
        adapter = AsyncOpenAIAdapter(config)

        # Check it has required attributes/methods
        assert hasattr(adapter, "name")
        assert hasattr(adapter, "config")
        assert hasattr(adapter, "send")
        assert hasattr(adapter, "stream")
        assert hasattr(adapter, "validate")

    def test_async_anthropic_adapter_implements_protocol(self):
        """AsyncAnthropicAdapter should implement IAsyncLLMProviderPort."""
        from forge_llm.infrastructure.providers import AsyncAnthropicAdapter

        config = ProviderConfig(provider="anthropic", api_key="test-key")
        adapter = AsyncAnthropicAdapter(config)

        # Check it has required attributes/methods
        assert hasattr(adapter, "name")
        assert hasattr(adapter, "config")
        assert hasattr(adapter, "send")
        assert hasattr(adapter, "stream")
        assert hasattr(adapter, "validate")
