"""Interface para observers de observabilidade."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class ObserverPort(ABC):
    """
    Interface abstrata para observers de eventos.

    Observers recebem eventos de observabilidade e podem processá-los
    de forma customizada (logging, métricas, callbacks, etc).

    Exemplo:
        class MyObserver(ObserverPort):
            async def on_event(self, event: Any) -> None:
                if isinstance(event, ChatCompleteEvent):
                    print(f"Chat completed in {event.latency_ms}ms")
    """

    @abstractmethod
    async def on_event(self, event: Any) -> None:
        """
        Recebe e processa um evento de observabilidade.

        Args:
            event: Evento de observabilidade (ChatStartEvent, ChatCompleteEvent, etc)
        """
        ...
