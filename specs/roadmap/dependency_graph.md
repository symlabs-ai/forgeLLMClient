# Grafo de Dependencias — ForgeLLMClient

> Mapeamento de dependencias entre features BDD

---

## Grafo de Features

```mermaid
flowchart TB
    subgraph Foundation["FUNDACAO"]
        config["config.feature<br/>@ci-fast"]
    end

    subgraph Core["CORE"]
        chat["chat.feature<br/>@ci-fast"]
    end

    subgraph Features["FEATURES"]
        response["response.feature<br/>@ci-fast"]
        tokens["tokens.feature<br/>@ci-fast"]
        tools["tools.feature<br/>@ci-fast"]
    end

    subgraph Future["FUTURO"]
        mcp["MCP"]
    end

    config --> chat
    chat --> response
    chat --> tokens
    chat --> tools
    tools -.-> mcp

    style config fill:#e8f5e9
    style chat fill:#fff3e0
    style response fill:#e3f2fd
    style tokens fill:#e3f2fd
    style tools fill:#e3f2fd
    style mcp fill:#f3e5f5,stroke-dasharray: 5 5
```

---

## Grafo de Provedores

```mermaid
flowchart TB
    subgraph Core["CORE"]
        chat["chat.feature<br/>(core)"]
    end

    subgraph Providers["PROVEDORES"]
        openai["openai.feature<br/>@ci-int"]
        anthropic["anthropic.feature<br/>@ci-int"]
    end

    chat --> openai
    chat --> anthropic

    style chat fill:#fff3e0
    style openai fill:#e8f5e9
    style anthropic fill:#fce4ec
```

---

## Ordem de Implementacao

### Sprint 1: Fundacao (P0 - CRITICO)

```mermaid
flowchart LR
    config["1. config.feature<br/>Configuracao base"]
    chat["2. chat.feature<br/>Chat sync/streaming"]
    response["3. response.feature<br/>Formato ChatResponse"]
    tokens["4. tokens.feature<br/>Contagem de tokens"]

    config --> chat
    chat --> response
    chat --> tokens
```

### Sprint 2: Tool Calling (P0 - CRITICO)

```mermaid
flowchart LR
    tools["5. tools.feature<br/>Tool calling normalizado"]
```

### Sprint 3: Provedores Reais (P1 - ALTO)

```mermaid
flowchart LR
    openai["6. openai.feature<br/>Integracao OpenAI<br/>(Responses API)"]
    anthropic["7. anthropic.feature<br/>Integracao Anthropic"]
```

---

## Matriz de Dependencias

| Feature | Depende de | Bloqueia |
|---------|------------|----------|
| config.feature | - | chat, response, tokens, tools |
| chat.feature | config | response, tokens, tools, openai, anthropic |
| response.feature | chat | - |
| tokens.feature | chat | - |
| tools.feature | chat | openai, anthropic |
| openai.feature | chat, tools | - |
| anthropic.feature | chat, tools | - |

---

## Caminho Critico

```mermaid
flowchart LR
    config["config"] --> chat["chat"] --> tools["tools"]
    tools --> openai["openai"]
    tools --> anthropic["anthropic"]

    style config fill:#ffcdd2
    style chat fill:#ffcdd2
    style tools fill:#ffcdd2
    style openai fill:#ffcdd2
    style anthropic fill:#ffcdd2
```

Todas as features neste caminho devem ser implementadas sequencialmente.

---

## Legenda

| Simbolo | Significado |
|---------|-------------|
| `@ci-fast` | Testes rapidos com mocks |
| `@ci-int` | Testes de integracao (API real) |
| `P0` | Prioridade critica |
| `P1` | Prioridade alta |

---

*Documento gerado pelo Roadmap Planning Process*
