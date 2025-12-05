"""Gerenciador de observabilidade do ForgeLLMClient."""

from __future__ import annotations

import contextlib
from dataclasses import dataclass
from typing import Any
from uuid import uuid4

from forge_llm.observability.observer_port import ObserverPort


@dataclass
class ObservabilityConfig:
    """
    Configuração de observabilidade.

    Attributes:
        enabled: Se observabilidade está habilitada
        capture_content: Se deve capturar conteúdo de mensagens (privacy)
    """

    enabled: bool = True
    capture_content: bool = False  # Privacy: não logar conteúdo por default


class ObservabilityManager:
    """
    Gerenciador central de observabilidade.

    Orquestra múltiplos observers e emite eventos para todos eles.

    Exemplo:
        obs = ObservabilityManager()
        obs.add_observer(LoggingObserver())
        obs.add_observer(MetricsObserver())

        await obs.emit(ChatStartEvent(...))
    """

    def __init__(self, config: ObservabilityConfig | None = None) -> None:
        """
        Inicializar gerenciador.

        Args:
            config: Configuração de observabilidade
        """
        self._config = config or ObservabilityConfig()
        self._observers: list[ObserverPort] = []

    @property
    def config(self) -> ObservabilityConfig:
        """Retorna configuração atual."""
        return self._config

    @property
    def enabled(self) -> bool:
        """Indica se observabilidade está habilitada."""
        return self._config.enabled

    @property
    def observer_count(self) -> int:
        """Retorna número de observers registrados."""
        return len(self._observers)

    def add_observer(self, observer: ObserverPort) -> None:
        """
        Adicionar observer.

        Args:
            observer: Observer a adicionar
        """
        if observer not in self._observers:
            self._observers.append(observer)

    def remove_observer(self, observer: ObserverPort) -> None:
        """
        Remover observer.

        Args:
            observer: Observer a remover
        """
        if observer in self._observers:
            self._observers.remove(observer)

    def clear_observers(self) -> None:
        """Remove todos os observers."""
        self._observers.clear()

    async def emit(self, event: Any) -> None:
        """
        Emitir evento para todos os observers.

        Args:
            event: Evento a emitir
        """
        if not self._config.enabled:
            return

        for observer in self._observers:
            with contextlib.suppress(Exception):
                await observer.on_event(event)

    @staticmethod
    def generate_request_id() -> str:
        """Gerar ID único para request."""
        return f"req_{uuid4().hex[:12]}"
