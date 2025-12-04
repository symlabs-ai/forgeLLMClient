"""Cliente principal do ForgeLLMClient."""

from collections.abc import AsyncIterator
from typing import Any

from forge_llm.application.ports.provider_port import ProviderPort
from forge_llm.domain.entities import ChatResponse, Conversation
from forge_llm.domain.exceptions import ValidationError
from forge_llm.domain.value_objects import Message
from forge_llm.infrastructure.retry import RetryConfig, with_retry
from forge_llm.providers.registry import ProviderRegistry


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
            **kwargs: Argumentos adicionais para o provider
        """
        self._provider: ProviderPort | None = None
        self._default_model = model

        # Configurar retry
        if retry_config is not None:
            self._retry_config = retry_config
        elif max_retries > 0:
            self._retry_config = RetryConfig(
                max_retries=max_retries,
                base_delay=retry_delay,
            )
        else:
            self._retry_config = None

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
    ) -> Conversation:
        """
        Criar uma nova conversa.

        Args:
            system: System prompt opcional
            max_messages: Limite maximo de mensagens no historico (None = sem limite)

        Returns:
            Conversation configurada com este client
        """
        if self._provider is None:
            raise RuntimeError("Cliente nao configurado")
        return Conversation(client=self, system=system, max_messages=max_messages)

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

        async def _do_chat() -> ChatResponse:
            return await self._provider.chat(  # type: ignore[union-attr]
                messages=messages,
                model=model or self._default_model,
                temperature=temperature,
                max_tokens=max_tokens,
                tools=tools,
                **kwargs,
            )

        if self._retry_config is not None:
            return await with_retry(
                _do_chat,
                self._retry_config,
                self._provider.provider_name,
            )
        return await _do_chat()

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
            await self._provider.close()  # type: ignore
