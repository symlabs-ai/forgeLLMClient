"""OpenRouter Provider - Acesso a 400+ modelos LLM via API unificada."""

import json
import warnings
from collections.abc import AsyncIterator
from typing import Any

from openai import (
    AsyncOpenAI,
)
from openai import (
    AuthenticationError as OpenAIAuthError,
)
from openai import (
    RateLimitError as OpenAIRateLimitError,
)

from forge_llm.application.ports.provider_port import ProviderPort
from forge_llm.domain.entities import ChatResponse, ToolCall
from forge_llm.domain.exceptions import AuthenticationError, RateLimitError
from forge_llm.domain.value_objects import (
    ImageContent,
    Message,
    ResponseFormat,
    TokenUsage,
)

# Constantes
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_MODEL = "openai/gpt-4o-mini"


class OpenRouterProvider(ProviderPort):
    """
    Provider para OpenRouter.

    OpenRouter oferece acesso a 400+ modelos LLM atraves de uma
    API unificada compativel com OpenAI Chat Completions.

    Exemplo:
        provider = OpenRouterProvider(
            api_key="sk-or-...",
            model="openai/gpt-4o-mini",
            site_url="https://myapp.com",
            site_name="My App",
        )
        response = await provider.chat([
            Message(role="user", content="Hello!")
        ])
    """

    def __init__(
        self,
        api_key: str,
        model: str = DEFAULT_MODEL,
        site_url: str | None = None,
        site_name: str | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Inicializar OpenRouterProvider.

        Args:
            api_key: API key do OpenRouter
            model: Modelo padrao (formato: provider/model)
            site_url: URL do site para atribuicao (HTTP-Referer)
            site_name: Nome do site para atribuicao (X-Title)
            **kwargs: Argumentos adicionais
        """
        self._api_key = api_key
        self._model = model
        self._site_url = site_url
        self._site_name = site_name

        # Validar formato do modelo
        self._validate_model_format(model)

        # Configurar headers opcionais
        headers: dict[str, str] = {}
        if site_url:
            headers["HTTP-Referer"] = site_url
        if site_name:
            headers["X-Title"] = site_name

        # Inicializar cliente OpenAI com base_url do OpenRouter
        self._client = AsyncOpenAI(
            api_key=api_key,
            base_url=OPENROUTER_BASE_URL,
            default_headers=headers if headers else None,
        )

    def _validate_model_format(self, model: str) -> None:
        """
        Validar formato do modelo OpenRouter.

        OpenRouter espera formato 'provider/model' (ex: 'openai/gpt-4o-mini').
        Emite warning se o formato nao for seguido.

        Args:
            model: Nome do modelo a validar
        """
        if "/" not in model:
            warnings.warn(
                f"Modelo '{model}' nao segue formato OpenRouter (provider/model). "
                f"Exemplo: 'openai/gpt-4o-mini'",
                UserWarning,
                stacklevel=3,
            )

    @property
    def provider_name(self) -> str:
        """Nome identificador do provedor."""
        return "openrouter"

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

    def _convert_messages(
        self, messages: list[Message]
    ) -> list[dict[str, Any]]:
        """
        Converter Message para formato Chat Completions.

        Args:
            messages: Lista de mensagens do dominio

        Returns:
            Lista de mensagens no formato OpenAI Chat Completions
        """
        result: list[dict[str, Any]] = []

        for msg in messages:
            converted: dict[str, Any] = {
                "role": msg.role,
                "content": self._convert_content(msg.content),
            }

            # Adicionar tool_call_id para mensagens de tool
            if msg.role == "tool" and msg.tool_call_id:
                converted["tool_call_id"] = msg.tool_call_id

            result.append(converted)

        return result

    def _convert_content(
        self, content: str | list[str | ImageContent]
    ) -> str | list[dict[str, Any]]:
        """
        Converter conteudo da mensagem.

        Args:
            content: Conteudo simples (str) ou misto (lista)

        Returns:
            Conteudo no formato Chat Completions
        """
        if isinstance(content, str):
            return content

        # Conteudo misto com imagens
        result: list[dict[str, Any]] = []
        for item in content:
            if isinstance(item, str):
                result.append({"type": "text", "text": item})
            elif isinstance(item, ImageContent):
                result.append(self._format_image(item))

        return result

    def _format_image(self, image: ImageContent) -> dict[str, Any]:
        """
        Formatar ImageContent para Chat Completions.

        Args:
            image: Objeto ImageContent

        Returns:
            Dicionario no formato image_url do Chat Completions
        """
        if image.url:
            return {
                "type": "image_url",
                "image_url": {"url": image.url},
            }

        # Base64 - usar data URL
        return {
            "type": "image_url",
            "image_url": {
                "url": f"data:{image.media_type};base64,{image.base64_data}"
            },
        }

    def _convert_response_format(
        self, response_format: ResponseFormat | None
    ) -> dict[str, Any] | None:
        """
        Converter ResponseFormat para formato OpenAI Chat Completions.

        OpenRouter usa a API Chat Completions, que suporta response_format
        no mesmo formato do OpenAI.

        Args:
            response_format: ResponseFormat

        Returns:
            Dict no formato OpenAI Chat Completions ou None
        """
        if response_format is None or response_format.type == "text":
            return None

        if response_format.type == "json_object":
            return {"type": "json_object"}

        # json_schema
        schema_name = response_format.schema_name or "response_schema"
        return {
            "type": "json_schema",
            "json_schema": {
                "name": schema_name,
                "schema": response_format.json_schema,
                "strict": response_format.strict,
            },
        }

    def _parse_tool_calls(
        self, tool_calls: list[Any] | None
    ) -> list[ToolCall]:
        """
        Parsear tool calls da resposta.

        Args:
            tool_calls: Lista de tool calls da API

        Returns:
            Lista de ToolCall do dominio
        """
        if not tool_calls:
            return []

        result: list[ToolCall] = []
        for tc in tool_calls:
            try:
                arguments = json.loads(tc.function.arguments)
            except (json.JSONDecodeError, AttributeError, TypeError):
                arguments = {}

            result.append(
                ToolCall(
                    id=tc.id,
                    name=tc.function.name,
                    arguments=arguments,
                )
            )

        return result

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
        Enviar mensagens e receber resposta.

        Args:
            messages: Lista de mensagens
            model: Modelo a usar (formato: provider/model)
            temperature: Temperatura de amostragem (0.0-2.0)
            max_tokens: Maximo de tokens na resposta
            tools: Definicoes de ferramentas
            response_format: Formato de resposta estruturada
            **kwargs: Argumentos adicionais para a API

        Returns:
            ChatResponse com a resposta do modelo

        Raises:
            AuthenticationError: Se a API key for invalida
            RateLimitError: Se exceder limite de requisicoes
        """
        try:
            # Construir parametros da requisicao
            request_params: dict[str, Any] = {
                "model": model or self._model,
                "messages": self._convert_messages(messages),
                "temperature": temperature,
            }

            if max_tokens is not None:
                request_params["max_tokens"] = max_tokens

            if tools:
                request_params["tools"] = tools

            # Adicionar response_format se especificado
            converted_format = self._convert_response_format(response_format)
            if converted_format:
                request_params["response_format"] = converted_format

            # Adicionar kwargs extras
            request_params.update(kwargs)

            # Fazer chamada
            response = await self._client.chat.completions.create(
                **request_params
            )

            # Extrair conteudo
            choice = response.choices[0] if response.choices else None
            content = choice.message.content if choice else ""
            tool_calls = self._parse_tool_calls(
                choice.message.tool_calls if choice else None
            )
            finish_reason = choice.finish_reason if choice else "stop"

            # Extrair usage
            usage = response.usage
            prompt_tokens = usage.prompt_tokens if usage else 0
            completion_tokens = usage.completion_tokens if usage else 0

            return ChatResponse(
                content=content or "",
                model=response.model,
                provider=self.provider_name,
                usage=TokenUsage(
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                ),
                tool_calls=tool_calls,
                finish_reason=finish_reason or "stop",
            )

        except OpenAIAuthError as e:
            raise AuthenticationError(
                message=f"OpenRouter authentication failed: {e}",
                provider=self.provider_name,
            ) from e

        except OpenAIRateLimitError as e:
            raise RateLimitError(
                message=f"OpenRouter rate limit exceeded: {e}",
                provider=self.provider_name,
            ) from e

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
        Enviar mensagens e receber resposta em streaming.

        Args:
            messages: Lista de mensagens
            model: Modelo a usar (formato: provider/model)
            temperature: Temperatura de amostragem (0.0-2.0)
            max_tokens: Maximo de tokens na resposta
            tools: Definicoes de ferramentas
            response_format: Formato de resposta estruturada
            **kwargs: Argumentos adicionais para a API

        Yields:
            Chunks de resposta com delta e finish_reason

        Raises:
            AuthenticationError: Se a API key for invalida
            RateLimitError: Se exceder limite de requisicoes
        """
        try:
            # Construir parametros da requisicao
            request_params: dict[str, Any] = {
                "model": model or self._model,
                "messages": self._convert_messages(messages),
                "temperature": temperature,
                "stream": True,
            }

            if max_tokens is not None:
                request_params["max_tokens"] = max_tokens

            if tools:
                request_params["tools"] = tools

            # Adicionar response_format se especificado
            converted_format = self._convert_response_format(response_format)
            if converted_format:
                request_params["response_format"] = converted_format

            # Adicionar kwargs extras
            request_params.update(kwargs)

            # Fazer chamada com streaming
            stream = await self._client.chat.completions.create(
                **request_params
            )

            async for chunk in stream:
                choice = chunk.choices[0] if chunk.choices else None
                delta = choice.delta if choice else None

                yield {
                    "delta": {
                        "content": delta.content or "" if delta else "",
                    },
                    "finish_reason": choice.finish_reason if choice else None,
                }

        except OpenAIAuthError as e:
            raise AuthenticationError(
                message=f"OpenRouter authentication failed: {e}",
                provider=self.provider_name,
            ) from e

        except OpenAIRateLimitError as e:
            raise RateLimitError(
                message=f"OpenRouter rate limit exceeded: {e}",
                provider=self.provider_name,
            ) from e
