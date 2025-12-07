# Arquitetura

O ForgeLLM segue uma **arquitetura hexagonal** (Ports and Adapters), garantindo separação clara entre lógica de domínio e infraestrutura.

## Visão Geral

```mermaid
graph TB
    subgraph "Application Layer"
        Client[Client<br/>Facade]
        Conv[Conversation<br/>Entity]
    end

    subgraph "Domain Layer"
        subgraph "Entities"
            CR[ChatResponse]
            TC[ToolCall]
        end
        subgraph "Value Objects"
            Msg[Message]
            TU[TokenUsage]
            RF[ResponseFormat]
            IC[ImageContent]
        end
        subgraph "Exceptions"
            FE[ForgeError]
            PE[ProviderError]
            VE[ValidationError]
        end
    end

    subgraph "Ports (Interfaces)"
        PP[ProviderPort]
        CP[CachePort]
        RP[RateLimiterPort]
        OP[ObserverPort]
        CCP[ConversationClientPort]
    end

    subgraph "Adapters (Infrastructure)"
        subgraph "Providers"
            OAI[OpenAIProvider]
            ANT[AnthropicProvider]
            OR[OpenRouterProvider]
            AF[AutoFallbackProvider]
        end
        subgraph "Cache"
            IMC[InMemoryCache]
            NOC[NoOpCache]
        end
        subgraph "Rate Limiter"
            TBR[TokenBucketRateLimiter]
            NOR[NoOpRateLimiter]
        end
        subgraph "Observability"
            LO[LoggingObserver]
            MO[MetricsObserver]
            CO[CallbackObserver]
        end
    end

    Client --> PP
    Client --> CP
    Client --> RP
    Client --> OP
    Client -.-> CCP
    Conv --> CCP

    PP --> OAI
    PP --> ANT
    PP --> OR
    PP --> AF
    CP --> IMC
    CP --> NOC
    RP --> TBR
    RP --> NOR
    OP --> LO
    OP --> MO
    OP --> CO
```

## Diagrama de Classes do Domínio

```mermaid
classDiagram
    class Client {
        -ProviderPort _provider
        -str _default_model
        -RetryConfig _retry_config
        -ObservabilityManager _observability
        +chat(message, model, temperature) ChatResponse
        +chat_stream(message, model) AsyncIterator
        +create_conversation(system) Conversation
        +configure(provider, api_key)
    }

    class Conversation {
        -ConversationClientPort _client
        -str _system_prompt
        -list~EnhancedMessage~ _messages
        -int _max_messages
        -int _max_tokens
        +chat(message) ChatResponse
        +add_user_message(content)
        +add_assistant_message(content)
        +change_provider(provider)
        +clear()
    }

    class ChatResponse {
        +str content
        +str model
        +str provider
        +TokenUsage usage
        +list~ToolCall~ tool_calls
        +str finish_reason
        +datetime created_at
        +has_tool_calls() bool
    }

    class ToolCall {
        +str id
        +str name
        +dict arguments
        +to_dict() dict
    }

    class Message {
        +str role
        +str content
        +list~ImageContent~ images
        +to_dict() dict
    }

    class TokenUsage {
        +int prompt_tokens
        +int completion_tokens
        +int total_tokens
    }

    class EnhancedMessage {
        +Message message
        +MessageMetadata metadata
    }

    class MessageMetadata {
        +datetime timestamp
        +str provider
        +str model
    }

    Client --> Conversation : creates
    Client ..|> ConversationClientPort : implements
    Conversation --> EnhancedMessage : contains
    Conversation --> ChatResponse : returns
    ChatResponse --> ToolCall : contains
    ChatResponse --> TokenUsage : contains
    EnhancedMessage --> Message : wraps
    EnhancedMessage --> MessageMetadata : has
```

## Fluxo de Chat (Sequência)

```mermaid
sequenceDiagram
    participant User
    participant Client
    participant Observability
    participant RetryHandler
    participant Provider
    participant LLM API

    User->>Client: chat("Hello!")
    Client->>Client: _normalize_messages()
    Client->>Observability: emit(ChatStartEvent)

    alt With Retry Config
        Client->>RetryHandler: with_retry(chat_fn)
        loop Until Success or Max Retries
            RetryHandler->>Provider: chat(messages)
            Provider->>LLM API: POST /chat/completions

            alt Success
                LLM API-->>Provider: Response
                Provider-->>RetryHandler: ChatResponse
            else Transient Error
                LLM API-->>Provider: 429/500/503
                Provider-->>RetryHandler: RateLimitError
                RetryHandler->>RetryHandler: wait(exponential_backoff)
            end
        end
        RetryHandler-->>Client: ChatResponse
    else No Retry
        Client->>Provider: chat(messages)
        Provider->>LLM API: POST /chat/completions
        LLM API-->>Provider: Response
        Provider-->>Client: ChatResponse
    end

    Client->>Observability: emit(ChatCompleteEvent)
    Client-->>User: ChatResponse
```

## Fluxo de Streaming

```mermaid
sequenceDiagram
    participant User
    participant Client
    participant Provider
    participant LLM API

    User->>Client: chat_stream("Hello!")
    Client->>Client: _normalize_messages()
    Client->>Provider: chat_stream(messages)
    Provider->>LLM API: POST /chat/completions (stream=true)

    loop For Each Chunk
        LLM API-->>Provider: SSE Chunk
        Provider->>Provider: Parse delta
        Provider-->>Client: yield chunk
        Client-->>User: yield chunk
    end

    LLM API-->>Provider: [DONE]
    Provider-->>Client: Stream ends
    Client-->>User: Stream ends
```

## Fluxo de Tool Calling

```mermaid
sequenceDiagram
    participant User
    participant Client
    participant Provider
    participant LLM API
    participant ToolExecutor

    User->>Client: chat("Weather?", tools=[get_weather])
    Client->>Provider: chat(messages, tools)
    Provider->>LLM API: POST /chat/completions
    LLM API-->>Provider: Response with tool_calls
    Provider-->>Client: ChatResponse(tool_calls=[...])
    Client-->>User: ChatResponse

    User->>ToolExecutor: Execute tool_calls
    ToolExecutor-->>User: Tool results

    User->>Client: chat(tool_results)
    Client->>Provider: chat(messages + tool_results)
    Provider->>LLM API: POST /chat/completions
    LLM API-->>Provider: Final response
    Provider-->>Client: ChatResponse
    Client-->>User: ChatResponse
```

## Fluxo de Auto-Fallback

```mermaid
sequenceDiagram
    participant User
    participant Client
    participant AutoFallback
    participant Provider1
    participant Provider2
    participant Provider3

    User->>Client: chat("Hello!")
    Client->>AutoFallback: chat(messages)

    AutoFallback->>Provider1: chat(messages)
    Provider1--xAutoFallback: AuthenticationError

    Note over AutoFallback: Fallback to next provider

    AutoFallback->>Provider2: chat(messages)
    Provider2--xAutoFallback: RateLimitError

    Note over AutoFallback: Fallback to next provider

    AutoFallback->>Provider3: chat(messages)
    Provider3-->>AutoFallback: ChatResponse

    AutoFallback-->>Client: ChatResponse
    Client-->>User: ChatResponse
```

## Arquitetura de Componentes

```mermaid
graph LR
    subgraph "Public API"
        CLI[CLI<br/>forge-llm]
        SDK[SDK<br/>forge_llm.Client]
    end

    subgraph "Core"
        Client[Client]
        Conv[Conversation]
        Registry[ProviderRegistry]
    end

    subgraph "Cross-Cutting"
        Obs[ObservabilityManager]
        Retry[RetryHandler]
        Cache[CachePort]
        RateLimit[RateLimiterPort]
    end

    subgraph "Providers"
        OpenAI[OpenAI]
        Anthropic[Anthropic]
        OpenRouter[OpenRouter]
        AutoFallback[AutoFallback]
    end

    subgraph "MCP"
        MCPClient[MCPClient]
        MCPAdapter[MCPToolAdapter]
    end

    subgraph "Persistence"
        JSONStore[JSONConversationStore]
        MemStore[InMemoryConversationStore]
    end

    CLI --> SDK
    SDK --> Client
    Client --> Registry
    Registry --> OpenAI
    Registry --> Anthropic
    Registry --> OpenRouter
    Registry --> AutoFallback

    Client --> Obs
    Client --> Retry
    Client --> Cache
    Client --> RateLimit

    Client --> Conv
    Conv --> JSONStore
    Conv --> MemStore

    Client --> MCPClient
    MCPClient --> MCPAdapter
```

## Camadas

### Domain Layer

Contém a lógica de negócio pura, sem dependências externas:

| Tipo | Classes | Responsabilidade |
|------|---------|------------------|
| **Entities** | `ChatResponse`, `Conversation`, `ToolCall` | Objetos com identidade e ciclo de vida |
| **Value Objects** | `Message`, `TokenUsage`, `ResponseFormat`, `ImageContent` | Objetos imutáveis sem identidade |
| **Exceptions** | `ForgeError`, `ProviderError`, `ValidationError` | Hierarquia de erros do domínio |

### Application Layer

Coordena o fluxo de dados e orquestra operações:

| Componente | Responsabilidade |
|------------|------------------|
| **Client** | Facade principal - simplifica uso do SDK |
| **Ports** | Interfaces que definem contratos (DIP) |
| **Registry** | Registro e factory de providers |

### Infrastructure Layer

Implementações concretas dos ports:

| Categoria | Implementações |
|-----------|----------------|
| **Providers** | `OpenAIProvider`, `AnthropicProvider`, `OpenRouterProvider`, `AutoFallbackProvider` |
| **Cache** | `InMemoryCache`, `NoOpCache` |
| **Rate Limiter** | `TokenBucketRateLimiter`, `CompositeRateLimiter`, `NoOpRateLimiter` |
| **Persistence** | `JSONConversationStore`, `InMemoryConversationStore` |
| **Observability** | `LoggingObserver`, `MetricsObserver`, `CallbackObserver` |

## Estrutura de Diretórios

```
src/forge_llm/
├── __init__.py              # Public API exports
├── client.py                # Client facade
├── cli.py                   # CLI interface
│
├── domain/
│   ├── entities.py          # ChatResponse, Conversation, ToolCall
│   ├── value_objects.py     # Message, TokenUsage, ImageContent
│   └── exceptions.py        # Exception hierarchy
│
├── application/
│   └── ports/
│       ├── provider_port.py           # ProviderPort interface
│       └── conversation_client_port.py # ConversationClientPort interface
│
├── providers/
│   ├── registry.py          # ProviderRegistry
│   ├── openai_provider.py   # OpenAI adapter
│   ├── anthropic_provider.py # Anthropic adapter
│   ├── openrouter_provider.py # OpenRouter adapter
│   └── auto_fallback_provider.py # Auto-fallback strategy
│
├── infrastructure/
│   ├── cache.py             # Cache implementations
│   ├── rate_limiter.py      # Rate limiter implementations
│   └── retry.py             # Retry with exponential backoff
│
├── observability/
│   ├── manager.py           # ObservabilityManager
│   ├── events.py            # Event types
│   └── observers.py         # Observer implementations
│
├── persistence/
│   ├── store.py             # ConversationStore interface
│   └── json_store.py        # JSON file persistence
│
├── mcp/
│   ├── client.py            # MCP client
│   └── adapter.py           # Tool adapter
│
└── utils/
    ├── token_counter.py     # Token counting
    ├── response_validator.py # Response validation
    └── summarizer.py        # Conversation summarization
```

## Princípios de Design

### 1. Dependency Inversion (DIP)

O domínio não depende de implementações concretas:

```python
# Port (abstração)
class ProviderPort(ABC):
    @abstractmethod
    async def chat(self, messages: list[Message]) -> ChatResponse: ...

# Adapter (implementação)
class OpenAIProvider(ProviderPort):
    async def chat(self, messages: list[Message]) -> ChatResponse:
        # Implementação específica OpenAI
        ...

# Client depende do Port, não do Adapter
class Client:
    def __init__(self, provider: ProviderPort): ...
```

### 2. Single Responsibility

Cada classe tem uma única responsabilidade:

- `Client`: Orquestra operações
- `ProviderRegistry`: Cria providers
- `RetryHandler`: Gerencia retries
- `ObservabilityManager`: Gerencia eventos

### 3. Open/Closed

Extensível sem modificação:

```python
# Adicionar novo provider sem modificar código existente
@ProviderRegistry.register("gemini")
class GeminiProvider(ProviderPort):
    ...
```

### 4. Interface Segregation

Interfaces específicas e focadas:

```python
class CachePort(ABC):
    async def get(self, key: CacheKey) -> Any | None: ...
    async def set(self, key: CacheKey, value: Any) -> None: ...

class RateLimiterPort(ABC):
    async def acquire(self) -> None: ...
    async def release(self) -> None: ...
```

## Benefícios

| Benefício | Descrição |
|-----------|-----------|
| **Testabilidade** | Fácil substituir implementações por mocks |
| **Extensibilidade** | Adicionar novos providers implementando `ProviderPort` |
| **Manutenibilidade** | Separação clara de responsabilidades |
| **Flexibilidade** | Trocar implementações sem afetar o domínio |
| **Observabilidade** | Sistema de eventos para logging/métricas |
| **Resiliência** | Retry automático e fallback entre providers |
