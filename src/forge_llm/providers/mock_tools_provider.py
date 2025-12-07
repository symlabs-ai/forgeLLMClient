"""Mock Tools Provider para testes de tool calling."""

import uuid
from collections.abc import AsyncIterator
from typing import Any

from forge_llm.application.ports.provider_port import ProviderPort
from forge_llm.domain.entities import ChatResponse, ToolCall
from forge_llm.domain.value_objects import (
    Message,
    ResponseFormat,
    TokenUsage,
    ToolDefinition,
)


class MockToolsProvider(ProviderPort):
    """
    Provider mock para testes de tool calling.

    Simula comportamento de providers reais com suporte a tools,
    permitindo configurar quais tools serao chamadas nas respostas.
    """

    def __init__(
        self,
        model: str = "mock-tools-model",
    ) -> None:
        """
        Inicializar MockToolsProvider.

        Args:
            model: Nome do modelo mock
        """
        self._model = model
        self._tools: list[ToolDefinition] = []
        self._next_tool_calls: list[str] = []
        self._next_tool_arguments: dict[str, Any] = {}
        self._call_count = 0

    @property
    def provider_name(self) -> str:
        """Nome identificador do provedor."""
        return "mock-tools"

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
    def tools(self) -> list[ToolDefinition]:
        """Lista de tools registradas."""
        return self._tools.copy()

    @property
    def call_count(self) -> int:
        """Numero de chamadas feitas ao provider."""
        return self._call_count

    def register_tool(self, tool: ToolDefinition) -> None:
        """
        Registrar uma tool.

        Args:
            tool: Definicao da tool
        """
        self._tools.append(tool)

    def has_tool(self, name: str) -> bool:
        """
        Verificar se tool esta registrada.

        Args:
            name: Nome da tool

        Returns:
            True se tool existe
        """
        return any(t.name == name for t in self._tools)

    def set_next_tool_calls(self, tool_names: list[str]) -> None:
        """
        Configurar quais tools serao chamadas na proxima resposta.

        Args:
            tool_names: Lista de nomes de tools a chamar
        """
        self._next_tool_calls = tool_names

    def set_next_tool_arguments(self, arguments: dict[str, Any]) -> None:
        """
        Configurar argumentos para proximo tool call.

        Args:
            arguments: Argumentos a incluir no tool call
        """
        self._next_tool_arguments = arguments

    def reset(self) -> None:
        """Resetar estado do provider."""
        self._tools.clear()
        self._next_tool_calls.clear()
        self._next_tool_arguments.clear()
        self._call_count = 0

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
        Retornar resposta mock com tool calls.

        Se tools estao registradas e nenhum tool call especifico foi
        configurado, retorna tool call para a primeira tool registrada.

        Args:
            messages: Lista de mensagens
            model: Modelo a usar
            temperature: Ignorado pelo mock
            max_tokens: Ignorado pelo mock
            tools: Ignorado (usa tools registradas)

        Returns:
            ChatResponse com tool_calls quando aplicavel
        """
        self._call_count += 1

        # Determinar quais tools chamar
        tool_calls_to_make: list[str] = []
        if self._next_tool_calls:
            tool_calls_to_make = self._next_tool_calls.copy()
            self._next_tool_calls.clear()
        elif self._tools:
            # Se tem tools registradas mas nenhuma especifica, chama a primeira
            tool_calls_to_make = [self._tools[0].name]

        # Criar tool calls
        tool_calls: list[ToolCall] = []
        for tool_name in tool_calls_to_make:
            if self.has_tool(tool_name):
                tool_calls.append(
                    ToolCall(
                        name=tool_name,
                        arguments=self._next_tool_arguments.copy() or {},
                        id=f"tc_{uuid.uuid4().hex[:8]}",
                    )
                )

        # Limpar argumentos apos uso
        self._next_tool_arguments.clear()

        # Conteudo vazio se ha tool calls, senao resposta padrao
        content = "" if tool_calls else "Mock response without tools"

        return ChatResponse(
            content=content,
            model=model or self._model,
            provider=self.provider_name,
            usage=TokenUsage(
                prompt_tokens=10,
                completion_tokens=20,
            ),
            tool_calls=tool_calls,
            finish_reason="tool_calls" if tool_calls else "stop",
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
        Stream mock (simplificado).

        Para tool calling, streaming geralmente nao e usado,
        mas implementamos para conformidade com a interface.
        """
        self._call_count += 1
        yield {
            "delta": {"content": "Mock stream response"},
            "finish_reason": "stop",
        }
