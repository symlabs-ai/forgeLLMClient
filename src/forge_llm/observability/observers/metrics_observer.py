"""Observer de métricas para observabilidade."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from typing import Any

from forge_llm.observability.events import (
    ChatCompleteEvent,
    ChatErrorEvent,
    ChatStartEvent,
    RetryEvent,
)
from forge_llm.observability.observer_port import ObserverPort


@dataclass
class UsageMetrics:
    """
    Métricas agregadas de uso.

    Rastreia totais de requests, tokens, erros e latência.

    Exemplo:
        metrics = MetricsObserver()
        # ... após várias chamadas ...
        print(metrics.metrics.total_tokens)  # 1234
        print(metrics.metrics.avg_latency_ms)  # 312.5
    """

    total_requests: int = 0
    total_tokens: int = 0
    total_prompt_tokens: int = 0
    total_completion_tokens: int = 0
    total_errors: int = 0
    total_retries: int = 0
    requests_by_provider: dict[str, int] = field(default_factory=dict)
    tokens_by_provider: dict[str, int] = field(default_factory=dict)
    errors_by_type: dict[str, int] = field(default_factory=dict)
    latency_sum_ms: float = 0.0
    latency_count: int = 0

    @property
    def avg_latency_ms(self) -> float:
        """Calcula latência média em ms."""
        if self.latency_count == 0:
            return 0.0
        return self.latency_sum_ms / self.latency_count

    def to_dict(self) -> dict[str, Any]:
        """Converte métricas para dicionário."""
        return {
            "total_requests": self.total_requests,
            "total_tokens": self.total_tokens,
            "total_prompt_tokens": self.total_prompt_tokens,
            "total_completion_tokens": self.total_completion_tokens,
            "total_errors": self.total_errors,
            "total_retries": self.total_retries,
            "requests_by_provider": self.requests_by_provider.copy(),
            "tokens_by_provider": self.tokens_by_provider.copy(),
            "errors_by_type": self.errors_by_type.copy(),
            "avg_latency_ms": self.avg_latency_ms,
        }


class MetricsObserver(ObserverPort):
    """
    Observer que coleta métricas agregadas.

    Thread-safe usando asyncio.Lock.

    Exemplo:
        obs = ObservabilityManager()
        metrics = MetricsObserver()
        obs.add_observer(metrics)

        # Após chamadas...
        print(metrics.metrics.total_tokens)
        print(metrics.metrics.requests_by_provider)
    """

    def __init__(self) -> None:
        """Inicializar observer."""
        self._metrics = UsageMetrics()
        self._lock = asyncio.Lock()

    @property
    def metrics(self) -> UsageMetrics:
        """Retorna métricas atuais."""
        return self._metrics

    def reset(self) -> None:
        """Reseta todas as métricas."""
        self._metrics = UsageMetrics()

    async def on_event(self, event: Any) -> None:
        """
        Processar evento e atualizar métricas.

        Args:
            event: Evento de observabilidade
        """
        async with self._lock:
            if isinstance(event, ChatStartEvent):
                self._on_chat_start(event)
            elif isinstance(event, ChatCompleteEvent):
                self._on_chat_complete(event)
            elif isinstance(event, ChatErrorEvent):
                self._on_chat_error(event)
            elif isinstance(event, RetryEvent):
                self._on_retry(event)

    def _on_chat_start(self, event: ChatStartEvent) -> None:
        """Processar início de chat."""
        self._metrics.total_requests += 1

        provider = event.provider
        if provider not in self._metrics.requests_by_provider:
            self._metrics.requests_by_provider[provider] = 0
        self._metrics.requests_by_provider[provider] += 1

    def _on_chat_complete(self, event: ChatCompleteEvent) -> None:
        """Processar conclusão de chat."""
        # Tokens
        usage = event.token_usage
        self._metrics.total_tokens += usage.total_tokens
        self._metrics.total_prompt_tokens += usage.prompt_tokens
        self._metrics.total_completion_tokens += usage.completion_tokens

        provider = event.provider
        if provider not in self._metrics.tokens_by_provider:
            self._metrics.tokens_by_provider[provider] = 0
        self._metrics.tokens_by_provider[provider] += usage.total_tokens

        # Latência
        self._metrics.latency_sum_ms += event.latency_ms
        self._metrics.latency_count += 1

    def _on_chat_error(self, event: ChatErrorEvent) -> None:
        """Processar erro de chat."""
        self._metrics.total_errors += 1

        error_type = event.error_type
        if error_type not in self._metrics.errors_by_type:
            self._metrics.errors_by_type[error_type] = 0
        self._metrics.errors_by_type[error_type] += 1

    def _on_retry(self, event: RetryEvent) -> None:
        """Processar retry."""
        self._metrics.total_retries += 1
