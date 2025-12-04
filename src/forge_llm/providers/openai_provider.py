"""OpenAI Provider - Integracao real com API OpenAI Responses."""

import json
from collections.abc import AsyncIterator
from typing import Any

from openai import AsyncOpenAI
from openai import AuthenticationError as OpenAIAuthError
from openai import RateLimitError as OpenAIRateLimitError

from forge_llm.application.ports.provider_port import ProviderPort
from forge_llm.domain.entities import ChatResponse, ToolCall
from forge_llm.domain.exceptions import AuthenticationError, RateLimitError
from forge_llm.domain.value_objects import ImageContent, Message, TokenUsage


class OpenAIProvider(ProviderPort):
    """
    Provider para OpenAI usando a Responses API.

    Integracao completa com API OpenAI via SDK oficial.
    Utiliza a nova Responses API (recomendada para agentes).
    Suporta chat, streaming e tool calling.
    """

    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4o-mini",
        **kwargs: Any,
    ) -> None:
        """
        Inicializar OpenAIProvider.

        Args:
            api_key: API key da OpenAI
            model: Modelo padrao a usar
            **kwargs: Argumentos adicionais
        """
        self._api_key = api_key
        self._model = model
        self._client = AsyncOpenAI(api_key=api_key)

    @property
    def provider_name(self) -> str:
        """Nome identificador do provedor."""
        return "openai"

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

    def _format_image_for_openai(self, image: ImageContent) -> dict[str, Any]:
        """
        Formatar ImageContent para OpenAI Responses API.

        Args:
            image: ImageContent

        Returns:
            Dict no formato OpenAI
        """
        if image.url:
            return {
                "type": "input_image",
                "image_url": image.url,
            }
        # Base64: data URL format
        return {
            "type": "input_image",
            "image_url": f"data:{image.media_type};base64,{image.base64_data}",
        }

    def _convert_message_content(
        self, content: str | list[str | ImageContent]
    ) -> str | list[dict[str, Any]]:
        """
        Converter conteudo da mensagem para formato OpenAI.

        Args:
            content: Conteudo string ou lista mista

        Returns:
            String ou lista de content items
        """
        if isinstance(content, str):
            return content

        # Conteudo misto com imagens
        result = []
        for item in content:
            if isinstance(item, str):
                result.append({"type": "input_text", "text": item})
            elif isinstance(item, ImageContent):
                result.append(self._format_image_for_openai(item))
        return result

    def _convert_messages_to_input(
        self, messages: list[Message]
    ) -> list[dict[str, Any]]:
        """
        Converter mensagens para formato de input da Responses API.

        A Responses API aceita input como lista de items.

        Args:
            messages: Lista de Message

        Returns:
            Lista de input items no formato Responses API
        """
        result = []
        for msg in messages:
            if msg.role == "system":
                # System messages sao tratados via instructions
                continue

            if msg.role == "user":
                result.append({
                    "type": "message",
                    "role": "user",
                    "content": self._convert_message_content(msg.content),
                })
            elif msg.role == "assistant":
                result.append({
                    "type": "message",
                    "role": "assistant",
                    "content": self._convert_message_content(msg.content),
                })
            elif msg.role == "tool":
                result.append({
                    "type": "function_call_output",
                    "call_id": msg.tool_call_id,
                    "output": msg.content if isinstance(msg.content, str) else str(msg.content),
                })
        return result

    def _get_system_instruction(self, messages: list[Message]) -> str | None:
        """
        Extrair system instruction das mensagens.

        Args:
            messages: Lista de Message

        Returns:
            System instruction ou None
        """
        for msg in messages:
            if msg.role == "system":
                return msg.content
        return None

    def _convert_tools_to_responses_format(
        self, tools: list[dict[str, Any]] | None
    ) -> list[dict[str, Any]] | None:
        """
        Converter tools do formato Chat Completions para Responses API.

        Args:
            tools: Lista de tools no formato Chat Completions

        Returns:
            Lista de tools no formato Responses API
        """
        if not tools:
            return None

        result = []
        for tool in tools:
            if tool.get("type") == "function":
                func = tool.get("function", {})
                result.append({
                    "type": "function",
                    "name": func.get("name"),
                    "description": func.get("description"),
                    "parameters": func.get("parameters"),
                })
            else:
                # Manter formato original para outros tipos
                result.append(tool)
        return result

    def _parse_response_items(
        self, output: list[Any]
    ) -> tuple[str, list[ToolCall]]:
        """
        Parsear items de resposta da Responses API.

        Args:
            output: Lista de items da resposta

        Returns:
            Tuple de (content, tool_calls)
        """
        content_parts = []
        tool_calls = []

        for item in output:
            item_type = getattr(item, "type", None)

            if item_type == "message":
                # Extrair conteudo da mensagem
                for content_item in getattr(item, "content", []):
                    if getattr(content_item, "type", None) == "output_text":
                        content_parts.append(getattr(content_item, "text", ""))

            elif item_type == "function_call":
                # Extrair tool call
                try:
                    arguments = json.loads(getattr(item, "arguments", "{}"))
                except (json.JSONDecodeError, AttributeError):
                    arguments = {}

                tool_calls.append(
                    ToolCall(
                        id=getattr(item, "call_id", getattr(item, "id", "")),
                        name=getattr(item, "name", ""),
                        arguments=arguments,
                    )
                )

        return "".join(content_parts), tool_calls

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
        Enviar mensagem para OpenAI usando Responses API.

        Args:
            messages: Lista de mensagens
            model: Modelo a usar
            temperature: Temperatura
            max_tokens: Maximo de tokens
            tools: Tools disponiveis

        Returns:
            ChatResponse

        Raises:
            AuthenticationError: Se API key invalida
            RateLimitError: Se rate limit excedido
        """
        try:
            request_params: dict[str, Any] = {
                "model": model or self._model,
                "input": self._convert_messages_to_input(messages),
                "temperature": temperature,
            }

            # Adicionar instructions se houver system message
            instructions = self._get_system_instruction(messages)
            if instructions:
                request_params["instructions"] = instructions

            if max_tokens is not None:
                request_params["max_output_tokens"] = max_tokens

            if tools:
                request_params["tools"] = self._convert_tools_to_responses_format(tools)

            response = await self._client.responses.create(**request_params)

            # Parsear resposta
            content, tool_calls = self._parse_response_items(response.output)

            # Extrair usage
            usage = response.usage
            prompt_tokens = getattr(usage, "input_tokens", 0)
            completion_tokens = getattr(usage, "output_tokens", 0)

            return ChatResponse(
                content=content,
                model=response.model,
                provider=self.provider_name,
                usage=TokenUsage(
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                    total_tokens=prompt_tokens + completion_tokens,
                ),
                tool_calls=tool_calls,
                finish_reason=response.status or "completed",
            )

        except OpenAIAuthError as e:
            raise AuthenticationError(
                message=f"OpenAI authentication failed: {e}",
                provider=self.provider_name,
            ) from e

        except OpenAIRateLimitError as e:
            raise RateLimitError(
                message=f"OpenAI rate limit exceeded: {e}",
                provider=self.provider_name,
            ) from e

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
        Stream de resposta da OpenAI usando Responses API.

        Args:
            messages: Lista de mensagens
            model: Modelo a usar
            temperature: Temperatura
            max_tokens: Maximo de tokens
            tools: Tools disponiveis

        Yields:
            Chunks de resposta
        """
        try:
            request_params: dict[str, Any] = {
                "model": model or self._model,
                "input": self._convert_messages_to_input(messages),
                "temperature": temperature,
                "stream": True,
            }

            # Adicionar instructions se houver system message
            instructions = self._get_system_instruction(messages)
            if instructions:
                request_params["instructions"] = instructions

            if max_tokens is not None:
                request_params["max_output_tokens"] = max_tokens

            if tools:
                request_params["tools"] = self._convert_tools_to_responses_format(tools)

            stream = await self._client.responses.create(**request_params)

            async for event in stream:
                event_type = getattr(event, "type", None)

                if event_type == "response.output_text.delta":
                    yield {
                        "delta": {
                            "content": getattr(event, "delta", ""),
                        },
                        "finish_reason": None,
                    }
                elif event_type == "response.completed":
                    yield {
                        "delta": {
                            "content": "",
                        },
                        "finish_reason": "stop",
                    }

        except OpenAIAuthError as e:
            raise AuthenticationError(
                message=f"OpenAI authentication failed: {e}",
                provider=self.provider_name,
            ) from e

        except OpenAIRateLimitError as e:
            raise RateLimitError(
                message=f"OpenAI rate limit exceeded: {e}",
                provider=self.provider_name,
            ) from e
