"""Testes unitarios para eventos de observabilidade."""

from datetime import datetime

import pytest

from forge_llm.domain.value_objects import TokenUsage
from forge_llm.observability.events import (
    ChatCompleteEvent,
    ChatErrorEvent,
    ChatStartEvent,
    RetryEvent,
    StreamChunkEvent,
)


class TestChatStartEvent:
    """Testes para ChatStartEvent."""

    def test_criar_evento(self) -> None:
        """Deve criar evento com todos os campos."""
        event = ChatStartEvent(
            timestamp=datetime(2024, 1, 15, 10, 30, 0),
            request_id="req_abc123",
            provider="openai",
            model="gpt-4",
            message_count=3,
            has_tools=True,
        )

        assert event.timestamp == datetime(2024, 1, 15, 10, 30, 0)
        assert event.request_id == "req_abc123"
        assert event.provider == "openai"
        assert event.model == "gpt-4"
        assert event.message_count == 3
        assert event.has_tools is True

    def test_evento_imutavel(self) -> None:
        """Evento deve ser imutavel (frozen)."""
        event = ChatStartEvent(
            timestamp=datetime.now(),
            request_id="req_abc123",
            provider="openai",
            model="gpt-4",
            message_count=1,
            has_tools=False,
        )

        with pytest.raises(AttributeError):
            event.provider = "anthropic"  # type: ignore


class TestChatCompleteEvent:
    """Testes para ChatCompleteEvent."""

    def test_criar_evento(self) -> None:
        """Deve criar evento com todos os campos."""
        usage = TokenUsage(prompt_tokens=10, completion_tokens=20, total_tokens=30)
        event = ChatCompleteEvent(
            timestamp=datetime(2024, 1, 15, 10, 30, 0),
            request_id="req_abc123",
            provider="openai",
            model="gpt-4",
            latency_ms=245.5,
            token_usage=usage,
            finish_reason="stop",
            tool_calls_count=0,
        )

        assert event.request_id == "req_abc123"
        assert event.latency_ms == 245.5
        assert event.token_usage.total_tokens == 30
        assert event.finish_reason == "stop"
        assert event.tool_calls_count == 0

    def test_evento_com_tool_calls(self) -> None:
        """Deve registrar tool calls."""
        usage = TokenUsage(prompt_tokens=10, completion_tokens=20, total_tokens=30)
        event = ChatCompleteEvent(
            timestamp=datetime.now(),
            request_id="req_abc123",
            provider="anthropic",
            model="claude-3",
            latency_ms=300.0,
            token_usage=usage,
            finish_reason="tool_use",
            tool_calls_count=2,
        )

        assert event.finish_reason == "tool_use"
        assert event.tool_calls_count == 2


class TestChatErrorEvent:
    """Testes para ChatErrorEvent."""

    def test_criar_evento_erro(self) -> None:
        """Deve criar evento de erro."""
        event = ChatErrorEvent(
            timestamp=datetime.now(),
            request_id="req_abc123",
            provider="openai",
            error_type="RateLimitError",
            error_message="Rate limit exceeded",
            latency_ms=50.0,
            retryable=True,
        )

        assert event.error_type == "RateLimitError"
        assert event.error_message == "Rate limit exceeded"
        assert event.retryable is True

    def test_erro_nao_retryable(self) -> None:
        """Deve marcar erros nao retryaveis."""
        event = ChatErrorEvent(
            timestamp=datetime.now(),
            request_id="req_abc123",
            provider="openai",
            error_type="AuthenticationError",
            error_message="Invalid API key",
            latency_ms=10.0,
            retryable=False,
        )

        assert event.retryable is False


class TestRetryEvent:
    """Testes para RetryEvent."""

    def test_criar_evento_retry(self) -> None:
        """Deve criar evento de retry."""
        event = RetryEvent(
            timestamp=datetime.now(),
            request_id="req_abc123",
            provider="openai",
            attempt=2,
            max_attempts=3,
            delay_ms=2000.0,
            error_type="RateLimitError",
        )

        assert event.attempt == 2
        assert event.max_attempts == 3
        assert event.delay_ms == 2000.0
        assert event.error_type == "RateLimitError"


class TestStreamChunkEvent:
    """Testes para StreamChunkEvent."""

    def test_criar_evento_chunk(self) -> None:
        """Deve criar evento de chunk."""
        event = StreamChunkEvent(
            timestamp=datetime.now(),
            request_id="req_abc123",
            provider="openai",
            chunk_index=5,
            has_content=True,
            has_tool_call=False,
        )

        assert event.chunk_index == 5
        assert event.has_content is True
        assert event.has_tool_call is False

    def test_chunk_com_tool_call(self) -> None:
        """Deve registrar chunk com tool call."""
        event = StreamChunkEvent(
            timestamp=datetime.now(),
            request_id="req_abc123",
            provider="anthropic",
            chunk_index=10,
            has_content=False,
            has_tool_call=True,
        )

        assert event.has_content is False
        assert event.has_tool_call is True
