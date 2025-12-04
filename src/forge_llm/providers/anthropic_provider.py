"""Anthropic Provider - Integracao real com API Anthropic."""

from collections.abc import AsyncIterator
from typing import Any

from anthropic import AsyncAnthropic
from anthropic import AuthenticationError as AnthropicAuthError
from anthropic import RateLimitError as AnthropicRateLimitError

from forge_llm.application.ports.provider_port import ProviderPort
from forge_llm.domain.entities import ChatResponse, ToolCall
from forge_llm.domain.exceptions import AuthenticationError, RateLimitError
from forge_llm.domain.value_objects import ImageContent, Message, TokenUsage


class AnthropicProvider(ProviderPort):
    """
    Provider para Anthropic usando a Messages API.

    Integracao completa com API Anthropic via SDK oficial.
    Suporta chat, streaming e tool calling.
    """

    def __init__(
        self,
        api_key: str,
        model: str = "claude-sonnet-4-20250514",
        **kwargs: Any,
    ) -> None:
        """
        Inicializar AnthropicProvider.

        Args:
            api_key: API key da Anthropic
            model: Modelo padrao a usar
            **kwargs: Argumentos adicionais
        """
        self._api_key = api_key
        self._model = model
        self._client = AsyncAnthropic(api_key=api_key)

    @property
    def provider_name(self) -> str:
        """Nome identificador do provedor."""
        return "anthropic"

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

    def _format_image_for_anthropic(self, image: ImageContent) -> dict[str, Any]:
        """
        Formatar ImageContent para Anthropic Messages API.

        Args:
            image: ImageContent

        Returns:
            Dict no formato Anthropic
        """
        if image.url:
            return {
                "type": "image",
                "source": {
                    "type": "url",
                    "url": image.url,
                },
            }
        # Base64
        return {
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": image.media_type,
                "data": image.base64_data,
            },
        }

    def _convert_message_content(
        self, content: str | list[str | ImageContent]
    ) -> str | list[dict[str, Any]]:
        """
        Converter conteudo da mensagem para formato Anthropic.

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
                result.append({"type": "text", "text": item})
            elif isinstance(item, ImageContent):
                result.append(self._format_image_for_anthropic(item))
        return result

    def _convert_messages(
        self, messages: list[Message]
    ) -> tuple[str | None, list[dict[str, Any]]]:
        """
        Converter mensagens para formato da Messages API.

        Args:
            messages: Lista de Message

        Returns:
            Tuple de (system_message, messages_list)
        """
        system_message = None
        result = []

        for msg in messages:
            if msg.role == "system":
                system_message = msg.content if isinstance(msg.content, str) else str(msg.content)
            elif msg.role == "user":
                result.append({
                    "role": "user",
                    "content": self._convert_message_content(msg.content),
                })
            elif msg.role == "assistant":
                result.append({
                    "role": "assistant",
                    "content": self._convert_message_content(msg.content),
                })
            elif msg.role == "tool":
                # Tool results em Anthropic vao como user message com tool_result
                result.append({
                    "role": "user",
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": msg.tool_call_id,
                            "content": msg.content if isinstance(msg.content, str) else str(msg.content),
                        }
                    ],
                })

        return system_message, result

    def _convert_tools_to_anthropic_format(
        self, tools: list[dict[str, Any]] | None
    ) -> list[dict[str, Any]] | None:
        """
        Converter tools do formato OpenAI para formato Anthropic.

        Args:
            tools: Lista de tools no formato OpenAI

        Returns:
            Lista de tools no formato Anthropic
        """
        if not tools:
            return None

        result = []
        for tool in tools:
            if tool.get("type") == "function":
                func = tool.get("function", {})
                result.append({
                    "name": func.get("name"),
                    "description": func.get("description"),
                    "input_schema": func.get("parameters"),
                })
            else:
                result.append(tool)
        return result

    def _parse_response_content(
        self, content: list[Any]
    ) -> tuple[str, list[ToolCall]]:
        """
        Parsear content blocks da resposta.

        Args:
            content: Lista de content blocks

        Returns:
            Tuple de (text_content, tool_calls)
        """
        text_parts = []
        tool_calls = []

        for block in content:
            block_type = getattr(block, "type", None)

            if block_type == "text":
                text_parts.append(getattr(block, "text", ""))
            elif block_type == "tool_use":
                tool_calls.append(
                    ToolCall(
                        id=getattr(block, "id", ""),
                        name=getattr(block, "name", ""),
                        arguments=getattr(block, "input", {}),
                    )
                )

        return "".join(text_parts), tool_calls

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
        Enviar mensagem para Anthropic usando Messages API.

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
            system_message, converted_messages = self._convert_messages(messages)

            request_params: dict[str, Any] = {
                "model": model or self._model,
                "messages": converted_messages,
                "temperature": temperature,
                "max_tokens": max_tokens or 4096,
            }

            if system_message:
                request_params["system"] = system_message

            if tools:
                request_params["tools"] = self._convert_tools_to_anthropic_format(tools)

            response = await self._client.messages.create(**request_params)

            # Parsear resposta
            content, tool_calls = self._parse_response_content(response.content)

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
                finish_reason=response.stop_reason or "end_turn",
            )

        except AnthropicAuthError as e:
            raise AuthenticationError(
                message=f"Anthropic authentication failed: {e}",
                provider=self.provider_name,
            ) from e

        except AnthropicRateLimitError as e:
            raise RateLimitError(
                message=f"Anthropic rate limit exceeded: {e}",
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
        Stream de resposta da Anthropic usando Messages API.

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
            system_message, converted_messages = self._convert_messages(messages)

            request_params: dict[str, Any] = {
                "model": model or self._model,
                "messages": converted_messages,
                "temperature": temperature,
                "max_tokens": max_tokens or 4096,
            }

            if system_message:
                request_params["system"] = system_message

            if tools:
                request_params["tools"] = self._convert_tools_to_anthropic_format(tools)

            async with self._client.messages.stream(**request_params) as stream:
                async for event in stream:
                    event_type = getattr(event, "type", None)

                    if event_type == "content_block_delta":
                        delta = getattr(event, "delta", None)
                        if delta:
                            text = getattr(delta, "text", "")
                            yield {
                                "delta": {"content": text},
                                "finish_reason": None,
                            }
                    elif event_type == "message_stop":
                        yield {
                            "delta": {"content": ""},
                            "finish_reason": "stop",
                        }

        except AnthropicAuthError as e:
            raise AuthenticationError(
                message=f"Anthropic authentication failed: {e}",
                provider=self.provider_name,
            ) from e

        except AnthropicRateLimitError as e:
            raise RateLimitError(
                message=f"Anthropic rate limit exceeded: {e}",
                provider=self.provider_name,
            ) from e
