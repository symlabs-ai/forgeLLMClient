# Guia: Criando Novos Providers

Este guia explica como criar um novo provider para integrar com diferentes APIs de LLM.

---

## 1. Arquitetura

### 1.1 Estrutura de Arquivos

```
src/forge_llm/
├── application/
│   └── ports/
│       └── provider_port.py      # Interface abstrata
├── providers/
│   ├── __init__.py
│   ├── registry.py               # Registro de providers
│   ├── openai_provider.py        # Exemplo: OpenAI
│   ├── anthropic_provider.py     # Exemplo: Anthropic
│   └── seu_provider.py           # Seu novo provider
└── domain/
    ├── entities.py               # ChatResponse, ToolCall
    ├── value_objects.py          # Message, TokenUsage, ImageContent
    └── exceptions.py             # Excecoes de dominio
```

### 1.2 Diagrama de Dependencias

```
Client --> ProviderPort (interface)
              ^
              |
    +---------+---------+
    |         |         |
OpenAI   Anthropic   SeuProvider
```

---

## 2. Interface ProviderPort

Todo provider deve implementar `ProviderPort`:

```python
from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from typing import Any

from forge_llm.domain.entities import ChatResponse
from forge_llm.domain.value_objects import Message


class ProviderPort(ABC):
    """Interface abstrata para providers de LLM."""

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Nome identificador do provedor (ex: 'openai', 'anthropic')."""
        ...

    @property
    @abstractmethod
    def supports_streaming(self) -> bool:
        """Indica se o provider suporta streaming."""
        ...

    @property
    @abstractmethod
    def supports_tool_calling(self) -> bool:
        """Indica se o provider suporta tool calling nativo."""
        ...

    @property
    @abstractmethod
    def default_model(self) -> str:
        """Modelo padrao do provider."""
        ...

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
        """Enviar mensagem e receber resposta."""
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
        """Enviar mensagem e receber resposta em streaming."""
        ...
```

---

## 3. Implementando um Novo Provider

### 3.1 Template Basico

```python
"""MeuProvider - Integracao com API XYZ."""

from collections.abc import AsyncIterator
from typing import Any

from forge_llm.application.ports.provider_port import ProviderPort
from forge_llm.domain.entities import ChatResponse, ToolCall
from forge_llm.domain.exceptions import AuthenticationError, RateLimitError
from forge_llm.domain.value_objects import ImageContent, Message, TokenUsage


class MeuProvider(ProviderPort):
    """Provider para API XYZ."""

    def __init__(
        self,
        api_key: str,
        model: str = "modelo-padrao",
        base_url: str | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Inicializar provider.

        Args:
            api_key: API key do servico
            model: Modelo padrao
            base_url: URL base da API (opcional)
            **kwargs: Argumentos adicionais
        """
        self._api_key = api_key
        self._model = model
        self._base_url = base_url or "https://api.exemplo.com/v1"
        # Inicializar cliente HTTP aqui
        # self._client = ...

    @property
    def provider_name(self) -> str:
        return "meu_provider"

    @property
    def supports_streaming(self) -> bool:
        return True  # ou False se nao suportar

    @property
    def supports_tool_calling(self) -> bool:
        return True  # ou False se nao suportar

    @property
    def default_model(self) -> str:
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
        """Implementar chamada de chat."""
        try:
            # 1. Converter mensagens para formato da API
            api_messages = self._convert_messages(messages)

            # 2. Fazer chamada a API
            response = await self._call_api(
                messages=api_messages,
                model=model or self._model,
                temperature=temperature,
                max_tokens=max_tokens,
                tools=tools,
            )

            # 3. Parsear resposta
            return self._parse_response(response)

        except SomeAuthError as e:
            raise AuthenticationError(str(e), self.provider_name) from e
        except SomeRateLimitError as e:
            raise RateLimitError(str(e), self.provider_name) from e

    async def chat_stream(
        self,
        messages: list[Message],
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int | None = None,
        tools: list[dict[str, Any]] | None = None,
        **kwargs: Any,
    ) -> AsyncIterator[dict[str, Any]]:
        """Implementar streaming."""
        # Similar ao chat, mas yield chunks
        async for chunk in self._stream_api(...):
            yield {
                "delta": {"content": chunk.text},
                "finish_reason": chunk.finish_reason,
            }
```

### 3.2 Conversao de Mensagens

Cada API tem seu proprio formato. Implemente metodos de conversao:

```python
def _convert_messages(
    self, messages: list[Message]
) -> list[dict[str, Any]]:
    """Converter Message para formato da API."""
    result = []
    for msg in messages:
        converted = {
            "role": msg.role,
            "content": self._convert_content(msg.content),
        }
        result.append(converted)
    return result

def _convert_content(
    self, content: str | list[str | ImageContent]
) -> str | list[dict[str, Any]]:
    """Converter conteudo (texto ou imagens)."""
    if isinstance(content, str):
        return content

    # Conteudo misto com imagens
    result = []
    for item in content:
        if isinstance(item, str):
            result.append({"type": "text", "text": item})
        elif isinstance(item, ImageContent):
            result.append(self._format_image(item))
    return result
```

### 3.3 Tratamento de Imagens

```python
def _format_image(self, image: ImageContent) -> dict[str, Any]:
    """Formatar ImageContent para API."""
    if image.url:
        return {
            "type": "image_url",
            "url": image.url,
        }
    # Base64
    return {
        "type": "image_base64",
        "media_type": image.media_type,
        "data": image.base64_data,
    }
```

### 3.4 Tratamento de Tools

```python
def _convert_tools(
    self, tools: list[dict[str, Any]] | None
) -> list[dict[str, Any]] | None:
    """Converter tools para formato da API."""
    if not tools:
        return None

    result = []
    for tool in tools:
        if tool.get("type") == "function":
            func = tool.get("function", {})
            result.append({
                "name": func.get("name"),
                "description": func.get("description"),
                "parameters": func.get("parameters"),
            })
    return result
```

---

## 4. Registrando o Provider

### 4.1 Adicionar ao Registry

Edite `src/forge_llm/providers/registry.py`:

```python
from forge_llm.providers.meu_provider import MeuProvider

class ProviderRegistry:
    _providers: dict[str, type] = {
        "openai": OpenAIProvider,
        "anthropic": AnthropicProvider,
        "meu_provider": MeuProvider,  # Adicionar aqui
    }
```

### 4.2 Uso

```python
from forge_llm import Client

client = Client(provider="meu_provider", api_key="...")
response = await client.chat("Ola!")
```

---

## 5. Funcionalidades Obrigatorias

### 5.1 Checklist

- [ ] Implementar `chat()` - chamada sincrona
- [ ] Implementar `chat_stream()` - chamada com streaming
- [ ] Tratar `AuthenticationError` - API key invalida
- [ ] Tratar `RateLimitError` - limite excedido
- [ ] Retornar `TokenUsage` correto
- [ ] Suportar `temperature` e `max_tokens`

### 5.2 Funcionalidades Opcionais

- [ ] Suporte a imagens (Vision)
- [ ] Suporte a tool calling
- [ ] Suporte a system prompts
- [ ] Parametros customizados via `**kwargs`

---

## 6. Tratamento de Excecoes

Mapeie excecoes da API para excecoes de dominio:

```python
from forge_llm.domain.exceptions import (
    AuthenticationError,
    RateLimitError,
    ProviderError,
    ValidationError,
)

# No metodo chat():
try:
    response = await self._client.call(...)
except ApiAuthError as e:
    raise AuthenticationError(str(e), self.provider_name) from e
except ApiRateLimitError as e:
    raise RateLimitError(str(e), self.provider_name) from e
except ApiError as e:
    raise ProviderError(str(e), self.provider_name) from e
```

---

## 7. Testes

### 7.1 Estrutura de Testes

```
tests/
├── unit/
│   └── providers/
│       └── test_meu_provider.py
├── integration/
│   └── test_meu_provider_integration.py
└── bdd/
    └── test_meu_provider_steps.py
```

### 7.2 Exemplo de Teste Unitario

```python
"""Tests for MeuProvider."""

import pytest
from unittest.mock import AsyncMock, MagicMock

from forge_llm.providers.meu_provider import MeuProvider
from forge_llm.domain.value_objects import Message


class TestMeuProvider:
    """Tests for MeuProvider."""

    @pytest.fixture
    def provider(self):
        return MeuProvider(api_key="test-key")

    def test_provider_name(self, provider):
        assert provider.provider_name == "meu_provider"

    def test_default_model(self, provider):
        assert provider.default_model == "modelo-padrao"

    def test_convert_messages(self, provider):
        messages = [Message(role="user", content="Ola")]
        result = provider._convert_messages(messages)

        assert len(result) == 1
        assert result[0]["role"] == "user"
        assert result[0]["content"] == "Ola"

    @pytest.mark.asyncio
    async def test_chat(self, provider, mocker):
        # Mock da API
        mock_response = MagicMock()
        mock_response.content = "Resposta"
        mocker.patch.object(
            provider, "_call_api",
            return_value=mock_response
        )

        response = await provider.chat([
            Message(role="user", content="Ola")
        ])

        assert response.content == "Resposta"
```

### 7.3 Exemplo de Teste de Integracao

```python
"""Integration tests for MeuProvider."""

import os
import pytest

from forge_llm.providers.meu_provider import MeuProvider


@pytest.mark.integration
@pytest.mark.skipif(
    not os.getenv("MEU_PROVIDER_API_KEY"),
    reason="MEU_PROVIDER_API_KEY not set"
)
class TestMeuProviderIntegration:
    """Integration tests."""

    @pytest.fixture
    def provider(self):
        return MeuProvider(
            api_key=os.getenv("MEU_PROVIDER_API_KEY")
        )

    @pytest.mark.asyncio
    async def test_chat_real(self, provider):
        response = await provider.chat([
            Message(role="user", content="Diga 'teste'")
        ])

        assert response.content
        assert response.model
        assert response.usage.total_tokens > 0
```

---

## 8. Boas Praticas

### 8.1 Performance

- Use cliente async (`httpx`, `aiohttp`)
- Reutilize conexoes (connection pooling)
- Configure timeouts adequados

### 8.2 Seguranca

- Nunca logue API keys
- Valide inputs antes de enviar
- Sanitize outputs se necessario

### 8.3 Resiliencia

- Implemente retries internos se necessario
- Configure timeouts
- Trate erros de rede graciosamente

### 8.4 Documentacao

- Docstrings em todos metodos publicos
- Type hints completos
- Exemplo de uso no docstring da classe

---

## 9. Exemplo Completo

Veja os providers existentes como referencia:

- `openai_provider.py` - OpenAI Responses API
- `anthropic_provider.py` - Anthropic Messages API
- `mock_provider.py` - Provider de teste

---

## 10. Suporte

Para duvidas ou problemas:

1. Consulte os providers existentes
2. Execute os testes para validar
3. Abra uma issue se necessario
