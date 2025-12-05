"""Observer de callbacks para observabilidade."""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any

from forge_llm.observability.events import (
    ChatCompleteEvent,
    ChatErrorEvent,
    ChatStartEvent,
    RetryEvent,
    StreamChunkEvent,
)
from forge_llm.observability.observer_port import ObserverPort


class CallbackObserver(ObserverPort):
    """
    Observer que executa callbacks customizados.

    Permite registrar funções para cada tipo de evento.

    Exemplo:
        async def on_complete(event):
            print(f"Completed in {event.latency_ms}ms")

        obs = CallbackObserver(on_complete=on_complete)
    """

    def __init__(
        self,
        on_start: Callable[[ChatStartEvent], Awaitable[None]] | None = None,
        on_complete: Callable[[ChatCompleteEvent], Awaitable[None]] | None = None,
        on_error: Callable[[ChatErrorEvent], Awaitable[None]] | None = None,
        on_retry: Callable[[RetryEvent], Awaitable[None]] | None = None,
        on_stream_chunk: Callable[[StreamChunkEvent], Awaitable[None]] | None = None,
    ) -> None:
        """
        Inicializar observer com callbacks.

        Args:
            on_start: Callback para ChatStartEvent
            on_complete: Callback para ChatCompleteEvent
            on_error: Callback para ChatErrorEvent
            on_retry: Callback para RetryEvent
            on_stream_chunk: Callback para StreamChunkEvent
        """
        self._on_start = on_start
        self._on_complete = on_complete
        self._on_error = on_error
        self._on_retry = on_retry
        self._on_stream_chunk = on_stream_chunk

    async def on_event(self, event: Any) -> None:
        """
        Processar evento e executar callback correspondente.

        Args:
            event: Evento de observabilidade
        """
        if isinstance(event, ChatStartEvent) and self._on_start:
            await self._on_start(event)
        elif isinstance(event, ChatCompleteEvent) and self._on_complete:
            await self._on_complete(event)
        elif isinstance(event, ChatErrorEvent) and self._on_error:
            await self._on_error(event)
        elif isinstance(event, RetryEvent) and self._on_retry:
            await self._on_retry(event)
        elif isinstance(event, StreamChunkEvent) and self._on_stream_chunk:
            await self._on_stream_chunk(event)
