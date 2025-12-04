# Guia: Tratamento de Erros do ForgeLLMClient

Este guia documenta as excecoes do ForgeLLMClient e padroes de tratamento de erros.

---

## 1. Hierarquia de Excecoes

```
ForgeError (base)
├── ValidationError         # Dados invalidos
├── ConfigurationError      # Erro de configuracao
├── ProviderError          # Erro generico do provider
│   ├── AuthenticationError # API key invalida
│   ├── RateLimitError     # Limite de requisicoes
│   └── APIError           # Erro generico de API
├── APITimeoutError        # Timeout na chamada
├── RetryExhaustedError    # Retries esgotados
├── ToolNotFoundError      # Tool nao existe
└── ToolCallNotFoundError  # Tool call ID nao encontrado
```

---

## 2. Excecoes Detalhadas

### 2.1 ForgeError

Excecao base de todas as excecoes do ForgeLLMClient.

```python
from forge_llm.domain.exceptions import ForgeError

try:
    response = await client.chat("Ola!")
except ForgeError as e:
    print(f"Erro do ForgeLLM: {e}")
```

### 2.2 ValidationError

Erro de validacao de dados de entrada.

```python
from forge_llm.domain.exceptions import ValidationError
from forge_llm.domain.value_objects import Message

# Exemplos que geram ValidationError
try:
    # Role invalido
    Message(role="invalid", content="Ola")
except ValidationError as e:
    print(e)  # "Role invalido: invalid"

try:
    # Mensagem vazia
    await client.chat("")
except ValidationError as e:
    print(e)  # "Mensagem nao pode ser vazia"

try:
    # TokenUsage com valor negativo
    TokenUsage(prompt_tokens=-1, completion_tokens=0)
except ValidationError as e:
    print(e)  # "prompt_tokens nao pode ser negativo"
```

### 2.3 AuthenticationError

Erro de autenticacao (API key invalida ou expirada).

```python
from forge_llm.domain.exceptions import AuthenticationError

try:
    client = Client(provider="openai", api_key="invalid-key")
    await client.chat("Ola!")
except AuthenticationError as e:
    print(f"Erro de autenticacao: {e}")
    print(f"Provider: {e.provider}")  # "openai"
```

**Atributos:**
- `provider`: Nome do provider que rejeitou a autenticacao

**Quando ocorre:**
- API key invalida
- API key expirada
- API key sem permissoes

### 2.4 RateLimitError

Erro quando o limite de requisicoes foi excedido.

```python
from forge_llm.domain.exceptions import RateLimitError

try:
    await client.chat("Ola!")
except RateLimitError as e:
    print(f"Rate limit excedido: {e}")
    print(f"Provider: {e.provider}")
    print(f"Aguardar: {e.retry_after} segundos")

    if e.retry_after:
        import asyncio
        await asyncio.sleep(e.retry_after)
        # Tentar novamente
```

**Atributos:**
- `provider`: Nome do provider
- `retry_after`: Tempo sugerido para retry (segundos ou None)

### 2.5 ProviderError

Erro generico ao comunicar com o provider.

```python
from forge_llm.domain.exceptions import ProviderError

try:
    await client.chat("Ola!")
except ProviderError as e:
    print(f"Erro do provider: {e}")
    print(f"Provider: {e.provider}")
    print(f"Status code: {e.status_code}")
```

**Atributos:**
- `provider`: Nome do provider
- `status_code`: Codigo HTTP (opcional)

### 2.6 APIError

Erro generico de API com indicacao de retry.

```python
from forge_llm.domain.exceptions import APIError

try:
    await client.chat("Ola!")
except APIError as e:
    print(f"Erro de API: {e}")
    print(f"Provider: {e.provider}")
    print(f"Status code: {e.status_code}")
    print(f"Retryable: {e.retryable}")

    if e.retryable:
        # Seguro fazer retry
        pass
```

**Atributos:**
- `provider`: Nome do provider
- `status_code`: Codigo HTTP (opcional)
- `retryable`: Se o erro e recuperavel via retry

### 2.7 APITimeoutError

Erro de timeout na chamada de API.

```python
from forge_llm.domain.exceptions import APITimeoutError

try:
    await client.chat("Gere um texto muito longo...")
except APITimeoutError as e:
    print(f"Timeout: {e}")
    print(f"Provider: {e.provider}")
    print(f"Timeout configurado: {e.timeout}s")
```

**Atributos:**
- `provider`: Nome do provider
- `timeout`: Valor do timeout em segundos (opcional)

### 2.8 RetryExhaustedError

Erro quando todas as tentativas de retry foram esgotadas.

```python
from forge_llm.domain.exceptions import RetryExhaustedError

client = Client(provider="openai", api_key="sk-...", max_retries=3)

try:
    await client.chat("Ola!")
except RetryExhaustedError as e:
    print(f"Retries esgotados: {e}")
    print(f"Provider: {e.provider}")
    print(f"Tentativas: {e.attempts}")
    print(f"Ultimo erro: {e.last_error}")
```

**Atributos:**
- `provider`: Nome do provider
- `attempts`: Numero de tentativas realizadas
- `last_error`: Ultima excecao antes de desistir

### 2.9 ConfigurationError

Erro de configuracao do cliente.

```python
from forge_llm.domain.exceptions import ConfigurationError

try:
    client = Client()  # Sem configurar provider
    await client.chat("Ola!")
except RuntimeError:
    print("Cliente nao configurado")

# Ou
try:
    from forge_llm.providers.registry import ProviderRegistry
    ProviderRegistry.create("provider_inexistente", api_key="...")
except ConfigurationError as e:
    print(f"Erro de configuracao: {e}")
```

### 2.10 ToolNotFoundError

Erro quando uma tool nao e encontrada.

```python
from forge_llm.domain.exceptions import ToolNotFoundError

try:
    # Codigo que busca tool inexistente
    pass
except ToolNotFoundError as e:
    print(f"Tool nao encontrada: {e.tool_name}")
    print(f"Tools disponiveis: {e.available_tools}")
```

**Atributos:**
- `tool_name`: Nome da tool procurada
- `available_tools`: Lista de tools disponiveis

### 2.11 ToolCallNotFoundError

Erro quando um tool_call_id nao e encontrado.

```python
from forge_llm.domain.exceptions import ToolCallNotFoundError

try:
    # Codigo que busca tool call inexistente
    pass
except ToolCallNotFoundError as e:
    print(f"Tool call nao encontrado: {e.tool_call_id}")
```

**Atributos:**
- `tool_call_id`: ID do tool call procurado

---

## 3. Padroes de Tratamento

### 3.1 Tratamento Basico

```python
from forge_llm.domain.exceptions import (
    ForgeError,
    AuthenticationError,
    RateLimitError,
    ProviderError,
)

async def chat_seguro(client, message):
    try:
        return await client.chat(message)
    except AuthenticationError:
        print("API key invalida. Verifique suas credenciais.")
        return None
    except RateLimitError as e:
        print(f"Limite excedido. Aguarde {e.retry_after or 60}s")
        return None
    except ProviderError as e:
        print(f"Erro do provider {e.provider}: {e}")
        return None
    except ForgeError as e:
        print(f"Erro inesperado: {e}")
        return None
```

### 3.2 Tratamento com Retry Manual

```python
import asyncio
from forge_llm.domain.exceptions import RateLimitError, APIError

async def chat_com_retry(client, message, max_retries=3):
    for attempt in range(max_retries):
        try:
            return await client.chat(message)
        except RateLimitError as e:
            if attempt < max_retries - 1:
                wait = e.retry_after or (2 ** attempt)
                print(f"Rate limit. Aguardando {wait}s...")
                await asyncio.sleep(wait)
            else:
                raise
        except APIError as e:
            if e.retryable and attempt < max_retries - 1:
                wait = 2 ** attempt
                print(f"Erro retryable. Tentativa {attempt + 1}...")
                await asyncio.sleep(wait)
            else:
                raise
```

### 3.3 Usando Retry Automatico do Client

```python
from forge_llm import Client
from forge_llm.infrastructure.retry import RetryConfig

# Configuracao simples
client = Client(
    provider="openai",
    api_key="sk-...",
    max_retries=3,
    retry_delay=1.0
)

# Configuracao avancada
config = RetryConfig(
    max_retries=5,
    base_delay=1.0,
    max_delay=30.0,
    exponential_base=2.0
)

client = Client(
    provider="openai",
    api_key="sk-...",
    retry_config=config
)

# Chamada normal - retry e automatico
try:
    response = await client.chat("Ola!")
except RetryExhaustedError as e:
    print(f"Todas {e.attempts} tentativas falharam")
    print(f"Ultimo erro: {e.last_error}")
```

### 3.4 Context Manager para Cleanup

```python
from forge_llm import Client
from forge_llm.domain.exceptions import ForgeError

async def main():
    client = Client(provider="openai", api_key="sk-...")
    try:
        response = await client.chat("Ola!")
        print(response.content)
    except ForgeError as e:
        print(f"Erro: {e}")
    finally:
        await client.close()
```

---

## 4. Mapeamento de Erros por Provider

### 4.1 OpenAI

| Erro OpenAI | Excecao ForgeLLM |
|-------------|------------------|
| `AuthenticationError` | `AuthenticationError` |
| `RateLimitError` | `RateLimitError` |
| `BadRequestError` | `ValidationError` |
| `APIError` | `ProviderError` |
| `APIConnectionError` | `APIError(retryable=True)` |
| `APITimeoutError` | `APITimeoutError` |

### 4.2 Anthropic

| Erro Anthropic | Excecao ForgeLLM |
|----------------|------------------|
| `AuthenticationError` | `AuthenticationError` |
| `RateLimitError` | `RateLimitError` |
| `BadRequestError` | `ValidationError` |
| `APIError` | `ProviderError` |
| `APIConnectionError` | `APIError(retryable=True)` |

### 4.3 Google Gemini

| Erro Gemini | Excecao ForgeLLM |
|-------------|------------------|
| `InvalidArgument` | `ValidationError` |
| `PermissionDenied` | `AuthenticationError` |
| `ResourceExhausted` | `RateLimitError` |
| Outros | `ProviderError` |

### 4.4 OpenRouter

| Erro OpenRouter | Excecao ForgeLLM |
|-----------------|------------------|
| `AuthenticationError` | `AuthenticationError` |
| `RateLimitError` | `RateLimitError` |
| `BadRequestError` | `ValidationError` |
| `APIError` | `ProviderError` |

---

## 5. Codigos HTTP Comuns

| Codigo | Significado | Excecao |
|--------|-------------|---------|
| 400 | Bad Request | `ValidationError` |
| 401 | Unauthorized | `AuthenticationError` |
| 403 | Forbidden | `AuthenticationError` |
| 404 | Not Found | `ProviderError` |
| 429 | Too Many Requests | `RateLimitError` |
| 500 | Internal Server Error | `APIError(retryable=True)` |
| 502 | Bad Gateway | `APIError(retryable=True)` |
| 503 | Service Unavailable | `APIError(retryable=True)` |
| 504 | Gateway Timeout | `APITimeoutError` |

---

## 6. Boas Praticas

### 6.1 Sempre Tratar Erros Especificos

```python
# Bom: Tratar erros especificos
try:
    response = await client.chat(message)
except AuthenticationError:
    # Acao especifica para auth
    pass
except RateLimitError:
    # Acao especifica para rate limit
    pass

# Evitar: Capturar Exception generica
try:
    response = await client.chat(message)
except Exception:  # Muito generico!
    pass
```

### 6.2 Logar Erros com Contexto

```python
import logging

logger = logging.getLogger(__name__)

try:
    response = await client.chat(message)
except ProviderError as e:
    logger.error(
        "Erro ao chamar provider",
        extra={
            "provider": e.provider,
            "status_code": e.status_code,
            "message": str(e),
        }
    )
    raise
```

### 6.3 Usar Retry para Erros Transientes

```python
# Erros transientes (vale retry):
# - RateLimitError (com backoff)
# - APIError com retryable=True
# - APITimeoutError (talvez)

# Erros permanentes (nao vale retry):
# - AuthenticationError
# - ValidationError
# - ConfigurationError
```

### 6.4 Validar Entrada Antes de Chamar

```python
from forge_llm.domain.exceptions import ValidationError

def validar_mensagem(message: str) -> str:
    if not message or not message.strip():
        raise ValidationError("Mensagem nao pode ser vazia")
    if len(message) > 100000:
        raise ValidationError("Mensagem muito longa")
    return message.strip()

# Uso
try:
    message = validar_mensagem(user_input)
    response = await client.chat(message)
except ValidationError as e:
    print(f"Entrada invalida: {e}")
```

---

## 7. Imports

```python
from forge_llm.domain.exceptions import (
    # Base
    ForgeError,

    # Validacao
    ValidationError,
    ConfigurationError,

    # Provider
    ProviderError,
    AuthenticationError,
    RateLimitError,
    APIError,
    APITimeoutError,

    # Retry
    RetryExhaustedError,

    # Tools
    ToolNotFoundError,
    ToolCallNotFoundError,
)
```

---

## Recursos Adicionais

- [Guia de Uso do Client](client-usage.md) - Como usar o SDK
- [Guia do Modelo de Dominio](domain-model.md) - Entidades e Value Objects
- [Guia de Criacao de Providers](creating-providers.md) - Novos providers

---

**Versao**: ForgeLLMClient 0.1.0
