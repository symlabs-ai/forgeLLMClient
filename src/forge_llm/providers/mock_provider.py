"""Mock Provider para testes."""

from collections.abc import AsyncIterator
from typing import Any

from forge_llm.application.ports.provider_port import ProviderPort
from forge_llm.domain.entities import ChatResponse
from forge_llm.domain.value_objects import Message, ResponseFormat, TokenUsage


class MockProvider(ProviderPort):
    """
    Provider mock para testes.

    Permite configurar respostas pre-definidas para simular
    comportamento de provedores reais sem fazer chamadas de API.
    Suporta mensagens com imagens para testes de vision.
    """

    def __init__(
        self,
        default_response: str = "Mock response",
        model: str = "mock-model",
    ) -> None:
        """
        Inicializar MockProvider.

        Args:
            default_response: Resposta padrao quando nenhuma especifica
            model: Nome do modelo mock
        """
        self._default_response = default_response
        self._model = model
        self._responses: list[str] = []
        self._call_count = 0
        self._last_messages: list[Message] = []
        self._images_received: int = 0

    @property
    def provider_name(self) -> str:
        """Nome identificador do provedor."""
        return "mock"

    @property
    def supports_streaming(self) -> bool:
        """Indica se provedor suporta streaming."""
        return True

    @property
    def supports_tool_calling(self) -> bool:
        """Indica se provedor suporta tool calling nativo."""
        return True

    @property
    def default_model(self) -> str:
        """Modelo padrao do provedor."""
        return self._model

    @property
    def call_count(self) -> int:
        """Numero de chamadas feitas ao provider."""
        return self._call_count

    @property
    def last_messages(self) -> list[Message]:
        """Ultimas mensagens recebidas."""
        return self._last_messages

    @property
    def images_received(self) -> int:
        """Numero de imagens recebidas na ultima chamada."""
        return self._images_received

    def _count_images(self, messages: list[Message]) -> int:
        """Contar imagens nas mensagens."""
        count = 0
        for msg in messages:
            if msg.has_images:
                count += len(msg.images)
        return count

    def set_response(self, response: str) -> None:
        """
        Configurar proxima resposta.

        Args:
            response: Conteudo da resposta
        """
        self._responses.append(response)

    def set_responses(self, responses: list[str]) -> None:
        """
        Configurar multiplas respostas em sequencia.

        Args:
            responses: Lista de conteudos de resposta
        """
        self._responses.extend(responses)

    def reset(self) -> None:
        """Resetar estado do provider."""
        self._responses.clear()
        self._call_count = 0
        self._last_messages = []
        self._images_received = 0

    async def chat(
        self,
        messages: list[Message],
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int | None = None,
        tools: list[dict[str, Any]] | None = None,
        response_format: ResponseFormat | None = None,
        **kwargs: Any,
    ) -> ChatResponse:
        """
        Retornar resposta mock.

        Args:
            messages: Lista de mensagens (ignoradas pelo mock)
            model: Modelo a usar
            temperature: Ignorado pelo mock
            max_tokens: Ignorado pelo mock
            tools: Ignorado pelo mock

        Returns:
            ChatResponse com conteudo mock
        """
        self._call_count += 1
        self._last_messages = messages
        self._images_received = self._count_images(messages)

        content = (
            self._responses.pop(0) if self._responses else self._default_response
        )

        return ChatResponse(
            content=content,
            model=model or self._model,
            provider=self.provider_name,
            usage=TokenUsage(
                prompt_tokens=10,
                completion_tokens=20,
            ),
            finish_reason="stop",
        )

    async def chat_stream(
        self,
        messages: list[Message],
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int | None = None,
        tools: list[dict[str, Any]] | None = None,
        response_format: ResponseFormat | None = None,
        **kwargs: Any,
    ) -> AsyncIterator[dict[str, Any]]:
        """
        Stream mock que retorna chunks simulados.

        Args:
            messages: Lista de mensagens
            model: Modelo a usar
            temperature: Ignorado
            max_tokens: Ignorado
            tools: Ignorado

        Yields:
            Chunks de resposta simulados
        """
        self._call_count += 1

        content = (
            self._responses.pop(0) if self._responses else self._default_response
        )

        # Simular chunks palavra por palavra
        words = content.split()
        for i, word in enumerate(words):
            is_last = i == len(words) - 1
            yield {
                "delta": {"content": word + (" " if not is_last else "")},
                "index": i,
                "finish_reason": "stop" if is_last else None,
            }
