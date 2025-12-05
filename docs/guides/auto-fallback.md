# Guia: Auto-Fallback entre Providers

Este guia documenta o sistema de fallback automatico do ForgeLLMClient para alta disponibilidade entre multiplos providers LLM.

---

## 1. Visao Geral

O `AutoFallbackProvider` permite configurar multiplos providers em sequencia. Se um provider falhar com erro transiente (rate limit, timeout), o sistema automaticamente tenta o proximo.

```
┌─────────────────────────────────────────────────────────┐
│                 AutoFallbackProvider                     │
│  ┌─────────────────────────────────────────────────┐   │
│  │  chat() / chat_stream()                          │   │
│  │                                                  │   │
│  │  1. Tenta Provider A ───────────────────────┐   │   │
│  │  2. Se RateLimitError, tenta Provider B ─┐  │   │   │
│  │  3. Se timeout, tenta Provider C         │  │   │   │
│  │  4. Retorna sucesso OU AllProvidersFailedError  │   │
│  └─────────────────────────────────────────────────┘   │
│                         │                               │
│         ┌───────────────┼───────────────┐              │
│         ▼               ▼               ▼              │
│  ┌───────────┐   ┌───────────┐   ┌───────────┐        │
│  │  OpenAI   │   │ Anthropic │   │  OpenRouter│        │
│  │ (primario)│   │(secundario)│  │ (terceiro) │        │
│  └───────────┘   └───────────┘   └───────────┘        │
└─────────────────────────────────────────────────────────┘
```

---

## 2. Configuracao Basica

### 2.1 Setup Minimo

```python
from forge_llm.providers.auto_fallback_provider import (
    AutoFallbackProvider,
    AutoFallbackConfig,
)

# Criar provider com fallback
provider = AutoFallbackProvider(
    providers=["openai", "anthropic"],
    api_keys={
        "openai": "sk-...",
        "anthropic": "sk-ant-...",
    },
)

# Usar normalmente
from forge_llm.domain.value_objects import Message

messages = [Message(role="user", content="Ola!")]
response = await provider.chat(messages)

# Verificar qual provider foi usado
print(f"Resposta de: {provider.last_provider_used}")
```

### 2.2 Com Client

```python
from forge_llm import Client
from forge_llm.providers.auto_fallback_provider import AutoFallbackProvider

# Criar provider com fallback
fallback_provider = AutoFallbackProvider(
    providers=["openai", "anthropic", "openrouter"],
    api_keys={
        "openai": "sk-...",
        "anthropic": "sk-ant-...",
        "openrouter": "sk-or-...",
    },
)

# Usar com Client
client = Client(provider=fallback_provider)
response = await client.chat("Ola!")

print(response.content)
print(f"Provider usado: {fallback_provider.last_provider_used}")
```

---

## 3. Configuracao Avancada

### 3.1 AutoFallbackConfig

```python
from forge_llm.providers.auto_fallback_provider import (
    AutoFallbackProvider,
    AutoFallbackConfig,
)
from forge_llm.infrastructure.retry import RetryConfig
from forge_llm.domain.exceptions import RateLimitError, APITimeoutError

config = AutoFallbackConfig(
    # Retry em cada provider antes de fallback
    retry_per_provider=True,

    # Configuracao de retry por provider
    retry_config=RetryConfig(
        max_retries=3,
        base_delay=1.0,
        max_delay=30.0,
        exponential_base=2.0,
    ),

    # Erros que disparam fallback
    fallback_on_errors=(RateLimitError, APITimeoutError),
)

provider = AutoFallbackProvider(
    providers=["openai", "anthropic"],
    api_keys={...},
    config=config,
)
```

**Campos:**

| Campo | Tipo | Default | Descricao |
|-------|------|---------|-----------|
| retry_per_provider | bool | True | Retry em cada provider antes de fallback |
| retry_config | RetryConfig | None | Configuracao de retry |
| fallback_on_errors | tuple | (RateLimitError, APITimeoutError) | Erros que disparam fallback |

### 3.2 Com Instancias de Provider

```python
from forge_llm.providers.openai_provider import OpenAIProvider
from forge_llm.providers.anthropic_provider import AnthropicProvider

# Criar providers com configuracao customizada
openai = OpenAIProvider(
    api_key="sk-...",
    default_model="gpt-4-turbo",
)

anthropic = AnthropicProvider(
    api_key="sk-ant-...",
    default_model="claude-3-opus-20240229",
)

# Usar instancias
provider = AutoFallbackProvider(providers=[openai, anthropic])
```

---

## 4. Comportamento de Fallback

### 4.1 Erros que Disparam Fallback

Por padrao, fallback ocorre para:

| Erro | Comportamento | Razao |
|------|---------------|-------|
| RateLimitError | Fallback | Erro transiente, outro provider pode funcionar |
| APITimeoutError | Fallback | Erro transiente |
| APIError (retryable=True) | Fallback | Erros marcados como recuperaveis |
| RetryExhaustedError | Fallback | Retries esgotados, tentar outro provider |

### 4.2 Erros que NAO Disparam Fallback

| Erro | Comportamento | Razao |
|------|---------------|-------|
| AuthenticationError | Propaga imediatamente | Credencial invalida nao sera resolvida tentando novamente |
| ValidationError | Propaga imediatamente | Input invalido nao mudara com outro provider |
| APIError (retryable=False) | Propaga imediatamente | Erro nao recuperavel |

### 4.3 Fluxo de Decisao

```
Erro ocorre
    │
    ├─► AuthenticationError? ─► Propaga imediatamente
    │
    ├─► RateLimitError ou APITimeoutError? ─► Fallback
    │
    ├─► APIError com retryable=True? ─► Fallback
    │
    └─► Outro erro ─► Propaga imediatamente
```

---

## 5. Resultados e Metadados

### 5.1 FallbackResult

```python
provider = AutoFallbackProvider(...)
response = await provider.chat(messages)

# Acessar resultado detalhado
result = provider.last_fallback_result

print(f"Provider usado: {result.provider_used}")
print(f"Providers tentados: {result.providers_tried}")
print(f"Erros: {result.errors}")
print(f"Resposta: {result.response}")
```

**Campos do FallbackResult:**

```python
result.response        # ChatResponse | None: Resposta se sucesso
result.provider_used   # str | None: Nome do provider que respondeu
result.providers_tried # list[str]: Lista de providers tentados
result.errors          # dict[str, Exception]: Erros por provider
```

### 5.2 Propriedades do Provider

```python
# Nome do ultimo provider que respondeu
provider.last_provider_used  # "openai"

# Lista de providers configurados
provider.providers_list  # ["openai", "anthropic"]

# Resultado detalhado
provider.last_fallback_result  # FallbackResult
```

---

## 6. Tratamento de Erros

### 6.1 AllProvidersFailedError

Quando todos os providers falham:

```python
from forge_llm.providers.auto_fallback_provider import (
    AutoFallbackProvider,
    AllProvidersFailedError,
)

provider = AutoFallbackProvider(
    providers=["openai", "anthropic"],
    api_keys={...},
)

try:
    response = await provider.chat(messages)
except AllProvidersFailedError as e:
    print(f"Todos falharam: {e}")
    print(f"Providers tentados: {e.providers_tried}")
    print(f"Erros por provider:")
    for name, error in e.errors.items():
        print(f"  {name}: {error}")
```

### 6.2 Erros Propagados Imediatamente

```python
from forge_llm.domain.exceptions import AuthenticationError

try:
    response = await provider.chat(messages)
except AuthenticationError as e:
    # Erro de auth e propagado imediatamente
    # Nao adianta tentar outro provider com mesma key
    print(f"Credencial invalida: {e}")
```

---

## 7. Streaming

### 7.1 Fallback com Streaming

```python
provider = AutoFallbackProvider(
    providers=["openai", "anthropic"],
    api_keys={...},
)

# Fallback funciona antes do primeiro chunk
async for chunk in provider.chat_stream(messages):
    if "content" in chunk:
        print(chunk["content"], end="")

print(f"\nProvider usado: {provider.last_provider_used}")
```

**IMPORTANTE:** O fallback so funciona ANTES do primeiro chunk ser recebido. Uma vez que o streaming comeca, erros sao propagados.

---

## 8. Exemplos de Uso

### 8.1 Alta Disponibilidade

```python
# Prioridade: OpenAI (mais rapido) > Anthropic > OpenRouter (backup)
provider = AutoFallbackProvider(
    providers=["openai", "anthropic", "openrouter"],
    api_keys={
        "openai": "sk-...",
        "anthropic": "sk-ant-...",
        "openrouter": "sk-or-...",
    },
    config=AutoFallbackConfig(
        retry_per_provider=True,
        retry_config=RetryConfig(max_retries=2, base_delay=1.0),
    ),
)

# Em caso de rate limit no OpenAI, tenta Anthropic
# Se Anthropic falhar, tenta OpenRouter
response = await provider.chat(messages)
```

### 8.2 Fallback para Modelo Local

```python
from forge_llm.providers.openai_provider import OpenAIProvider

# OpenAI como primario, Ollama como backup local
openai = OpenAIProvider(api_key="sk-...", default_model="gpt-4")

ollama = OpenAIProvider(
    api_key="",  # Ollama nao precisa
    base_url="http://localhost:11434/v1",
    default_model="llama2",
)

provider = AutoFallbackProvider(providers=[openai, ollama])
```

### 8.3 Custo Otimizado

```python
# Tentar modelo mais barato primeiro, caro como fallback
openai_mini = OpenAIProvider(api_key="sk-...", default_model="gpt-4o-mini")
openai_full = OpenAIProvider(api_key="sk-...", default_model="gpt-4-turbo")
anthropic = AnthropicProvider(api_key="sk-ant-...", default_model="claude-3-opus")

provider = AutoFallbackProvider(providers=[openai_mini, openai_full, anthropic])
```

---

## 9. Boas Praticas

### 9.1 Ordem dos Providers

Ordene por prioridade:
1. **Mais rapido/barato primeiro**: gpt-4o-mini antes de gpt-4
2. **Mais confiavel primeiro**: OpenAI/Anthropic antes de OpenRouter
3. **Backup local por ultimo**: Ollama como ultima opcao

### 9.2 Retry Equilibrado

```python
# Retry moderado por provider para nao demorar muito
config = AutoFallbackConfig(
    retry_per_provider=True,
    retry_config=RetryConfig(
        max_retries=2,      # Max 2 retries por provider
        base_delay=1.0,     # 1 segundo inicial
        max_delay=5.0,      # Max 5 segundos
    ),
)
```

### 9.3 Logging para Debug

```python
import logging

logging.getLogger("forge_llm").setLevel(logging.DEBUG)

# Logs mostrarao qual provider foi tentado e por que falhou
```

---

## 10. Imports

```python
from forge_llm.providers.auto_fallback_provider import (
    # Provider
    AutoFallbackProvider,

    # Configuracao
    AutoFallbackConfig,

    # Resultado
    FallbackResult,

    # Excecao
    AllProvidersFailedError,
)

from forge_llm.infrastructure.retry import RetryConfig
```

---

## Recursos Adicionais

- [Guia de Uso do Client](client-usage.md) - Uso basico do SDK
- [Guia de Tratamento de Erros](error-handling.md) - Excecoes e retry
- [Guia de Observability](observability.md) - Logging e metricas

---

**Versao**: ForgeLLMClient 0.1.0
