# Guia: Observability & Metricas

Este guia documenta o sistema de observabilidade do ForgeLLMClient para logging, metricas e monitoramento.

---

## 1. Visao Geral

O sistema de observabilidade usa o padrao Observer para emitir eventos durante chamadas de chat.

```
┌─────────────────────────────────────────────────────────┐
│                       Client                             │
│  ┌─────────────────────────────────────────────────┐   │
│  │  chat() / chat_stream()                          │   │
│  │    ├─ emit(ChatStartEvent)                       │   │
│  │    ├─ provider.chat()                            │   │
│  │    └─ emit(ChatCompleteEvent | ChatErrorEvent)   │   │
│  └─────────────────────────────────────────────────┘   │
│                         │                               │
│                         ▼                               │
│  ┌─────────────────────────────────────────────────┐   │
│  │           ObservabilityManager                   │   │
│  │    observers: list[ObserverPort]                 │   │
│  └─────────────────────────────────────────────────┘   │
│         ┌───────────────┼───────────────┐              │
│         ▼               ▼               ▼              │
│  ┌───────────┐   ┌───────────┐   ┌───────────┐        │
│  │ Logging   │   │ Metrics   │   │ Callback  │        │
│  │ Observer  │   │ Observer  │   │ Observer  │        │
│  └───────────┘   └───────────┘   └───────────┘        │
└─────────────────────────────────────────────────────────┘
```

---

## 2. Configuracao Basica

### 2.1 Setup Minimo

```python
from forge_llm import Client, ObservabilityManager, LoggingObserver

# Criar manager de observabilidade
obs = ObservabilityManager()
obs.add_observer(LoggingObserver())

# Usar com client
client = Client(
    provider="openai",
    api_key="sk-...",
    observability=obs
)

# Chamadas agora sao logadas automaticamente
response = await client.chat("Ola!")
# Logs:
# INFO - [req_abc123] Chat started: provider=openai, model=gpt-4o-mini
# INFO - [req_abc123] Chat completed: latency=245ms, tokens=42
```

### 2.2 Multiplos Observers

```python
from forge_llm import (
    ObservabilityManager,
    LoggingObserver,
    MetricsObserver,
    CallbackObserver,
)

obs = ObservabilityManager()

# Adicionar varios observers
obs.add_observer(LoggingObserver())
obs.add_observer(MetricsObserver())

# Todos recebem os mesmos eventos
```

---

## 3. Observers Disponiveis

### 3.1 LoggingObserver

Loga eventos usando `logging` stdlib.

```python
import logging
from forge_llm import LoggingObserver

# Logger padrao (forge_llm)
observer = LoggingObserver()

# Logger customizado
my_logger = logging.getLogger("minha_app")
observer = LoggingObserver(logger=my_logger, level=logging.DEBUG)
```

**Formato dos logs:**

```
INFO  - [req_abc123] Chat started: provider=openai, model=gpt-4, messages=3, tools=True
INFO  - [req_abc123] Chat completed: provider=openai, model=gpt-4, latency=245.5ms, tokens=42, finish=stop
ERROR - [req_abc123] Chat error: provider=openai, error=RateLimitError, latency=50.0ms, retryable=True
WARN  - [req_abc123] Retry: provider=openai, attempt=2/3, delay=2000.0ms, error=RateLimitError
DEBUG - [req_abc123] Stream chunk: provider=openai, index=5, content=True, tool_call=False
```

### 3.2 MetricsObserver

Coleta metricas agregadas de uso.

```python
from forge_llm import MetricsObserver

metrics_obs = MetricsObserver()
obs.add_observer(metrics_obs)

# Apos varias chamadas...
metrics = metrics_obs.metrics

# Totais
print(f"Requests: {metrics.total_requests}")
print(f"Tokens: {metrics.total_tokens}")
print(f"Prompt tokens: {metrics.total_prompt_tokens}")
print(f"Completion tokens: {metrics.total_completion_tokens}")
print(f"Errors: {metrics.total_errors}")
print(f"Retries: {metrics.total_retries}")
print(f"Latencia media: {metrics.avg_latency_ms}ms")

# Por provider
print(f"Requests por provider: {metrics.requests_by_provider}")
# {"openai": 5, "anthropic": 3}

print(f"Tokens por provider: {metrics.tokens_by_provider}")
# {"openai": 1234, "anthropic": 567}

print(f"Erros por tipo: {metrics.errors_by_type}")
# {"RateLimitError": 2, "AuthenticationError": 1}

# Converter para dict (util para exportar)
data = metrics.to_dict()

# Resetar metricas
metrics_obs.reset()
```

### 3.3 CallbackObserver

Executa callbacks customizados para cada tipo de evento.

```python
from forge_llm import CallbackObserver, ChatStartEvent, ChatCompleteEvent

async def on_start(event: ChatStartEvent):
    print(f"Iniciando chamada para {event.provider}")

async def on_complete(event: ChatCompleteEvent):
    print(f"Concluido em {event.latency_ms}ms")
    print(f"Tokens: {event.token_usage.total_tokens}")

    # Enviar para sistema de monitoramento externo
    await send_to_datadog(event)

async def on_error(event):
    await send_alert(f"Erro: {event.error_type}")

observer = CallbackObserver(
    on_start=on_start,
    on_complete=on_complete,
    on_error=on_error,
)

obs.add_observer(observer)
```

---

## 4. Eventos

### 4.1 ChatStartEvent

Emitido no inicio de uma chamada de chat.

```python
from forge_llm import ChatStartEvent

# Campos
event.timestamp      # datetime: Quando ocorreu
event.request_id     # str: ID unico (ex: "req_abc123")
event.provider       # str: Nome do provider
event.model          # str | None: Modelo usado
event.message_count  # int: Quantidade de mensagens
event.has_tools      # bool: Se tem tools definidas
```

### 4.2 ChatCompleteEvent

Emitido quando uma chamada completa com sucesso.

```python
from forge_llm import ChatCompleteEvent

# Campos
event.timestamp        # datetime
event.request_id       # str
event.provider         # str
event.model            # str
event.latency_ms       # float: Tempo de resposta
event.token_usage      # TokenUsage: Consumo de tokens
event.finish_reason    # str: "stop", "tool_calls", etc
event.tool_calls_count # int: Quantidade de tool calls
```

### 4.3 ChatErrorEvent

Emitido quando ocorre um erro.

```python
from forge_llm import ChatErrorEvent

# Campos
event.timestamp      # datetime
event.request_id     # str
event.provider       # str
event.error_type     # str: Nome da excecao
event.error_message  # str: Mensagem de erro
event.latency_ms     # float: Tempo ate o erro
event.retryable      # bool: Se e recuperavel via retry
```

### 4.4 RetryEvent

Emitido quando uma tentativa de retry e feita.

```python
from forge_llm import RetryEvent

# Campos
event.timestamp    # datetime
event.request_id   # str
event.provider     # str
event.attempt      # int: Tentativa atual (1, 2, 3...)
event.max_attempts # int: Maximo de tentativas
event.delay_ms     # float: Delay antes do retry
event.error_type   # str: Tipo do erro que causou retry
```

### 4.5 StreamChunkEvent

Emitido para cada chunk em streaming.

```python
from forge_llm import StreamChunkEvent

# Campos
event.timestamp     # datetime
event.request_id    # str
event.provider      # str
event.chunk_index   # int: Indice do chunk (0, 1, 2...)
event.has_content   # bool: Se tem conteudo de texto
event.has_tool_call # bool: Se tem tool call
```

---

## 5. Configuracao

### 5.1 ObservabilityConfig

```python
from forge_llm import ObservabilityManager, ObservabilityConfig

# Desabilitar observabilidade
config = ObservabilityConfig(enabled=False)
obs = ObservabilityManager(config=config)

# Nenhum evento sera emitido
await client.chat("Ola!")

# Habilitar novamente
config.enabled = True
```

### 5.2 Privacy - Conteudo nao logado

Por design, os eventos NAO contem o conteudo das mensagens.
Apenas metadados sao emitidos para proteger dados sensiveis.

```python
# ChatStartEvent tem:
event.message_count  # 3 (quantidade, nao conteudo)

# ChatCompleteEvent tem:
event.token_usage    # tokens, nao texto
event.finish_reason  # "stop", nao resposta
```

---

## 6. Observer Customizado

### 6.1 Implementando ObserverPort

```python
from forge_llm import ObserverPort
from typing import Any

class MeuObserver(ObserverPort):
    """Observer que envia metricas para Prometheus."""

    def __init__(self, registry):
        self._registry = registry
        self._counter = Counter(
            "llm_requests_total",
            "Total de requests LLM",
            ["provider", "model"]
        )

    async def on_event(self, event: Any) -> None:
        if isinstance(event, ChatCompleteEvent):
            self._counter.labels(
                provider=event.provider,
                model=event.model
            ).inc()

# Usar
obs = ObservabilityManager()
obs.add_observer(MeuObserver(prometheus_registry))
```

### 6.2 Observer com Filtragem

```python
class FilteredObserver(ObserverPort):
    """Observer que filtra por provider."""

    def __init__(self, provider_filter: str):
        self._filter = provider_filter

    async def on_event(self, event: Any) -> None:
        if hasattr(event, 'provider'):
            if event.provider == self._filter:
                await self._process(event)

    async def _process(self, event: Any) -> None:
        # Processar apenas eventos do provider filtrado
        print(f"Evento: {event}")
```

---

## 7. Integracao com Sistemas Externos

### 7.1 DataDog

```python
from datadog import statsd
from forge_llm import CallbackObserver

async def send_to_datadog(event):
    if isinstance(event, ChatCompleteEvent):
        statsd.timing(
            "llm.latency",
            event.latency_ms,
            tags=[f"provider:{event.provider}", f"model:{event.model}"]
        )
        statsd.increment(
            "llm.tokens",
            event.token_usage.total_tokens,
            tags=[f"provider:{event.provider}"]
        )

obs.add_observer(CallbackObserver(on_complete=send_to_datadog))
```

### 7.2 OpenTelemetry

```python
from opentelemetry import trace, metrics

tracer = trace.get_tracer(__name__)
meter = metrics.get_meter(__name__)

request_counter = meter.create_counter("llm_requests")

async def on_complete(event):
    with tracer.start_as_current_span("llm_call") as span:
        span.set_attribute("provider", event.provider)
        span.set_attribute("model", event.model)
        span.set_attribute("latency_ms", event.latency_ms)

    request_counter.add(1, {"provider": event.provider})
```

### 7.3 Sentry

```python
import sentry_sdk

async def on_error(event):
    sentry_sdk.capture_message(
        f"LLM Error: {event.error_type}",
        level="error",
        extras={
            "provider": event.provider,
            "request_id": event.request_id,
            "error_message": event.error_message,
        }
    )
```

---

## 8. Boas Praticas

### 8.1 Observers Async

Observers devem ser rapidos e nao bloquear a chamada principal.
Para operacoes lentas, use fire-and-forget:

```python
import asyncio

async def on_complete(event):
    # Fire-and-forget para nao bloquear
    asyncio.create_task(slow_operation(event))

async def slow_operation(event):
    await asyncio.sleep(1)  # Operacao lenta
    await save_to_database(event)
```

### 8.2 Tratamento de Erros em Observers

Erros em observers sao silenciados automaticamente para nao afetar o fluxo principal:

```python
class UnstableObserver(ObserverPort):
    async def on_event(self, event):
        raise RuntimeError("Erro!")  # Silenciado

# A chamada continua funcionando
response = await client.chat("Ola!")  # Sucesso
```

### 8.3 Gerenciamento de Observers

```python
# Adicionar
obs.add_observer(my_observer)

# Remover
obs.remove_observer(my_observer)

# Limpar todos
obs.clear_observers()

# Verificar quantidade
print(obs.observer_count)  # 3
```

---

## 9. Imports

```python
from forge_llm import (
    # Manager
    ObservabilityManager,
    ObservabilityConfig,

    # Interface
    ObserverPort,

    # Observers
    LoggingObserver,
    MetricsObserver,
    UsageMetrics,
    CallbackObserver,

    # Events
    ChatStartEvent,
    ChatCompleteEvent,
    ChatErrorEvent,
    RetryEvent,
    StreamChunkEvent,
)
```

---

## Recursos Adicionais

- [Guia de Uso do Client](client-usage.md) - Uso basico do SDK
- [Guia de Tratamento de Erros](error-handling.md) - Excecoes e retry

---

**Versao**: ForgeLLMClient 0.1.0
