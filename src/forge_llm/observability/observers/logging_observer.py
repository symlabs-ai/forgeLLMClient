"""Observer de logging para observabilidade."""

from __future__ import annotations

import logging
from typing import Any

from forge_llm.observability.events import (
    ChatCompleteEvent,
    ChatErrorEvent,
    ChatStartEvent,
    RetryEvent,
    StreamChunkEvent,
)
from forge_llm.observability.observer_port import ObserverPort


class LoggingObserver(ObserverPort):
    """
    Observer que loga eventos usando logging stdlib.

    Loga eventos de forma estruturada para facilitar análise.

    Exemplo:
        obs = ObservabilityManager()
        obs.add_observer(LoggingObserver())

        # Logs:
        # INFO - [req_abc123] Chat started: provider=openai, model=gpt-4
        # INFO - [req_abc123] Chat completed: latency=245ms, tokens=42
    """

    def __init__(
        self,
        logger: logging.Logger | None = None,
        level: int = logging.INFO,
    ) -> None:
        """
        Inicializar observer.

        Args:
            logger: Logger a usar (default: forge_llm)
            level: Nível de log (default: INFO)
        """
        self._logger = logger or logging.getLogger("forge_llm")
        self._level = level

    async def on_event(self, event: Any) -> None:
        """
        Processar evento e logar.

        Args:
            event: Evento de observabilidade
        """
        if isinstance(event, ChatStartEvent):
            self._log_chat_start(event)
        elif isinstance(event, ChatCompleteEvent):
            self._log_chat_complete(event)
        elif isinstance(event, ChatErrorEvent):
            self._log_chat_error(event)
        elif isinstance(event, RetryEvent):
            self._log_retry(event)
        elif isinstance(event, StreamChunkEvent):
            self._log_stream_chunk(event)

    def _log_chat_start(self, event: ChatStartEvent) -> None:
        """Logar início de chat."""
        self._logger.log(
            self._level,
            "[%s] Chat started: provider=%s, model=%s, messages=%d, tools=%s",
            event.request_id,
            event.provider,
            event.model or "default",
            event.message_count,
            event.has_tools,
        )

    def _log_chat_complete(self, event: ChatCompleteEvent) -> None:
        """Logar conclusão de chat."""
        self._logger.log(
            self._level,
            "[%s] Chat completed: provider=%s, model=%s, latency=%.1fms, "
            "tokens=%d (prompt=%d, completion=%d), finish=%s, tool_calls=%d",
            event.request_id,
            event.provider,
            event.model,
            event.latency_ms,
            event.token_usage.total_tokens,
            event.token_usage.prompt_tokens,
            event.token_usage.completion_tokens,
            event.finish_reason,
            event.tool_calls_count,
        )

    def _log_chat_error(self, event: ChatErrorEvent) -> None:
        """Logar erro de chat."""
        self._logger.log(
            logging.ERROR,
            "[%s] Chat error: provider=%s, error=%s, message=%s, "
            "latency=%.1fms, retryable=%s",
            event.request_id,
            event.provider,
            event.error_type,
            event.error_message,
            event.latency_ms,
            event.retryable,
        )

    def _log_retry(self, event: RetryEvent) -> None:
        """Logar tentativa de retry."""
        self._logger.log(
            logging.WARNING,
            "[%s] Retry: provider=%s, attempt=%d/%d, delay=%.1fms, error=%s",
            event.request_id,
            event.provider,
            event.attempt,
            event.max_attempts,
            event.delay_ms,
            event.error_type,
        )

    def _log_stream_chunk(self, event: StreamChunkEvent) -> None:
        """Logar chunk de streaming."""
        self._logger.log(
            logging.DEBUG,
            "[%s] Stream chunk: provider=%s, index=%d, content=%s, tool_call=%s",
            event.request_id,
            event.provider,
            event.chunk_index,
            event.has_content,
            event.has_tool_call,
        )
