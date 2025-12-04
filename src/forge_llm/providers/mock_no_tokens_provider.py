"""Mock Provider sem informacao de tokens."""

from collections.abc import AsyncIterator
from typing import Any

from forge_llm.application.ports.provider_port import ProviderPort
from forge_llm.domain.entities import ChatResponse
from forge_llm.domain.value_objects import Message, TokenUsage


class MockNoTokensProvider(ProviderPort):
    """
    Provider mock que retorna tokens zerados.

    Util para testar comportamento quando provider nao informa tokens.
    """

    def __init__(
        self,
        default_response: str = "Mock response",
        model: str = "mock-no-tokens-model",
    ) -> None:
        """Inicializar MockNoTokensProvider."""
        self._default_response = default_response
        self._model = model

    @property
    def provider_name(self) -> str:
        """Nome identificador do provedor."""
        return "mock-no-tokens"

    @property
    def supports_streaming(self) -> bool:
        """Indica se provedor suporta streaming."""
        return True

    @property
    def supports_tool_calling(self) -> bool:
        """Indica se provedor suporta tool calling nativo."""
        return False

    @property
    def default_model(self) -> str:
        """Modelo padrao do provedor."""
        return self._model

    async def chat(
        self,
        messages: list[Message],
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int | None = None,
        tools: list[dict[str, Any]] | None = None,
        **kwargs: Any,
    ) -> ChatResponse:
        """Retornar resposta mock sem tokens."""
        return ChatResponse(
            content=self._default_response,
            model=model or self._model,
            provider=self.provider_name,
            usage=TokenUsage(
                prompt_tokens=0,
                completion_tokens=0,
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
        **kwargs: Any,
    ) -> AsyncIterator[dict[str, Any]]:
        """Stream mock que retorna chunks simulados."""
        words = self._default_response.split()
        for i, word in enumerate(words):
            is_last = i == len(words) - 1
            yield {
                "delta": {"content": word + (" " if not is_last else "")},
                "finish_reason": "stop" if is_last else None,
            }
