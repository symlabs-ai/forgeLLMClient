"""
Unit tests for ChatChunk entity.

Tests for streaming chunk representation and factory methods.
"""
from unittest.mock import MagicMock

import pytest

from forge_llm.domain.entities import ChatChunk


class TestChatChunkCreation:
    """Tests for ChatChunk instantiation."""

    def test_create_basic_chunk(self):
        """Should create chunk with content."""
        chunk = ChatChunk(content="Hello")

        assert chunk.content == "Hello"
        assert chunk.role == "assistant"
        assert chunk.finish_reason is None
        assert chunk.is_final is False

    def test_create_chunk_with_all_fields(self):
        """Should create chunk with all fields."""
        chunk = ChatChunk(
            content="Done",
            role="assistant",
            finish_reason="stop",
            is_final=True,
            usage={"prompt_tokens": 10, "completion_tokens": 5},
            tool_calls=[{"id": "call_1", "type": "function"}],
        )

        assert chunk.content == "Done"
        assert chunk.finish_reason == "stop"
        assert chunk.is_final is True
        assert chunk.usage["prompt_tokens"] == 10
        assert len(chunk.tool_calls) == 1

    def test_create_empty_chunk(self):
        """Should create empty chunk."""
        chunk = ChatChunk(content="")

        assert chunk.content == ""
        assert chunk.is_final is False

    def test_create_final_chunk(self):
        """Should create final chunk with finish_reason."""
        chunk = ChatChunk(content="", finish_reason="stop", is_final=True)

        assert chunk.is_final is True
        assert chunk.finish_reason == "stop"

    def test_create_tool_calls_chunk(self):
        """Should create chunk with tool_calls."""
        tool_calls = [
            {
                "id": "call_123",
                "type": "function",
                "function": {"name": "get_weather", "arguments": '{"loc": "NYC"}'},
            }
        ]
        chunk = ChatChunk(
            content="",
            finish_reason="tool_calls",
            is_final=True,
            tool_calls=tool_calls,
        )

        assert chunk.finish_reason == "tool_calls"
        assert chunk.tool_calls is not None
        assert chunk.tool_calls[0]["id"] == "call_123"


class TestChatChunkFromOpenAI:
    """Tests for ChatChunk.from_openai() factory method."""

    def test_from_openai_content_chunk(self):
        """Should parse OpenAI content chunk."""
        mock_chunk = MagicMock()
        mock_chunk.choices = [MagicMock()]
        mock_chunk.choices[0].delta.content = "Hello"
        mock_chunk.choices[0].delta.role = "assistant"
        mock_chunk.choices[0].finish_reason = None

        chunk = ChatChunk.from_openai(mock_chunk)

        assert chunk.content == "Hello"
        assert chunk.role == "assistant"
        assert chunk.is_final is False

    def test_from_openai_final_chunk(self):
        """Should parse OpenAI final chunk."""
        mock_chunk = MagicMock()
        mock_chunk.choices = [MagicMock()]
        mock_chunk.choices[0].delta.content = ""
        mock_chunk.choices[0].delta.role = None
        mock_chunk.choices[0].finish_reason = "stop"

        chunk = ChatChunk.from_openai(mock_chunk)

        assert chunk.finish_reason == "stop"
        assert chunk.is_final is True

    def test_from_openai_empty_choices(self):
        """Should handle empty choices."""
        mock_chunk = MagicMock()
        mock_chunk.choices = []

        chunk = ChatChunk.from_openai(mock_chunk)

        assert chunk.content == ""
        assert chunk.is_final is False

    def test_from_openai_no_content(self):
        """Should handle chunk without content."""
        mock_chunk = MagicMock()
        mock_chunk.choices = [MagicMock()]
        mock_chunk.choices[0].delta.content = None
        mock_chunk.choices[0].delta.role = None
        mock_chunk.choices[0].finish_reason = None

        chunk = ChatChunk.from_openai(mock_chunk)

        assert chunk.content == ""

    def test_from_openai_with_role(self):
        """Should parse role from delta."""
        mock_chunk = MagicMock()
        mock_chunk.choices = [MagicMock()]
        mock_chunk.choices[0].delta.content = "Hi"
        mock_chunk.choices[0].delta.role = "assistant"
        mock_chunk.choices[0].finish_reason = None

        chunk = ChatChunk.from_openai(mock_chunk)

        assert chunk.role == "assistant"


class TestChatChunkFromAnthropic:
    """Tests for ChatChunk.from_anthropic() factory method."""

    def test_from_anthropic_content_delta(self):
        """Should parse Anthropic content_block_delta event."""
        mock_event = MagicMock()
        mock_event.type = "content_block_delta"
        mock_event.delta.text = "Hello"

        chunk = ChatChunk.from_anthropic(mock_event)

        assert chunk.content == "Hello"
        assert chunk.role == "assistant"
        assert chunk.is_final is False

    def test_from_anthropic_message_stop(self):
        """Should parse Anthropic message_stop event."""
        mock_event = MagicMock()
        mock_event.type = "message_stop"

        chunk = ChatChunk.from_anthropic(mock_event)

        assert chunk.content == ""
        assert chunk.finish_reason == "stop"
        assert chunk.is_final is True

    def test_from_anthropic_other_event(self):
        """Should handle other Anthropic events."""
        mock_event = MagicMock()
        mock_event.type = "content_block_start"

        chunk = ChatChunk.from_anthropic(mock_event)

        assert chunk.content == ""
        assert chunk.is_final is False

    def test_from_anthropic_no_text_attribute(self):
        """Should handle delta without text attribute."""
        mock_event = MagicMock()
        mock_event.type = "content_block_delta"
        # Remove text attribute
        del mock_event.delta.text

        chunk = ChatChunk.from_anthropic(mock_event)

        assert chunk.content == ""


class TestChatChunkEquality:
    """Tests for ChatChunk equality and hashing."""

    def test_chunks_equal(self):
        """Same chunks should be equal."""
        chunk1 = ChatChunk(content="Hello", role="assistant")
        chunk2 = ChatChunk(content="Hello", role="assistant")

        assert chunk1 == chunk2

    def test_chunks_not_equal(self):
        """Different chunks should not be equal."""
        chunk1 = ChatChunk(content="Hello")
        chunk2 = ChatChunk(content="World")

        assert chunk1 != chunk2

    def test_chunk_repr(self):
        """ChatChunk should have string representation."""
        chunk = ChatChunk(content="Hello", finish_reason="stop")

        repr_str = repr(chunk)

        assert "Hello" in repr_str
        assert "stop" in repr_str
