"""Tests for the conversation summarizer."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from forge_llm.domain.entities import ChatResponse
from forge_llm.domain.value_objects import Message, TokenUsage
from forge_llm.utils.summarizer import (
    ConversationSummarizer,
    NoOpSummarizer,
    SummarizerConfig,
    SummaryResult,
)


class TestSummarizerConfig:
    """Tests for SummarizerConfig."""

    def test_defaults(self) -> None:
        """Test default configuration."""
        config = SummarizerConfig()

        assert config.max_messages == 50
        assert config.keep_recent == 10
        assert config.auto_summarize is True
        assert config.summary_model is None
        assert config.max_summary_tokens == 500

    def test_custom_values(self) -> None:
        """Test custom configuration."""
        config = SummarizerConfig(
            max_messages=100,
            keep_recent=20,
            auto_summarize=False,
            summary_model="gpt-4",
        )

        assert config.max_messages == 100
        assert config.keep_recent == 20
        assert config.auto_summarize is False
        assert config.summary_model == "gpt-4"


class TestSummaryResult:
    """Tests for SummaryResult."""

    def test_messages_condensed(self) -> None:
        """Test messages_condensed calculation."""
        result = SummaryResult(
            summary="test summary",
            original_message_count=50,
            summarized_message_count=11,  # 10 kept + 1 summary
        )

        assert result.messages_condensed == 39

    def test_with_metadata(self) -> None:
        """Test result with metadata."""
        result = SummaryResult(
            summary="test",
            original_message_count=50,
            summarized_message_count=11,
            tokens_saved=1000,
            metadata={"model_used": "gpt-4"},
        )

        assert result.tokens_saved == 1000
        assert result.metadata["model_used"] == "gpt-4"


class TestConversationSummarizer:
    """Tests for ConversationSummarizer."""

    @pytest.fixture
    def mock_provider(self) -> MagicMock:
        """Create a mock provider."""
        provider = MagicMock()
        provider.chat = AsyncMock(
            return_value=ChatResponse(
                content="This is a summary of the conversation.",
                model="gpt-4",
                provider="openai",
                finish_reason="stop",
                usage=TokenUsage(prompt_tokens=100, completion_tokens=50, total_tokens=150),
            )
        )
        return provider

    @pytest.fixture
    def summarizer(self, mock_provider: MagicMock) -> ConversationSummarizer:
        """Create a summarizer instance."""
        return ConversationSummarizer(
            provider=mock_provider,
            config=SummarizerConfig(max_messages=10, keep_recent=3),
        )

    @pytest.fixture
    def many_messages(self) -> list[Message]:
        """Create a list of messages exceeding threshold."""
        messages = []
        for i in range(15):
            messages.append(Message(role="user", content=f"Message {i}"))
            messages.append(Message(role="assistant", content=f"Response {i}"))
        return messages

    @pytest.fixture
    def few_messages(self) -> list[Message]:
        """Create a list of messages below threshold."""
        return [
            Message(role="user", content="Hello"),
            Message(role="assistant", content="Hi there!"),
        ]

    @pytest.mark.asyncio
    async def test_should_summarize_true(
        self, summarizer: ConversationSummarizer, many_messages: list[Message]
    ) -> None:
        """Test should_summarize returns True when over threshold."""
        result = await summarizer.should_summarize(many_messages)
        assert result is True

    @pytest.mark.asyncio
    async def test_should_summarize_false(
        self, summarizer: ConversationSummarizer, few_messages: list[Message]
    ) -> None:
        """Test should_summarize returns False when under threshold."""
        result = await summarizer.should_summarize(few_messages)
        assert result is False

    @pytest.mark.asyncio
    async def test_summarize_returns_result(
        self,
        summarizer: ConversationSummarizer,
        many_messages: list[Message],
        mock_provider: MagicMock,
    ) -> None:
        """Test summarize returns a SummaryResult."""
        result = await summarizer.summarize(many_messages)

        assert isinstance(result, SummaryResult)
        assert result.summary == "This is a summary of the conversation."
        assert result.original_message_count == len(many_messages)
        assert result.summarized_message_count == 4  # 3 kept + 1 summary
        assert mock_provider.chat.called

    @pytest.mark.asyncio
    async def test_summarize_calls_provider(
        self,
        summarizer: ConversationSummarizer,
        many_messages: list[Message],
        mock_provider: MagicMock,
    ) -> None:
        """Test that summarize calls the provider correctly."""
        await summarizer.summarize(many_messages)

        mock_provider.chat.assert_called_once()
        call_kwargs = mock_provider.chat.call_args.kwargs
        assert "messages" in call_kwargs
        assert call_kwargs["max_tokens"] == 500

    @pytest.mark.asyncio
    async def test_summarize_few_messages(
        self, summarizer: ConversationSummarizer, few_messages: list[Message]
    ) -> None:
        """Test summarize with few messages returns empty summary."""
        result = await summarizer.summarize(few_messages)

        assert result.summary == ""
        assert result.original_message_count == len(few_messages)
        assert result.summarized_message_count == len(few_messages)

    @pytest.mark.asyncio
    async def test_summarize_with_custom_config(
        self, mock_provider: MagicMock, many_messages: list[Message]
    ) -> None:
        """Test summarize with custom config."""
        summarizer = ConversationSummarizer(
            provider=mock_provider,
            config=SummarizerConfig(keep_recent=5, summary_model="gpt-3.5-turbo"),
        )

        await summarizer.summarize(many_messages)

        call_kwargs = mock_provider.chat.call_args.kwargs
        assert call_kwargs["model"] == "gpt-3.5-turbo"

    def test_apply_summary(
        self, summarizer: ConversationSummarizer, many_messages: list[Message]
    ) -> None:
        """Test applying a summary to messages."""
        result = SummaryResult(
            summary="Previous discussion summary.",
            original_message_count=len(many_messages),
            summarized_message_count=4,
        )

        new_messages = summarizer.apply_summary(many_messages, result)

        # Should have summary message + keep_recent messages
        assert len(new_messages) == 4  # 1 summary + 3 recent
        assert "[Previous conversation summary:" in new_messages[0].content or ""

    def test_apply_summary_empty(
        self, summarizer: ConversationSummarizer, many_messages: list[Message]
    ) -> None:
        """Test applying an empty summary returns original messages."""
        result = SummaryResult(
            summary="",
            original_message_count=len(many_messages),
            summarized_message_count=len(many_messages),
        )

        new_messages = summarizer.apply_summary(many_messages, result)
        assert new_messages == many_messages

    def test_apply_summary_preserves_system_messages(
        self, summarizer: ConversationSummarizer
    ) -> None:
        """Test that apply_summary preserves existing system messages."""
        messages = [
            Message(role="system", content="You are a helpful assistant."),
            Message(role="user", content="Hello 1"),
            Message(role="assistant", content="Response 1"),
            Message(role="user", content="Hello 2"),
            Message(role="assistant", content="Response 2"),
            Message(role="user", content="Hello 3"),
            Message(role="assistant", content="Response 3"),
            Message(role="user", content="Hello 4"),
            Message(role="assistant", content="Response 4"),
        ]

        result = SummaryResult(
            summary="Previous conversation summary.",
            original_message_count=len(messages),
            summarized_message_count=4,
        )

        new_messages = summarizer.apply_summary(messages, result)

        # First message should be the original system message
        assert new_messages[0].role == "system"
        assert new_messages[0].content == "You are a helpful assistant."


class TestNoOpSummarizer:
    """Tests for NoOpSummarizer."""

    @pytest.fixture
    def summarizer(self) -> NoOpSummarizer:
        """Create a no-op summarizer."""
        return NoOpSummarizer()

    @pytest.mark.asyncio
    async def test_should_summarize_always_false(
        self, summarizer: NoOpSummarizer
    ) -> None:
        """Test should_summarize always returns False."""
        messages = [Message(role="user", content="test") for _ in range(100)]
        result = await summarizer.should_summarize(messages)
        assert result is False

    @pytest.mark.asyncio
    async def test_summarize_returns_empty(self, summarizer: NoOpSummarizer) -> None:
        """Test summarize returns empty result."""
        messages = [Message(role="user", content="test")]
        result = await summarizer.summarize(messages)

        assert result.summary == ""
        assert result.original_message_count == 1
        assert result.summarized_message_count == 1
