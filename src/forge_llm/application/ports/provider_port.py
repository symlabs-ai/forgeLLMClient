"""Port abstrato para provedores LLM."""

from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from typing import Any

from forge_llm.domain.entities import ChatResponse
from forge_llm.domain.value_objects import Message


class ProviderPort(ABC):
    """
    Interface para provedores LLM.

    Todos os provedores devem implementar esta interface.
    Define contrato para operacoes de chat sync e streaming.
    """

    @abstractmethod
    async def chat(
        self,
        messages: list[Message],
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int | None = None,
        tools: list[dict[str, Any]] | None = None,
        **kwargs: Any,
    ) -> ChatResponse:
        """
        Enviar mensagens e receber resposta completa.

        Args:
            messages: Lista de mensagens da conversa
            model: Modelo a usar (ou default do provider)
            temperature: Temperatura de sampling (0-2)
            max_tokens: Maximo de tokens na resposta
            tools: Lista de tools disponiveis
            **kwargs: Parametros adicionais do provider

        Returns:
            ChatResponse com conteudo, uso de tokens, etc.

        Raises:
            ProviderError: Erro de comunicacao
            AuthenticationError: Credenciais invalidas
            RateLimitError: Rate limit excedido
        """
        ...

    @abstractmethod
    async def chat_stream(
        self,
        messages: list[Message],
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int | None = None,
        tools: list[dict[str, Any]] | None = None,
        **kwargs: Any,
    ) -> AsyncIterator[dict[str, Any]]:
        """
        Enviar mensagens e receber resposta em streaming.

        Args:
            messages: Lista de mensagens da conversa
            model: Modelo a usar (ou default do provider)
            temperature: Temperatura de sampling (0-2)
            max_tokens: Maximo de tokens na resposta
            tools: Lista de tools disponiveis
            **kwargs: Parametros adicionais do provider

        Yields:
            Chunks de resposta com delta de conteudo

        O ultimo chunk contem finish_reason e usage.
        """
        ...
        # Necessario para tipo AsyncIterator
        yield {}  # pragma: no cover

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Nome identificador do provedor."""
        ...

    @property
    @abstractmethod
    def supports_streaming(self) -> bool:
        """Indica se provedor suporta streaming."""
        ...

    @property
    @abstractmethod
    def supports_tool_calling(self) -> bool:
        """Indica se provedor suporta tool calling nativo."""
        ...

    @property
    @abstractmethod
    def default_model(self) -> str:
        """Modelo padrao do provedor."""
        ...
