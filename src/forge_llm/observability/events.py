"""Eventos de observabilidade do ForgeLLMClient."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from forge_llm.domain.value_objects import TokenUsage


@dataclass(frozen=True)
class ChatStartEvent:
    """Evento emitido no início de uma chamada chat."""

    timestamp: datetime
    request_id: str
    provider: str
    model: str | None
    message_count: int
    has_tools: bool


@dataclass(frozen=True)
class ChatCompleteEvent:
    """Evento emitido quando uma chamada chat é concluída com sucesso."""

    timestamp: datetime
    request_id: str
    provider: str
    model: str
    latency_ms: float
    token_usage: TokenUsage
    finish_reason: str
    tool_calls_count: int


@dataclass(frozen=True)
class ChatErrorEvent:
    """Evento emitido quando uma chamada chat falha."""

    timestamp: datetime
    request_id: str
    provider: str
    error_type: str
    error_message: str
    latency_ms: float
    retryable: bool


@dataclass(frozen=True)
class RetryEvent:
    """Evento emitido quando ocorre uma tentativa de retry."""

    timestamp: datetime
    request_id: str
    provider: str
    attempt: int
    max_attempts: int
    delay_ms: float
    error_type: str


@dataclass(frozen=True)
class StreamChunkEvent:
    """Evento emitido para cada chunk de streaming."""

    timestamp: datetime
    request_id: str
    provider: str
    chunk_index: int
    has_content: bool
    has_tool_call: bool
