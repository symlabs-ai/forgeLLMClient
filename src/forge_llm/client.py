"""Cliente principal do ForgeLLMClient."""

from __future__ import annotations

import time
from collections.abc import AsyncIterator
from datetime import datetime
from typing import TYPE_CHECKING, Any

from forge_llm.application.ports.provider_port import ProviderPort
from forge_llm.domain.entities import ChatResponse, Conversation
from forge_llm.domain.exceptions import ValidationError
from forge_llm.domain.value_objects import Message
from forge_llm.infrastructure.retry import RetryConfig, with_retry
from forge_llm.providers.registry import ProviderRegistry

if TYPE_CHECKING:
    from forge_llm.observability.manager import ObservabilityManager


class Client:
    """
    Cliente principal do ForgeLLMClient.

    Facade que simplifica uso do SDK.

    Exemplo:
        client = Client(provider="openai", api_key="sk-...")
        response = await client.chat("Ola!")
        print(response.content)

    Com retry:
        client = Client(provider="openai", api_key="sk-...", max_retries=3)
        response = await client.chat("Ola!")  # Auto-retry on transient errors
    """

    def __init__(
        self,
        provider: str | ProviderPort | None = None,
        api_key: str | None = None,
        model: str | None = None,
        max_retries: int = 0,
        retry_delay: float = 1.0,
        retry_config: RetryConfig | None = None,
        observability: ObservabilityManager | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Inicializar cliente.

        Args:
            provider: Nome do provider ou instancia de ProviderPort
            api_key: API key para o provider
            model: Modelo padrao a usar
            max_retries: Numero maximo de retries (0 = sem retry)
            retry_delay: Delay base entre retries em segundos
            retry_config: Configuracao de retry customizada (sobrescreve max_retries/retry_delay)
            observability: Gerenciador de observabilidade para logging/metricas
            **kwargs: Argumentos adicionais para o provider
        """
        self._provider: ProviderPort | None = None
        self._default_model = model
        self._observability = observability
        self._retry_config: RetryConfig | None = None

        # Configurar retry
        if retry_config is not None:
            self._retry_config = retry_config
        elif max_retries > 0:
            self._retry_config = RetryConfig(
                max_retries=max_retries,
                base_delay=retry_delay,
            )

        if provider is not None:
            self.configure(provider, api_key=api_key, **kwargs)

    def configure(
        self,
        provider: str | ProviderPort,
        api_key: str | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Configurar ou reconfigurar o cliente.

        Args:
            provider: Nome do provider ou instancia
            api_key: API key para o provider
            **kwargs: Argumentos adicionais
        """
        if isinstance(provider, str):
            self._provider = ProviderRegistry.create(
                provider,
                api_key=api_key,
                **kwargs,
            )
        else:
            self._provider = provider

    @property
    def is_configured(self) -> bool:
        """Indica se o cliente esta configurado."""
        return self._provider is not None

    @property
    def provider_name(self) -> str:
        """Nome do provedor ativo."""
        if self._provider is None:
            raise RuntimeError("Cliente nao configurado")
        return self._provider.provider_name

    @property
    def model(self) -> str:
        """Modelo ativo."""
        if self._provider is None:
            raise RuntimeError("Cliente nao configurado")
        return self._default_model or self._provider.default_model

    def create_conversation(
        self,
        system: str | None = None,
        max_messages: int | None = None,
        max_tokens: int | None = None,
        model: str | None = None,
    ) -> Conversation:
        """
        Criar uma nova conversa.

        Args:
            system: System prompt opcional
            max_messages: Limite maximo de mensagens no historico (None = sem limite)
            max_tokens: Limite maximo de tokens no historico (None = sem limite)
            model: Modelo para contagem de tokens (usa default se nao especificado)

        Returns:
            Conversation configurada com este client
        """
        if self._provider is None:
            raise RuntimeError("Cliente nao configurado")
        return Conversation(
            client=self,
            system=system,
            max_messages=max_messages,
            max_tokens=max_tokens,
            model=model or self._default_model,
        )

    async def chat(
        self,
        message: str | list[Message],
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int | None = None,
        tools: list[dict[str, Any]] | None = None,
        **kwargs: Any,
    ) -> ChatResponse:
        """
        Enviar mensagem e receber resposta.

        Args:
            message: Mensagem (str) ou lista de Messages
            model: Modelo a usar
            temperature: Temperatura (0-2)
            max_tokens: Maximo de tokens
            tools: Lista de tools

        Returns:
            ChatResponse
        """
        if self._provider is None:
            raise RuntimeError("Cliente nao configurado")

        messages = self._normalize_messages(message)
        request_id = self._generate_request_id()
        start_time = time.perf_counter()

        # Emitir evento de início
        await self._emit_chat_start(
            request_id=request_id,
            model=model,
            messages=messages,
            tools=tools,
        )

        async def _do_chat() -> ChatResponse:
            return await self._provider.chat(  # type: ignore[union-attr]
                messages=messages,
                model=model or self._default_model,
                temperature=temperature,
                max_tokens=max_tokens,
                tools=tools,
                **kwargs,
            )

        try:
            response: ChatResponse
            if self._retry_config is not None:
                response = await with_retry(
                    _do_chat,
                    self._retry_config,
                    self._provider.provider_name,
                )
            else:
                response = await _do_chat()

            # Emitir evento de conclusão
            latency_ms = (time.perf_counter() - start_time) * 1000
            await self._emit_chat_complete(
                request_id=request_id,
                response=response,
                latency_ms=latency_ms,
            )

            return response

        except Exception as e:
            # Emitir evento de erro
            latency_ms = (time.perf_counter() - start_time) * 1000
            await self._emit_chat_error(
                request_id=request_id,
                error=e,
                latency_ms=latency_ms,
            )
            raise

    async def chat_stream(
        self,
        message: str | list[Message],
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int | None = None,
        tools: list[dict[str, Any]] | None = None,
        **kwargs: Any,
    ) -> AsyncIterator[dict[str, Any]]:
        """
        Enviar mensagem e receber resposta em streaming.

        Yields:
            Chunks de resposta
        """
        if self._provider is None:
            raise RuntimeError("Cliente nao configurado")

        messages = self._normalize_messages(message)

        async for chunk in self._provider.chat_stream(
            messages=messages,
            model=model or self._default_model,
            temperature=temperature,
            max_tokens=max_tokens,
            tools=tools,
            **kwargs,
        ):
            yield chunk

    def _normalize_messages(self, message: str | list[Message]) -> list[Message]:
        """Normalizar input para lista de Messages."""
        if isinstance(message, str):
            if not message.strip():
                raise ValidationError("Mensagem nao pode ser vazia")
            return [Message(role="user", content=message)]
        if not message:
            raise ValidationError("Lista de mensagens nao pode ser vazia")
        return message

    async def close(self) -> None:
        """Fechar conexoes."""
        if self._provider and hasattr(self._provider, "close"):
            await self._provider.close()

    # Métodos auxiliares de observabilidade

    def _generate_request_id(self) -> str:
        """Gerar ID único para request."""
        from uuid import uuid4

        return f"req_{uuid4().hex[:12]}"

    async def _emit_chat_start(
        self,
        request_id: str,
        model: str | None,
        messages: list[Message],
        tools: list[dict[str, Any]] | None,
    ) -> None:
        """Emitir evento de início de chat."""
        if self._observability is None:
            return

        from forge_llm.observability.events import ChatStartEvent

        event = ChatStartEvent(
            timestamp=datetime.now(),
            request_id=request_id,
            provider=self._provider.provider_name,  # type: ignore
            model=model or self._default_model,
            message_count=len(messages),
            has_tools=bool(tools),
        )
        await self._observability.emit(event)

    async def _emit_chat_complete(
        self,
        request_id: str,
        response: ChatResponse,
        latency_ms: float,
    ) -> None:
        """Emitir evento de conclusão de chat."""
        if self._observability is None:
            return

        from forge_llm.observability.events import ChatCompleteEvent

        event = ChatCompleteEvent(
            timestamp=datetime.now(),
            request_id=request_id,
            provider=response.provider,
            model=response.model,
            latency_ms=latency_ms,
            token_usage=response.usage,
            finish_reason=response.finish_reason,
            tool_calls_count=len(response.tool_calls),
        )
        await self._observability.emit(event)

    async def _emit_chat_error(
        self,
        request_id: str,
        error: Exception,
        latency_ms: float,
    ) -> None:
        """Emitir evento de erro de chat."""
        if self._observability is None:
            return

        from forge_llm.observability.events import ChatErrorEvent

        # Determinar se erro é retryable
        retryable = False
        if hasattr(error, "retryable"):
            retryable = getattr(error, "retryable", False)

        event = ChatErrorEvent(
            timestamp=datetime.now(),
            request_id=request_id,
            provider=self._provider.provider_name if self._provider else "unknown",
            error_type=type(error).__name__,
            error_message=str(error),
            latency_ms=latency_ms,
            retryable=retryable,
        )
        await self._observability.emit(event)
