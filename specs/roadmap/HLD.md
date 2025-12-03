# HLD — ForgeLLMClient High Level Design

> **Versao:** 1.0
> **Data:** 2025-12-03
> **Status:** Aprovado

---

## 1. Visao Geral do Sistema

O ForgeLLMClient e um SDK Python que oferece interface unificada para multiplos provedores LLM, permitindo:

- **PortableChat**: Chat sync e streaming com interface padronizada
- **HotSwap**: Trocar provedor em runtime sem alterar codigo
- **AutoFallback**: Fallback automatico entre provedores
- **UnifiedTools**: Normalizacao de tool calling entre provedores
- **MCPClient**: Integracao com MCP (Model Context Protocol)

---

## 2. Diagrama de Contexto (C4)

```mermaid
C4Context
    title Diagrama de Contexto - ForgeLLMClient

    Person(dev, "Desenvolvedor Python", "Utiliza o SDK para integrar LLMs")

    System(forgellm, "ForgeLLMClient", "SDK Python para interface unificada com LLMs<br/>- Chat sync/streaming<br/>- Tool calling normalizado<br/>- HotSwap e AutoFallback<br/>- MCP Client")

    System_Ext(openai, "OpenAI API", "Responses API")
    System_Ext(anthropic, "Anthropic API", "Messages API")
    System_Ext(mcp, "MCP Server", "Model Context Protocol")

    Rel(dev, forgellm, "Usa")
    Rel(forgellm, openai, "HTTPS/REST")
    Rel(forgellm, anthropic, "HTTPS/REST")
    Rel(forgellm, mcp, "JSON-RPC")
```

---

## 3. Diagrama de Componentes

```mermaid
flowchart TB
    subgraph Adapters["ADAPTERS"]
        CLI["CLI Adapter"]
        HTTP["HTTP Adapter<br/>(futuro)"]
    end

    subgraph Application["APPLICATION"]
        ChatUC["ChatUseCase"]
        StreamUC["StreamUseCase"]
        ToolsUC["ToolsUseCase"]

        subgraph Ports["PORTS (Interfaces)"]
            ProviderPort["ProviderPort"]
            ConfigPort["ConfigPort"]
            ToolRegistryPort["ToolRegistryPort"]
        end
    end

    subgraph Domain["DOMAIN"]
        ChatResponse["ChatResponse<br/>(Entity)"]
        Message["Message<br/>(ValueObject)"]
        ToolCall["ToolCall<br/>(Entity)"]
        TokenUsage["TokenUsage<br/>(ValueObject)"]
        ForgeError["ForgeError<br/>(Exception)"]
    end

    subgraph Infrastructure["INFRASTRUCTURE"]
        ConfigLoader["ConfigLoader"]
        HTTPClient["HTTPClient"]
    end

    subgraph Providers["PROVIDERS"]
        OpenAI["OpenAI<br/>Provider"]
        Anthropic["Anthropic<br/>Provider"]
        Mock["Mock<br/>Provider"]
    end

    subgraph External["EXTERNAL APIs"]
        OpenAIAPI["OpenAI API"]
        AnthropicAPI["Anthropic API"]
        InMemory["In-Memory<br/>(Testes)"]
    end

    CLI --> ChatUC
    HTTP --> ChatUC
    CLI --> StreamUC
    HTTP --> StreamUC

    ChatUC --> ProviderPort
    StreamUC --> ProviderPort
    ToolsUC --> ToolRegistryPort

    ProviderPort --> Domain

    OpenAI -.-> ProviderPort
    Anthropic -.-> ProviderPort
    Mock -.-> ProviderPort

    OpenAI --> OpenAIAPI
    Anthropic --> AnthropicAPI
    Mock --> InMemory
```

---

## 4. Diagrama de Sequencia — Chat Sync

```mermaid
sequenceDiagram
    participant User
    participant Client
    participant ChatUseCase
    participant Provider
    participant OpenAI as OpenAI API

    User->>Client: chat(msg)
    Client->>ChatUseCase: execute(dto)
    ChatUseCase->>Provider: chat(messages)
    Provider->>OpenAI: POST /responses
    OpenAI-->>Provider: response
    Provider-->>ChatUseCase: ChatResponse
    ChatUseCase-->>Client: ChatResponse
    Client-->>User: ChatResponse
```

---

## 5. Diagrama de Sequencia — Chat Streaming

```mermaid
sequenceDiagram
    participant User
    participant Client
    participant StreamUseCase
    participant Provider
    participant OpenAI as OpenAI API

    User->>Client: chat_stream()
    Client->>StreamUseCase: execute(dto)
    StreamUseCase->>Provider: chat_stream()
    Provider->>OpenAI: POST /responses (stream=true)

    loop SSE Chunks
        OpenAI-->>Provider: chunk
        Provider-->>StreamUseCase: chunk
        StreamUseCase-->>Client: chunk
        Client-->>User: chunk
    end

    OpenAI-->>Provider: [DONE]
    Provider-->>StreamUseCase: stream end
    StreamUseCase-->>Client: stream end
    Client-->>User: (stream end)
```

---

## 6. Diagrama de Sequencia — AutoFallback

```mermaid
sequenceDiagram
    participant User
    participant Client
    participant FallbackMgr as Fallback Manager
    participant OpenAI
    participant Anthropic

    User->>Client: chat(msg)
    Client->>FallbackMgr: try_providers()
    FallbackMgr->>OpenAI: chat(msg)
    OpenAI-->>FallbackMgr: ERROR

    Note over FallbackMgr: Log: fallback to Anthropic

    FallbackMgr->>Anthropic: chat(msg)
    Anthropic-->>FallbackMgr: ChatResponse
    FallbackMgr-->>Client: ChatResponse
    Client-->>User: ChatResponse
```

---

## 7. Integracao com MCP

```mermaid
flowchart TB
    subgraph ForgeLLMClient["ForgeLLMClient"]
        subgraph MCPClient["MCP Client"]
            connect["connect(server_url)"]
            list_tools["list_tools()"]
            call_tool["call_tool(name, args)"]
            list_resources["list_resources()"]
            read_resource["read_resource(uri)"]
        end
    end

    subgraph MCPServer["MCP Server"]
        Tools["Tools:<br/>calculadora, weather, search"]
        Resources["Resources:<br/>files, databases"]
        Prompts["Prompts:<br/>templates"]
    end

    MCPClient -->|"MCP Protocol<br/>(JSON-RPC)"| MCPServer
```

---

## 8. Arquitetura em Camadas

```mermaid
flowchart TB
    subgraph External["EXTERNAL"]
        User["Usuario/Cliente"]
    end

    subgraph Adapters["ADAPTERS LAYER"]
        direction LR
        CLI["CLI"]
        API["HTTP API"]
    end

    subgraph Application["APPLICATION LAYER"]
        direction LR
        UseCases["Use Cases"]
        Ports["Ports/Interfaces"]
        DTOs["DTOs"]
    end

    subgraph Domain["DOMAIN LAYER"]
        direction LR
        Entities["Entities"]
        ValueObjects["Value Objects"]
        Exceptions["Exceptions"]
    end

    subgraph Infrastructure["INFRASTRUCTURE LAYER"]
        direction LR
        Config["Config"]
        HTTP["HTTP Client"]
    end

    subgraph Providers["PROVIDERS LAYER"]
        direction LR
        OpenAI["OpenAI"]
        Anthropic["Anthropic"]
        Mock["Mock"]
    end

    External --> Adapters
    Adapters --> Application
    Application --> Domain
    Application --> Ports
    Infrastructure --> Ports
    Providers --> Ports
    Providers --> External2["External APIs"]

    style Domain fill:#e1f5fe
    style Application fill:#fff3e0
    style Infrastructure fill:#f3e5f5
    style Providers fill:#e8f5e9
```

---

## 9. Integracao com ForgeBase

O ForgeLLMClient segue a arquitetura ForgeBase:

### Classes Base Utilizadas

| ForgeLLMClient | ForgeBase Base |
|----------------|----------------|
| `ChatResponse` | `EntityBase` |
| `Message` | `ValueObjectBase` |
| `TokenUsage` | `ValueObjectBase` |
| `ChatUseCase` | `UseCaseBase` |
| `ProviderPort` | ABC |
| `OpenAIProvider` | Implementa `ProviderPort` |
| `ForgeError` | `DomainException` |

### Observabilidade

```python
from forgebase.observability import LogService, TrackMetrics

# Logging estruturado
log = LogService(service_name="forge-llm")
log.info("Chat request", provider="openai", model="gpt-4")

# Metricas
metrics = TrackMetrics()
metrics.increment("chat.requests", provider="openai")
with metrics.timer("chat.duration"):
    response = provider.chat(messages)
```

---

## 10. Decisoes Arquiteturais

| Aspecto | Decisao | ADR |
|---------|---------|-----|
| Arquitetura | Clean + Hexagonal (ForgeBase) | ADR-001 |
| Provedores | Plugin Architecture com ABC | ADR-002 |
| OpenAI API | Responses API (NUNCA ChatCompletions) | ADR-003 |
| HTTP Client | httpx (async) | ADR-004 |
| Estrutura | Monorepo src layout | ADR-005 |
| Metodologia | TDD | ADR-006 |

---

## 11. Referencias

- `specs/roadmap/ARCHITECTURAL_DECISIONS_APPROVED.md`
- `specs/roadmap/ADR.md`
- `docs/guides/forgebase_guides/referencia/arquitetura.md`
- `docs/visao.md`

---

*Documento gerado pelo Roadmap Planning Process*
