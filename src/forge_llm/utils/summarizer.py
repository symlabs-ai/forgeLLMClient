"""Conversation summarization utilities."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from forge_llm.application.ports.provider_port import ProviderPort
    from forge_llm.domain.value_objects import Message


@dataclass
class SummarizerConfig:
    """Configuration for conversation summarization."""

    # Maximum messages before triggering summarization
    max_messages: int = 50
    # Minimum messages to keep (most recent)
    keep_recent: int = 10
    # Whether to auto-summarize when threshold reached
    auto_summarize: bool = True
    # Model to use for summarization (if different from main)
    summary_model: str | None = None
    # Maximum tokens for summary
    max_summary_tokens: int = 500
    # System prompt for summarization
    summary_prompt: str = (
        "Summarize the following conversation concisely, "
        "capturing the main topics discussed, key decisions made, "
        "and any important context that should be remembered. "
        "Focus on facts and outcomes rather than dialogue structure."
    )


@dataclass
class SummaryResult:
    """Result of a conversation summarization."""

    summary: str
    original_message_count: int
    summarized_message_count: int
    tokens_saved: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def messages_condensed(self) -> int:
        """Number of messages condensed into the summary."""
        return self.original_message_count - self.summarized_message_count


class SummarizerPort(ABC):
    """Abstract interface for conversation summarization."""

    @abstractmethod
    async def summarize(
        self,
        messages: list[Message],
        config: SummarizerConfig | None = None,
    ) -> SummaryResult:
        """
        Summarize a list of messages.

        Args:
            messages: Messages to summarize
            config: Optional summarization config

        Returns:
            SummaryResult with summary and metadata
        """
        ...

    @abstractmethod
    async def should_summarize(
        self,
        messages: list[Message],
        config: SummarizerConfig | None = None,
    ) -> bool:
        """
        Check if messages should be summarized.

        Args:
            messages: Current messages
            config: Optional config

        Returns:
            True if summarization is recommended
        """
        ...


class ConversationSummarizer(SummarizerPort):
    """
    Summarizes conversations using an LLM provider.

    Example:
        summarizer = ConversationSummarizer(provider)
        if await summarizer.should_summarize(messages):
            result = await summarizer.summarize(messages)
            new_messages = summarizer.apply_summary(messages, result)
    """

    def __init__(
        self,
        provider: ProviderPort,
        config: SummarizerConfig | None = None,
    ) -> None:
        self._provider = provider
        self._config = config or SummarizerConfig()

    async def should_summarize(
        self,
        messages: list[Message],
        config: SummarizerConfig | None = None,
    ) -> bool:
        """Check if messages exceed the threshold for summarization."""
        cfg = config or self._config
        return len(messages) > cfg.max_messages

    async def summarize(
        self,
        messages: list[Message],
        config: SummarizerConfig | None = None,
    ) -> SummaryResult:
        """
        Summarize older messages using the LLM.

        Keeps the most recent messages and summarizes the rest.
        """
        cfg = config or self._config

        if len(messages) <= cfg.keep_recent:
            # Not enough messages to summarize
            return SummaryResult(
                summary="",
                original_message_count=len(messages),
                summarized_message_count=len(messages),
            )

        # Split messages: older ones to summarize, recent ones to keep
        messages_to_summarize = messages[: -cfg.keep_recent]
        original_count = len(messages)

        # Format messages for summarization
        conversation_text = self._format_messages(messages_to_summarize)

        # Create summarization request
        from forge_llm.domain.value_objects import Message

        summary_messages = [
            Message(role="system", content=cfg.summary_prompt),
            Message(role="user", content=f"Conversation to summarize:\n\n{conversation_text}"),
        ]

        # Get summary from LLM
        response = await self._provider.chat(
            messages=summary_messages,
            model=cfg.summary_model,
            max_tokens=cfg.max_summary_tokens,
        )

        # Estimate tokens saved (rough approximation)
        original_chars = sum(len(m.content or "") for m in messages_to_summarize)
        summary_chars = len(response.content or "")
        tokens_saved = max(0, (original_chars - summary_chars) // 4)  # ~4 chars per token

        return SummaryResult(
            summary=response.content or "",
            original_message_count=original_count,
            summarized_message_count=cfg.keep_recent + 1,  # +1 for summary message
            tokens_saved=tokens_saved,
            metadata={
                "messages_summarized": len(messages_to_summarize),
                "model_used": response.model,
            },
        )

    def _format_messages(self, messages: list[Message]) -> str:
        """Format messages into text for summarization."""
        lines = []
        for msg in messages:
            role = msg.role.upper()
            content = msg.content or "[no content]"
            lines.append(f"{role}: {content}")
        return "\n\n".join(lines)

    def apply_summary(
        self,
        messages: list[Message],
        result: SummaryResult,
        config: SummarizerConfig | None = None,
    ) -> list[Message]:
        """
        Apply a summary to the messages list.

        Returns a new list with the summary as a system message
        followed by the most recent messages.
        """
        cfg = config or self._config

        if not result.summary:
            return messages

        from forge_llm.domain.value_objects import Message

        # Create summary message
        summary_msg = Message(
            role="system",
            content=f"[Previous conversation summary: {result.summary}]",
        )

        # Find system messages from the ORIGINAL messages (not just recent)
        original_system_messages = [m for m in messages if m.role == "system"]

        # Keep recent non-system messages
        non_system_messages = [m for m in messages if m.role != "system"]
        recent_non_system = (
            non_system_messages[-cfg.keep_recent:]
            if len(non_system_messages) > cfg.keep_recent
            else non_system_messages
        )

        # Place original system messages first, then summary, then recent messages
        return original_system_messages + [summary_msg] + recent_non_system


class NoOpSummarizer(SummarizerPort):
    """A summarizer that does nothing (for disabled summarization)."""

    async def summarize(
        self,
        messages: list[Message],
        config: SummarizerConfig | None = None,
    ) -> SummaryResult:
        """Return empty result."""
        return SummaryResult(
            summary="",
            original_message_count=len(messages),
            summarized_message_count=len(messages),
        )

    async def should_summarize(
        self,
        messages: list[Message],
        config: SummarizerConfig | None = None,
    ) -> bool:
        """Always returns False."""
        return False
