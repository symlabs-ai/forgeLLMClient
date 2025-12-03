# LLD — ForgeLLMClient Low Level Design

> **Versao:** 1.0
> **Data:** 2025-12-03
> **Status:** Aprovado

---

## 1. Estrutura de Diretorios

```
src/forge_llm/
├── __init__.py                 # Exports publicos
├── client.py                   # Classe Client (facade)
│
├── domain/                     # CAMADA DE DOMINIO (PURA)
│   ├── __init__.py
│   ├── entities.py             # ChatResponse, ToolCall
│   ├── value_objects.py        # Message, TokenUsage, ToolDefinition
│   └── exceptions.py           # ForgeError, ProviderError, etc.
│
├── application/                # CAMADA DE APLICACAO
│   ├── __init__.py
│   ├── ports/                  # Interfaces (ABC)
│   │   ├── __init__.py
│   │   ├── provider_port.py    # ProviderPort ABC
│   │   ├── config_port.py      # ConfigPort ABC
│   │   └── tool_registry_port.py
│   ├── usecases/               # Casos de uso
│   │   ├── __init__.py
│   │   ├── chat_usecase.py     # ChatUseCase
│   │   ├── stream_usecase.py   # StreamUseCase
│   │   └── tools_usecase.py    # ToolsUseCase
│   └── dtos/                   # Data Transfer Objects
│       ├── __init__.py
│       └── chat_dtos.py        # ChatInput, ChatOutput
│
├── infrastructure/             # CAMADA DE INFRAESTRUTURA
│   ├── __init__.py
│   ├── config.py               # ConfigLoader
│   └── http_client.py          # HTTPClient base (httpx)
│
├── adapters/                   # ADAPTERS
│   ├── __init__.py
│   └── cli/                    # CLI Adapter (futuro)
│       └── __init__.py
│
└── providers/                  # PROVEDORES LLM
    ├── __init__.py
    ├── registry.py             # ProviderRegistry
    ├── openai_provider.py      # OpenAI (Responses API)
    ├── anthropic_provider.py   # Anthropic
    └── mock_provider.py        # Mock (testes)
```

---

## 2. Camada de Dominio

### 2.1 Entidades

```python
# src/forge_llm/domain/entities.py
"""Entidades de dominio do ForgeLLMClient."""

from forgebase.domain import EntityBase
from datetime import datetime
from typing import Optional


class ChatResponse(EntityBase):
    """
    Resposta de chat de um provedor LLM.

    Representa uma resposta completa (nao streaming).
    """

    def __init__(
        self,
        content: str,
        model: str,
        provider: str,
        usage: "TokenUsage",
        tool_calls: list["ToolCall"] | None = None,
        finish_reason: str = "stop",
        id: str | None = None,
        created_at: datetime | None = None,
    ):
        super().__init__(id=id)
        self.content = content
        self.model = model
        self.provider = provider
        self.usage = usage
        self.tool_calls = tool_calls or []
        self.finish_reason = finish_reason
        self.created_at = created_at or datetime.now()
        self.validate()

    def validate(self) -> None:
        """Validar invariantes da resposta."""
        if not self.model:
            raise ValidationError("Modelo e obrigatorio")
        if not self.provider:
            raise ValidationError("Provider e obrigatorio")

    @property
    def has_tool_calls(self) -> bool:
        """Indica se resposta contem tool calls."""
        return len(self.tool_calls) > 0


class ToolCall(EntityBase):
    """
    Chamada de ferramenta solicitada pelo LLM.
    """

    def __init__(
        self,
        name: str,
        arguments: dict,
        id: str | None = None,
    ):
        super().__init__(id=id)
        self.name = name
        self.arguments = arguments
        self.validate()

    def validate(self) -> None:
        if not self.name:
            raise ValidationError("Nome da tool e obrigatorio")
        if not isinstance(self.arguments, dict):
            raise ValidationError("Argumentos devem ser um dicionario")
```

### 2.2 Value Objects

```python
# src/forge_llm/domain/value_objects.py
"""Value Objects do ForgeLLMClient."""

from forgebase.domain import ValueObjectBase, ValidationError
from typing import Literal


class Message(ValueObjectBase):
    """
    Mensagem em uma conversa com LLM.

    Value object imutavel representando uma mensagem.
    """

    def __init__(
        self,
        role: Literal["system", "user", "assistant", "tool"],
        content: str,
        name: str | None = None,
        tool_call_id: str | None = None,
    ):
        super().__init__()
        self.role = role
        self.content = content
        self.name = name
        self.tool_call_id = tool_call_id
        self.validate()
        self._freeze()

    def validate(self) -> None:
        valid_roles = {"system", "user", "assistant", "tool"}
        if self.role not in valid_roles:
            raise ValidationError(f"Role invalido: {self.role}")

        if self.role == "tool" and not self.tool_call_id:
            raise ValidationError("tool_call_id obrigatorio para role 'tool'")

    def to_dict(self) -> dict:
        d = {"role": self.role, "content": self.content}
        if self.name:
            d["name"] = self.name
        if self.tool_call_id:
            d["tool_call_id"] = self.tool_call_id
        return d


class TokenUsage(ValueObjectBase):
    """
    Informacoes de consumo de tokens.
    """

    def __init__(
        self,
        prompt_tokens: int,
        completion_tokens: int,
        total_tokens: int | None = None,
    ):
        super().__init__()
        self.prompt_tokens = prompt_tokens
        self.completion_tokens = completion_tokens
        self.total_tokens = total_tokens or (prompt_tokens + completion_tokens)
        self.validate()
        self._freeze()

    def validate(self) -> None:
        if self.prompt_tokens < 0:
            raise ValidationError("prompt_tokens nao pode ser negativo")
        if self.completion_tokens < 0:
            raise ValidationError("completion_tokens nao pode ser negativo")

    def to_dict(self) -> dict:
        return {
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "total_tokens": self.total_tokens,
        }


class ToolDefinition(ValueObjectBase):
    """
    Definicao de uma ferramenta para tool calling.
    """

    def __init__(
        self,
        name: str,
        description: str,
        parameters: dict,
    ):
        super().__init__()
        self.name = name
        self.description = description
        self.parameters = parameters
        self.validate()
        self._freeze()

    def validate(self) -> None:
        if not self.name:
            raise ValidationError("Nome da tool e obrigatorio")
        if not self.description:
            raise ValidationError("Descricao da tool e obrigatoria")

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters,
        }
```

### 2.3 Excecoes

```python
# src/forge_llm/domain/exceptions.py
"""Excecoes de dominio do ForgeLLMClient."""

from forgebase.domain.exceptions import (
    DomainException,
    ValidationError,
    BusinessRuleViolation,
)


class ForgeError(DomainException):
    """Excecao base do ForgeLLMClient."""
    pass


class ProviderError(ForgeError):
    """Erro ao comunicar com provedor LLM."""

    def __init__(self, message: str, provider: str, status_code: int | None = None):
        super().__init__(message)
        self.provider = provider
        self.status_code = status_code


class AuthenticationError(ForgeError):
    """Erro de autenticacao com provedor."""

    def __init__(self, message: str, provider: str):
        super().__init__(message)
        self.provider = provider


class RateLimitError(ForgeError):
    """Erro de rate limit do provedor."""

    def __init__(self, message: str, provider: str, retry_after: int | None = None):
        super().__init__(message)
        self.provider = provider
        self.retry_after = retry_after


class ConfigurationError(ForgeError):
    """Erro de configuracao."""
    pass


class ToolNotFoundError(ForgeError):
    """Ferramenta nao encontrada."""

    def __init__(self, tool_name: str, available_tools: list[str]):
        super().__init__(f"Tool '{tool_name}' nao encontrada")
        self.tool_name = tool_name
        self.available_tools = available_tools
```

---

## 3. Camada de Aplicacao

### 3.1 Ports (Interfaces)

```python
# src/forge_llm/application/ports/provider_port.py
"""Port abstrato para provedores LLM."""

from abc import ABC, abstractmethod
from typing import AsyncIterator
from forge_llm.domain.entities import ChatResponse
from forge_llm.domain.value_objects import Message


class ProviderPort(ABC):
    """
    Interface para provedores LLM.

    Todos os provedores devem implementar esta interface.
    """

    @abstractmethod
    async def chat(
        self,
        messages: list[Message],
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int | None = None,
        tools: list[dict] | None = None,
        **kwargs,
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
        pass

    @abstractmethod
    async def chat_stream(
        self,
        messages: list[Message],
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int | None = None,
        tools: list[dict] | None = None,
        **kwargs,
    ) -> AsyncIterator["ChatResponseChunk"]:
        """
        Enviar mensagens e receber resposta em streaming.

        Yields:
            ChatResponseChunk com delta de conteudo

        O ultimo chunk contem finish_reason e usage.
        """
        pass

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Nome identificador do provedor."""
        pass

    @property
    @abstractmethod
    def supports_streaming(self) -> bool:
        """Indica se provedor suporta streaming."""
        pass

    @property
    @abstractmethod
    def supports_tool_calling(self) -> bool:
        """Indica se provedor suporta tool calling nativo."""
        pass

    @property
    @abstractmethod
    def default_model(self) -> str:
        """Modelo padrao do provedor."""
        pass
```

### 3.2 DTOs

```python
# src/forge_llm/application/dtos/chat_dtos.py
"""DTOs para operacoes de chat."""

from forgebase.application import DTOBase
from forge_llm.domain.value_objects import Message


class ChatInput(DTOBase):
    """Input para operacao de chat."""

    def __init__(
        self,
        messages: list[Message],
        provider: str | None = None,
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int | None = None,
        stream: bool = False,
        tools: list[dict] | None = None,
    ):
        self.messages = messages
        self.provider = provider
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.stream = stream
        self.tools = tools

    def validate(self) -> None:
        if not self.messages:
            raise ValueError("Pelo menos uma mensagem e obrigatoria")
        if self.temperature < 0 or self.temperature > 2:
            raise ValueError("Temperature deve estar entre 0 e 2")

    def to_dict(self) -> dict:
        return {
            "messages": [m.to_dict() for m in self.messages],
            "provider": self.provider,
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "stream": self.stream,
            "tools": self.tools,
        }


class ChatOutput(DTOBase):
    """Output da operacao de chat."""

    def __init__(
        self,
        content: str,
        model: str,
        provider: str,
        prompt_tokens: int,
        completion_tokens: int,
        total_tokens: int,
        finish_reason: str,
        tool_calls: list[dict] | None = None,
    ):
        self.content = content
        self.model = model
        self.provider = provider
        self.prompt_tokens = prompt_tokens
        self.completion_tokens = completion_tokens
        self.total_tokens = total_tokens
        self.finish_reason = finish_reason
        self.tool_calls = tool_calls

    def validate(self) -> None:
        pass

    def to_dict(self) -> dict:
        return {
            "content": self.content,
            "model": self.model,
            "provider": self.provider,
            "usage": {
                "prompt_tokens": self.prompt_tokens,
                "completion_tokens": self.completion_tokens,
                "total_tokens": self.total_tokens,
            },
            "finish_reason": self.finish_reason,
            "tool_calls": self.tool_calls,
        }
```

### 3.3 UseCases

```python
# src/forge_llm/application/usecases/chat_usecase.py
"""UseCase para chat sync."""

from forgebase.application import UseCaseBase
from forge_llm.application.dtos.chat_dtos import ChatInput, ChatOutput
from forge_llm.application.ports.provider_port import ProviderPort


class ChatUseCase(UseCaseBase):
    """
    Executar chat com LLM.

    Orquestra:
    1. Validar input
    2. Obter provider
    3. Enviar mensagens
    4. Normalizar resposta
    5. Retornar output
    """

    def __init__(
        self,
        provider: ProviderPort,
        logger=None,
        metrics=None,
    ):
        self.provider = provider
        self.logger = logger
        self.metrics = metrics

    async def execute(self, input_dto: ChatInput) -> ChatOutput:
        """Executar chat."""
        # 1. Validar
        input_dto.validate()

        # 2. Log
        if self.logger:
            self.logger.info(
                "Chat request",
                provider=self.provider.provider_name,
                model=input_dto.model,
                messages_count=len(input_dto.messages),
            )

        # 3. Executar
        try:
            response = await self.provider.chat(
                messages=input_dto.messages,
                model=input_dto.model,
                temperature=input_dto.temperature,
                max_tokens=input_dto.max_tokens,
                tools=input_dto.tools,
            )

            # 4. Metricas
            if self.metrics:
                self.metrics.increment(
                    "chat.success",
                    provider=self.provider.provider_name,
                )
                self.metrics.gauge(
                    "chat.tokens",
                    response.usage.total_tokens,
                    provider=self.provider.provider_name,
                )

            # 5. Retornar output
            return ChatOutput(
                content=response.content,
                model=response.model,
                provider=response.provider,
                prompt_tokens=response.usage.prompt_tokens,
                completion_tokens=response.usage.completion_tokens,
                total_tokens=response.usage.total_tokens,
                finish_reason=response.finish_reason,
                tool_calls=[tc.to_dict() for tc in response.tool_calls],
            )

        except Exception as e:
            if self.logger:
                self.logger.error(
                    "Chat failed",
                    provider=self.provider.provider_name,
                    error=str(e),
                )
            if self.metrics:
                self.metrics.increment(
                    "chat.error",
                    provider=self.provider.provider_name,
                )
            raise
```

---

## 4. Provedores

### 4.1 OpenAI Provider

```python
# src/forge_llm/providers/openai_provider.py
"""Provedor OpenAI usando Responses API."""

import httpx
from typing import AsyncIterator
from forge_llm.application.ports.provider_port import ProviderPort
from forge_llm.domain.entities import ChatResponse, ToolCall
from forge_llm.domain.value_objects import Message, TokenUsage
from forge_llm.domain.exceptions import ProviderError, AuthenticationError, RateLimitError


class OpenAIProvider(ProviderPort):
    """
    Provedor OpenAI usando Responses API.

    IMPORTANTE: Usa APENAS Responses API, NUNCA ChatCompletions.
    """

    BASE_URL = "https://api.openai.com/v1"
    DEFAULT_MODEL = "gpt-4"

    def __init__(
        self,
        api_key: str,
        base_url: str | None = None,
        timeout: float = 60.0,
    ):
        self.api_key = api_key
        self.base_url = base_url or self.BASE_URL
        self.timeout = timeout
        self._client: httpx.AsyncClient | None = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(
                timeout=httpx.Timeout(self.timeout),
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
            )
        return self._client

    @property
    def provider_name(self) -> str:
        return "openai"

    @property
    def supports_streaming(self) -> bool:
        return True

    @property
    def supports_tool_calling(self) -> bool:
        return True

    @property
    def default_model(self) -> str:
        return self.DEFAULT_MODEL

    async def chat(
        self,
        messages: list[Message],
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int | None = None,
        tools: list[dict] | None = None,
        **kwargs,
    ) -> ChatResponse:
        """Enviar chat usando Responses API."""
        client = await self._get_client()

        payload = {
            "model": model or self.default_model,
            "input": [m.to_dict() for m in messages],
            "temperature": temperature,
        }

        if max_tokens:
            payload["max_output_tokens"] = max_tokens

        if tools:
            payload["tools"] = tools

        try:
            response = await client.post(
                f"{self.base_url}/responses",
                json=payload,
            )

            if response.status_code == 401:
                raise AuthenticationError(
                    "API key invalida",
                    provider=self.provider_name,
                )

            if response.status_code == 429:
                retry_after = response.headers.get("Retry-After")
                raise RateLimitError(
                    "Rate limit excedido",
                    provider=self.provider_name,
                    retry_after=int(retry_after) if retry_after else None,
                )

            if response.status_code != 200:
                raise ProviderError(
                    f"Erro OpenAI: {response.text}",
                    provider=self.provider_name,
                    status_code=response.status_code,
                )

            data = response.json()
            return self._parse_response(data)

        except httpx.RequestError as e:
            raise ProviderError(
                f"Erro de conexao: {str(e)}",
                provider=self.provider_name,
            )

    async def chat_stream(
        self,
        messages: list[Message],
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int | None = None,
        tools: list[dict] | None = None,
        **kwargs,
    ) -> AsyncIterator:
        """Streaming usando Responses API."""
        client = await self._get_client()

        payload = {
            "model": model or self.default_model,
            "input": [m.to_dict() for m in messages],
            "temperature": temperature,
            "stream": True,
        }

        if max_tokens:
            payload["max_output_tokens"] = max_tokens

        async with client.stream(
            "POST",
            f"{self.base_url}/responses",
            json=payload,
        ) as response:
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    data = line[6:]
                    if data == "[DONE]":
                        break
                    yield self._parse_chunk(data)

    def _parse_response(self, data: dict) -> ChatResponse:
        """Parse resposta da Responses API."""
        output = data.get("output", [{}])[0]
        usage = data.get("usage", {})

        tool_calls = []
        if "tool_calls" in output:
            for tc in output["tool_calls"]:
                tool_calls.append(
                    ToolCall(
                        id=tc.get("id"),
                        name=tc.get("name"),
                        arguments=tc.get("arguments", {}),
                    )
                )

        return ChatResponse(
            id=data.get("id"),
            content=output.get("content", ""),
            model=data.get("model"),
            provider=self.provider_name,
            usage=TokenUsage(
                prompt_tokens=usage.get("input_tokens", 0),
                completion_tokens=usage.get("output_tokens", 0),
            ),
            tool_calls=tool_calls,
            finish_reason=output.get("finish_reason", "stop"),
        )

    def _parse_chunk(self, data: str):
        """Parse chunk de streaming."""
        import json
        chunk = json.loads(data)
        # Implementar parsing de chunks
        return chunk

    async def close(self):
        """Fechar cliente HTTP."""
        if self._client:
            await self._client.aclose()
            self._client = None
```

### 4.2 Anthropic Provider

```python
# src/forge_llm/providers/anthropic_provider.py
"""Provedor Anthropic."""

import httpx
from typing import AsyncIterator
from forge_llm.application.ports.provider_port import ProviderPort
from forge_llm.domain.entities import ChatResponse
from forge_llm.domain.value_objects import Message, TokenUsage


class AnthropicProvider(ProviderPort):
    """Provedor Anthropic Claude."""

    BASE_URL = "https://api.anthropic.com/v1"
    DEFAULT_MODEL = "claude-3-5-sonnet-20241022"

    def __init__(
        self,
        api_key: str,
        base_url: str | None = None,
        timeout: float = 60.0,
    ):
        self.api_key = api_key
        self.base_url = base_url or self.BASE_URL
        self.timeout = timeout
        self._client: httpx.AsyncClient | None = None

    @property
    def provider_name(self) -> str:
        return "anthropic"

    @property
    def supports_streaming(self) -> bool:
        return True

    @property
    def supports_tool_calling(self) -> bool:
        return True

    @property
    def default_model(self) -> str:
        return self.DEFAULT_MODEL

    async def chat(
        self,
        messages: list[Message],
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int | None = None,
        tools: list[dict] | None = None,
        **kwargs,
    ) -> ChatResponse:
        """Enviar chat para Anthropic."""
        # Implementar
        pass

    async def chat_stream(
        self,
        messages: list[Message],
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int | None = None,
        tools: list[dict] | None = None,
        **kwargs,
    ) -> AsyncIterator:
        """Streaming Anthropic."""
        # Implementar
        pass
```

### 4.3 Mock Provider

```python
# src/forge_llm/providers/mock_provider.py
"""Mock Provider para testes."""

from typing import AsyncIterator
from forge_llm.application.ports.provider_port import ProviderPort
from forge_llm.domain.entities import ChatResponse
from forge_llm.domain.value_objects import Message, TokenUsage


class MockProvider(ProviderPort):
    """
    Provider mock para testes.

    Permite configurar respostas pre-definidas.
    """

    def __init__(
        self,
        default_response: str = "Mock response",
        model: str = "mock-model",
    ):
        self._default_response = default_response
        self._model = model
        self._responses: list[str] = []
        self._call_count = 0

    @property
    def provider_name(self) -> str:
        return "mock"

    @property
    def supports_streaming(self) -> bool:
        return True

    @property
    def supports_tool_calling(self) -> bool:
        return True

    @property
    def default_model(self) -> str:
        return self._model

    def set_response(self, response: str) -> None:
        """Configurar proxima resposta."""
        self._responses.append(response)

    def set_responses(self, responses: list[str]) -> None:
        """Configurar multiplas respostas."""
        self._responses.extend(responses)

    @property
    def call_count(self) -> int:
        """Numero de chamadas feitas."""
        return self._call_count

    async def chat(
        self,
        messages: list[Message],
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int | None = None,
        tools: list[dict] | None = None,
        **kwargs,
    ) -> ChatResponse:
        """Retornar resposta mock."""
        self._call_count += 1

        content = (
            self._responses.pop(0)
            if self._responses
            else self._default_response
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
        tools: list[dict] | None = None,
        **kwargs,
    ) -> AsyncIterator:
        """Stream mock."""
        self._call_count += 1

        content = (
            self._responses.pop(0)
            if self._responses
            else self._default_response
        )

        # Simular chunks
        words = content.split()
        for i, word in enumerate(words):
            yield {
                "delta": {"content": word + " "},
                "finish_reason": None if i < len(words) - 1 else "stop",
            }
```

---

## 5. Cliente Principal (Facade)

```python
# src/forge_llm/client.py
"""Cliente principal do ForgeLLMClient."""

from typing import AsyncIterator
from forge_llm.domain.entities import ChatResponse
from forge_llm.domain.value_objects import Message
from forge_llm.application.ports.provider_port import ProviderPort
from forge_llm.providers.registry import ProviderRegistry


class Client:
    """
    Cliente principal do ForgeLLMClient.

    Facade que simplifica uso do SDK.

    Exemplo:
        client = Client(provider="openai", api_key="sk-...")
        response = await client.chat("Ola!")
        print(response.content)
    """

    def __init__(
        self,
        provider: str | ProviderPort,
        api_key: str | None = None,
        model: str | None = None,
        **kwargs,
    ):
        if isinstance(provider, str):
            self._provider = ProviderRegistry.create(
                provider,
                api_key=api_key,
                **kwargs,
            )
        else:
            self._provider = provider

        self._default_model = model

    async def chat(
        self,
        message: str | list[Message],
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int | None = None,
        tools: list[dict] | None = None,
        **kwargs,
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
        messages = self._normalize_messages(message)

        return await self._provider.chat(
            messages=messages,
            model=model or self._default_model,
            temperature=temperature,
            max_tokens=max_tokens,
            tools=tools,
            **kwargs,
        )

    async def chat_stream(
        self,
        message: str | list[Message],
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int | None = None,
        tools: list[dict] | None = None,
        **kwargs,
    ) -> AsyncIterator:
        """
        Enviar mensagem e receber resposta em streaming.

        Yields:
            Chunks de resposta
        """
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
            return [Message(role="user", content=message)]
        return message

    @property
    def provider_name(self) -> str:
        """Nome do provedor atual."""
        return self._provider.provider_name

    async def close(self):
        """Fechar conexoes."""
        if hasattr(self._provider, "close"):
            await self._provider.close()
```

---

## 6. Referencias

- `specs/roadmap/HLD.md`
- `specs/roadmap/ARCHITECTURAL_DECISIONS_APPROVED.md`
- `docs/guides/forgebase_guides/usuarios/receitas.md`
- `docs/guides/forgebase_guides/usuarios/forgebase-rules.md`

---

*Documento gerado pelo Roadmap Planning Process*
