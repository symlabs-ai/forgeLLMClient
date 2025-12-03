# 🗺️ Roadmap Planning Process

**Subprocesso do Execution Process – da especificação (BDD) ao backlog executável.**

---

## 🌟 Visão Geral

O **Roadmap Planning** é a fase de planejamento executivo que transforma features Gherkin em um backlog sequencial e executável. Ele é a **primeira subetapa** do
`process/execution/PROCESS.md` e responde:

- **QUANDO** cada feature será implementada?
- **EM QUE ORDEM** as tarefas devem ser executadas?
- **QUANTO ESFORÇO** cada item demanda?
- **QUEM** é responsável por cada track?
- **COMO** medir progresso?

```
BDD (O QUÊ fazer) → ROADMAP PLANNING (QUANDO/COMO) → TDD (Implementar)
     ↓                         ↓                            ↓
specs/bdd/*.feature      ROADMAP.md + BACKLOG         forge/* código
"Comportamento"          "Planejamento"               "Implementação"
```

---

## 🎯 Propósito do Roadmap Planning

**Não é** sobre tecnologia. **É** sobre:
- Sequenciar features por dependência e valor
- Quebrar features complexas em tarefas menores
- Estimar esforço e alocar recursos
- Criar backlog vivo que evolui durante TDD
- Dar visibilidade de progresso para stakeholders

**Entrada**: Features BDD prontas (Etapa 6 completa)
**Saída**: Roadmap executável + Backlog priorizado

---

## 📖 As Seis Subetapas do Roadmap Planning

```
┌─────────────────────────────────────────────────────────┐
│ 0. Validação Arquitetural com Stakeholders ⭐ NOVO    │
│    "Apresentar propostas e obter aprovação"            │
└────────────────┬────────────────────────────────────────┘
                 │ Alinhamento e Aprovação
                 ▼
┌─────────────────────────────────────────────────────────┐
│ 1. Definição Arquitetural e Stack (ADR)               │
│    "Decisões técnicas fundamentais APROVADAS"          │
└────────────────┬────────────────────────────────────────┘
                 │ Fundação Técnica
                 ▼
┌─────────────────────────────────────────────────────────┐
│ 2. Análise de Dependências                            │
│    "Identificar ordem técnica obrigatória"             │
└────────────────┬────────────────────────────────────────┘
                 │ Mapeamento: Feature → Dependências
                 ▼
┌─────────────────────────────────────────────────────────┐
│ 3. Quebra de Features (Feature Breakdown)             │
│    "Dividir features grandes em tarefas menores"       │
└────────────────┬────────────────────────────────────────┘
                 │ Granularização
                 ▼
┌─────────────────────────────────────────────────────────┐
│ 4. Estimativa e Priorização                           │
│    "Estimar esforço e ordenar por valor/dependência"   │
└────────────────┬────────────────────────────────────────┘
                 │ Planejamento
                 ▼
┌─────────────────────────────────────────────────────────┐
│ 5. Criação do Roadmap e Backlog                       │
│    "Gerar documentos executáveis (ROADMAP + BACKLOG)"  │
└─────────────────────────────────────────────────────────┘
```

---

## 🗂️ Estrutura de Saída Esperada

> **Estrutura alvo em projetos ForgeProcess**
> Os caminhos abaixo representam a organização **esperada** em um projeto real que adota o ForgeProcess.
> Este repositório não contém `specs/roadmap` nem outros diretórios de código; eles serão criados
> por ferramentas como `symforge init -p forgeprocess myproject` ou por scaffolding equivalente.

Ao final do Roadmap Planning, um projeto típico terá:

```
specs/
 └── roadmap/
      ├── TECH_STACK.md           ← Stack completo (libs, versões, ferramentas)
      ├── ADR.md                  ← Índice de Architecture Decision Records
      ├── adr/                    ← ADRs individuais
      │   ├── ADR-001.md         (Framework HTTP)
      │   ├── ADR-002.md         (Plugin Architecture)
      │   └── ADR-00N.md         (etc)
      ├── HLD.md                  ← High Level Design (arquitetura macro) ⭐
      ├── LLD.md                  ← Low Level Design (classes, fluxos) ⭐
      ├── ROADMAP.md              ← Visão executiva (fases, marcos, datas)
      ├── BACKLOG.md              ← Backlog detalhado (tarefas priorizadas)
      ├── dependency_graph.md     ← Grafo de dependências (Mermaid)
      └── estimates.yml           ← Estimativas de esforço por feature
```

---

## 🔹 Subetapa 0: Validação Arquitetural com Stakeholders ⭐ NOVA

### Objetivo
**Apresentar propostas técnicas e obter validação/aprovação ANTES de tomar decisões definitivas.**

### Por que esta subetapa é crítica?

❌ **Problema comum**: Equipe técnica toma decisões arquiteturais sem consultar stakeholders, resultando em:
- Retrabalho custoso quando stakeholders discordam
- Decisões que não alinham com restrições de negócio (budget, prazos, skills do time)
- Falta de buy-in dos stakeholders

✅ **Solução**: Criar questionário de validação arquitetural para apresentar **propostas fundamentadas** e obter aprovação.

### Processo

#### 0.1 Análise Preparatória (Claude/IA)

Antes de perguntar ao stakeholder, a IA deve:
1. Analisar `project/docs/visao.md` (problema, solução, métricas)
2. Revisar `specs/bdd/*.feature` (casos de uso técnicos)
3. Revisar `specs/bdd/tracks.yml` (ValueTracks e métricas)
4. Identificar constraints técnicos (BDD já definiu comportamentos esperados)

#### 0.2 Esboçar Propostas Técnicas

Com base na análise, a IA esboça propostas para:
- **Stack tecnológico** (linguagem, frameworks, libs principais)
- **Arquitetura macro** (monolito, microserviços, plugins, etc)
- **Modelo de concorrência** (sync, async, threads, etc)
- **Infraestrutura** (cloud, on-premise, containers, etc)
- **Estratégia de deployment** (Docker, K8s, serverless, etc)

**Formato das propostas**: Para cada decisão, apresentar 2-3 alternativas com trade-offs claros.

#### 0.3 Criar Questionário de Validação

**Criar**: `specs/roadmap/ARCHITECTURAL_QUESTIONNAIRE.md`

O questionário deve conter:
- **Proposta principal** (recomendação da IA)
- **Alternativas consideradas** (com prós/contras)
- **Perguntas de validação** (para stakeholder responder)
- **Trade-offs explícitos** (custo vs. performance, simplicidade vs. flexibilidade, etc)

#### 0.4 Apresentar ao Stakeholder

**Formato sugerido**:
```markdown
## Decisão 1: Stack Backend

### Proposta Principal (Recomendada)
**Python 3.11+ com FastAPI**

**Por quê?**
- Requisito explícito: "módulo Python instalável via pip"
- FastAPI: async nativo, OpenAPI automático, validação Pydantic
- Ecossistema ML/LLM maduro em Python

**Trade-offs**:
- ✅ Prós: Rápido para MVP, ótima DX, type-safe
- ❌ Contras: Performance inferior a Go/Rust, GIL pode limitar concorrência CPU-bound

### Alternativas Consideradas

#### Alt 1: Node.js + Express
- ✅ Prós: Async nativo, npm ecosystem, performance excelente I/O
- ❌ Contras: Não atende requisito "módulo Python", menos natural para ML

#### Alt 2: Go + net/http
- ✅ Prós: Performance, concorrência nativa (goroutines)
- ❌ Contras: Não atende requisito "módulo Python", curva aprendizado

### ❓ Perguntas para Stakeholder

1. **Confirma requisito**: O SDK DEVE ser Python? Ou pode ser language-agnostic desde o início?
   - [ ] Sim, DEVE ser Python (conforme visao.md)
   - [ ] Podemos reconsiderar outra linguagem

2. **Performance vs. Simplicidade**: Você prioriza:
   - [ ] Simplicidade/velocidade de desenvolvimento (Python)
   - [ ] Performance máxima (Go/Rust)
   - [ ] Ambos igualmente (explicar trade-off)

3. **Skills do time**: Time atual tem experiência em:
   - [ ] Python (pronto para começar)
   - [ ] Outra linguagem (especificar)
```

#### 0.5 Aguardar Aprovação

**IMPORTANTE**: **NÃO PROSSEGUIR** para Subetapa 1 sem aprovação explícita do stakeholder!

Aguardar respostas no questionário. Stakeholder pode:
- ✅ Aprovar proposta
- 🔄 Solicitar ajustes
- ❌ Rejeitar e propor alternativa

#### 0.6 Consolidar Decisões Aprovadas

Após aprovação, criar `specs/roadmap/ARCHITECTURAL_DECISIONS_APPROVED.md` com:
- Decisões aprovadas pelo stakeholder
- Data de aprovação
- Nome do stakeholder aprovador
- Justificativas finais

**Somente após este documento criado**, prosseguir para Subetapa 1.

---

## 🔹 Subetapa 1: Definição Arquitetural e Stack (ADR)

### Objetivo
**Documentar decisões técnicas APROVADAS** na Subetapa 0 em formato ADR (Architecture Decision Record).

### Por que ADR (Architecture Decision Records)?
- **Rastreabilidade**: Por QUE escolhemos X ao invés de Y?
- **Onboarding**: Novos desenvolvedores entendem decisões passadas
- **Evita debates repetidos**: Decisão já foi tomada e documentada
- **Accountability**: Quem decidiu, quando, com base em quê?

### Processo

#### 1.1 Definir Stack Tecnológico

**Perguntas a responder**:
- Qual versão do Python? (3.11+, 3.12+?)
- Quais bibliotecas core? (httpx, pydantic, pytest-bdd, etc)
- Qual framework HTTP? (FastAPI, Flask, Starlette?)
- Qual biblioteca para STDIO/JSON-RPC? (Custom, python-jsonrpc?)
- Como gerenciar dependências? (poetry, pip-tools, uv?)
- Qual ferramenta de build? (setuptools, hatch, flit?)
- Type checking? (mypy, pyright?)
- Linting? (ruff, pylint, flake8?)
- Formatação? (black, ruff format?)

**Criar**: `specs/roadmap/TECH_STACK.md`

**Exemplo**:
```markdown
# Tech Stack — forgeLLMClient

## Python Core
- **Versão**: Python 3.11+ (3.12 recomendado)
- **Justificativa**: Type hints melhoradas, performance, suporte LTS

## Bibliotecas Principais

### SDK (Forge)
- **httpx** (0.27+): Cliente HTTP assíncrono para provedores cloud
- **pydantic** (2.0+): Validação de dados e schemas
- **typing-extensions**: Backport de tipos para 3.11

### Servidor (SymClient)
- **FastAPI** (0.110+): Framework HTTP com OpenAPI automático
- **uvicorn** (0.28+): ASGI server para produção
- **python-multipart**: Upload de arquivos (se necessário)

### JSON-RPC (STDIO)
- **jsonrpc-base** + custom wrapper: Protocolo STDIO
- **Justificativa**: Biblioteca leve, controle total do protocolo

### Testes
- **pytest** (8.0+): Framework de testes
- **pytest-bdd** (7.0+): Suporte a Gherkin
- **pytest-asyncio** (0.23+): Testes async
- **pytest-cov**: Cobertura de código

### Dev Tools
- **ruff** (0.3+): Linting + formatação (substitui black + flake8)
- **mypy** (1.9+): Type checking estático
- **pre-commit**: Git hooks
- **uv** ou **poetry**: Gerenciamento de dependências

## Estrutura de Projeto

```
forge/
├── pyproject.toml           # Configuração central (PEP 621)
├── src/
│   ├── forge/              # SDK Python
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── chat.py
│   │   ├── providers/      # Plugins de provedores
│   │   └── utils/
│   └── symclient/          # Servidor HTTP/STDIO
│       ├── __init__.py
│       ├── http.py         # FastAPI app
│       └── stdio.py        # JSON-RPC handler
├── tests/
│   ├── bdd/                # Tests pytest-bdd
│   └── unit/               # Unit tests
└── specs/
    └── bdd/                # Features Gherkin
```

## Decisões Arquiteturais (ver ADR.md)
```

---

#### 1.2 Criar Architecture Decision Records (ADRs)

Para **cada decisão arquitetural importante**, criar um ADR seguindo formato padrão.

**Template ADR**:
```markdown
# ADR-001: [Título da Decisão]

**Status**: [Proposto | Aceito | Rejeitado | Superseded]
**Data**: AAAA-MM-DD
**Decisores**: [@tech-lead, @dev1, @dev2]

## Contexto

[Por que precisamos tomar essa decisão? Qual o problema?]

## Decisão

[O que decidimos fazer?]

## Alternativas Consideradas

1. **Opção A**: [Descrição]
   - ✅ Prós: ...
   - ❌ Contras: ...

2. **Opção B**: [Descrição] ← **ESCOLHIDA**
   - ✅ Prós: ...
   - ❌ Contras: ...

3. **Opção C**: [Descrição]
   - ✅ Prós: ...
   - ❌ Contras: ...

## Consequências

### Positivas
- [Benefício 1]
- [Benefício 2]

### Negativas
- [Trade-off 1]
- [Trade-off 2]

## Validação

Como saberemos se foi a decisão correta?
- [Critério 1]
- [Critério 2]

## Referências

- [Link para discussão no GitHub]
- [Documento técnico]
```

**Criar**: `specs/roadmap/ADR.md` (índice) + `specs/roadmap/adr/ADR-001.md`, `ADR-002.md`, etc.

---

### Exemplos de ADRs Necessários para Forge

#### ADR-001: Usar FastAPI para SymClient HTTP

**Contexto**: Precisamos expor Forge via HTTP. Opções: FastAPI, Flask, Django.

**Decisão**: Usar **FastAPI**

**Alternativas**:
- Flask: Mais simples, mas sem async nativo e OpenAPI manual
- Django: Muito pesado para servidor stateless
- **FastAPI**: Async nativo, OpenAPI automático, validação Pydantic

**Consequências**:
- ✅ OpenAPI docs automático (`/docs`)
- ✅ Async de primeira classe
- ✅ Validação de schemas via Pydantic
- ❌ Curva de aprendizado maior que Flask

---

#### ADR-002: Plugin Architecture para Provedores

**Contexto**: Múltiplos provedores (OpenRouter, llama.cpp, echo) com capacidades diferentes.

**Decisão**: Arquitetura de **plugins** com interface `Provider` base.

**Alternativas**:
- Hard-coded if/else: Não escalável
- **Plugin system com ABC**: Extensível, testável
- Biblioteca third-party: Dependência extra

**Consequências**:
- ✅ Fácil adicionar novos provedores
- ✅ Testes isolados por provider
- ✅ Fallback strategies isoladas
- ❌ Overhead inicial de abstração

**Interface**:
```python
class Provider(ABC):
    @abstractmethod
    async def chat(self, messages: list[Message]) -> ChatResponse:
        ...

    @property
    @abstractmethod
    def supports_tool_calling(self) -> bool:
        ...
```

---

#### ADR-003: Usar pytest-bdd para Automação BDD

**Contexto**: Features Gherkin existem. Precisamos automatizar.

**Decisão**: **pytest-bdd**

**Alternativas**:
- behave: Python puro, mas ecosistema menor
- **pytest-bdd**: Integra com pytest (já usamos)
- Robot Framework: Muito verboso

**Consequências**:
- ✅ Usa infraestrutura pytest existente
- ✅ Fixtures compartilhadas
- ✅ Plugins pytest (cov, asyncio, etc)
- ❌ Sintaxe decorators pode confundir iniciantes

---

#### ADR-004: Gerenciamento de Dependências com UV

**Contexto**: Escolher entre pip-tools, poetry, uv.

**Decisão**: **uv** (https://github.com/astral-sh/uv)

**Alternativas**:
- pip-tools: Funciona, mas lento
- poetry: Bom, mas reinventa wheels
- **uv**: Rápido (Rust), compatível com pip, futuro do Python

**Consequências**:
- ✅ 10-100x mais rápido que pip
- ✅ Lock file automático
- ✅ Compatível com requirements.txt
- ❌ Ferramenta nova (risco de bugs)

---

#### ADR-005: Estrutura Monorepo vs Multi-repo

**Contexto**: Forge (SDK) e SymClient (servidor) no mesmo repo ou separados?

**Decisão**: **Monorepo** (mesmo repositório)

**Alternativas**:
- Multi-repo: Versionamento independente
- **Monorepo**: Compartilha código, sincroniza versões

**Consequências**:
- ✅ Código compartilhado (types, utils)
- ✅ Testes integrados
- ✅ Versionamento sincronizado
- ❌ Releases acopladas

**Estrutura**:
```
src/
├── forge/          # SDK (publicado no PyPI)
└── symclient/      # Servidor (container/binary)
```

---

---

#### 1.3 Criar Diagramas de Arquitetura (HLD e LLD)

Decisões arquiteturais devem ser **visualizadas** para facilitar compreensão e comunicação.

### HLD (High Level Design) - Visão Macro

**Objetivo**: Mostrar componentes principais, integrações externas, fluxos de dados de alto nível.

**Criar**: `specs/roadmap/HLD.md`

**Exemplo para Forge**:

```markdown
# HLD — Forge & SymClient Architecture

## Componentes Principais

```mermaid
C4Context
    title Sistema Forge - Contexto

    Person(dev, "Desenvolvedor", "Integra LLMs em sua aplicação")

    System_Boundary(forge_system, "Forge Ecosystem") {
        System(forge_sdk, "Forge SDK", "SDK Python - Interface unificada")
        System(symclient, "SymClient", "Servidor HTTP/STDIO")
    }

    System_Ext(openrouter, "OpenRouter API", "Provedor LLM Cloud")
    System_Ext(llama, "llama.cpp", "Provedor LLM Local")
    System_Ext(mcp, "MCP Tecnospeed", "Marketplace de Serviços")

    Rel(dev, forge_sdk, "Usa", "Python import")
    Rel(dev, symclient, "Usa", "HTTP/STDIO")

    Rel(forge_sdk, openrouter, "Chama", "HTTPS")
    Rel(forge_sdk, llama, "Chama", "Native bindings")
    Rel(symclient, forge_sdk, "Usa internamente")
    Rel(symclient, mcp, "Integra", "MCP Protocol")
```

## Arquitetura de Plugins

```mermaid
graph TB
    subgraph "Forge SDK"
        CORE[Forge Core]
        CONFIG[Config Manager]
        SESSION[Session Manager]

        subgraph "Provider Plugins"
            ECHO[Echo Provider]
            OPENROUTER[OpenRouter Provider]
            LLAMA[Llama.cpp Provider]
        end

        subgraph "Capability Handlers"
            TOOL[Tool Calling Handler]
            STREAM[Streaming Handler]
            FALLBACK[Fallback Strategy]
        end
    end

    subgraph "SymClient"
        HTTP[FastAPI HTTP Server]
        STDIO[JSON-RPC STDIO Server]
        MCP_CONN[MCP Connector]
    end

    CORE --> CONFIG
    CORE --> SESSION
    CORE --> ECHO
    CORE --> OPENROUTER
    CORE --> LLAMA

    TOOL --> FALLBACK
    STREAM --> FALLBACK

    HTTP --> CORE
    STDIO --> CORE
    MCP_CONN --> CORE

    style CORE fill:#4CAF50
    style HTTP fill:#2196F3
    style STDIO fill:#2196F3
```

## Fluxo de Dados - Chat Request

```mermaid
sequenceDiagram
    actor Dev as Desenvolvedor
    participant SDK as Forge SDK
    participant Config as Config Manager
    participant Provider as Provider Plugin
    participant LLM as OpenRouter API

    Dev->>SDK: forge.chat("Hello")
    SDK->>Config: load_config()
    Config-->>SDK: provider="openrouter"

    SDK->>Provider: get_provider("openrouter")
    Provider-->>SDK: OpenRouterProvider instance

    SDK->>Provider: chat(messages)
    Provider->>LLM: POST /api/v1/chat/completions
    LLM-->>Provider: {"choices": [...]}
    Provider-->>SDK: ChatResponse(content="Hi!")
    SDK-->>Dev: ChatResponse
```

## Integrações Externas

| Componente | Protocolo | Autenticação | Observações |
|------------|-----------|--------------|-------------|
| OpenRouter API | HTTPS/REST | API Key (Bearer) | Rate limits aplicam |
| llama.cpp | Native C bindings | N/A | Execução local |
| MCP Tecnospeed | MCP Protocol | OAuth 2.0 | Staging + Prod |
| LLM Broker | HTTPS/REST | JWT | Roteamento inteligente |
```

**Elementos de um bom HLD**:
- ✅ Diagrama C4 Context (contexto geral)
- ✅ Diagrama de componentes (módulos principais)
- ✅ Diagrama de sequência (fluxos principais)
- ✅ Integrações externas (protocolos, auth)
- ✅ Decisões arquiteturais resumidas

---

### LLD (Low Level Design) - Visão Detalhada

**Objetivo**: Mostrar estrutura interna de módulos, classes, interfaces, padrões de design.

**Criar**: `specs/roadmap/LLD.md`

**Exemplo para Forge**:

```markdown
# LLD — Forge & SymClient Detailed Design

## Módulo: Forge SDK Core

### Estrutura de Classes

```mermaid
classDiagram
    class Forge {
        -config: Config
        -provider_registry: ProviderRegistry
        -session_manager: SessionManager
        +chat(messages: List[Message]) ChatResponse
        +stream_chat(messages) AsyncIterator
        +register_tool(tool: Tool) None
    }

    class Config {
        +provider: str
        +api_key: str
        +model: str
        +load_from_env() Config
        +load_from_file(path) Config
        +validate() None
    }

    class ProviderRegistry {
        -providers: Dict[str, Provider]
        +register(name: str, provider: Provider)
        +get(name: str) Provider
        +list_available() List[str]
    }

    class Provider {
        <<abstract>>
        +chat(messages) ChatResponse
        +supports_tool_calling: bool
        +supports_streaming: bool
    }

    class OpenRouterProvider {
        -api_key: str
        -base_url: str
        +chat(messages) ChatResponse
        +supports_tool_calling: True
    }

    class EchoProvider {
        +chat(messages) ChatResponse
        +supports_tool_calling: False
    }

    class SessionManager {
        -sessions: Dict[str, Session]
        +create_session(id: str) Session
        +get_session(id: str) Session
        +add_message(session_id, message)
    }

    Forge --> Config
    Forge --> ProviderRegistry
    Forge --> SessionManager
    ProviderRegistry --> Provider
    Provider <|-- OpenRouterProvider
    Provider <|-- EchoProvider
```

### Interface: Provider (ABC)

```python
from abc import ABC, abstractmethod
from typing import List, AsyncIterator

class Provider(ABC):
    """
    Interface base para todos os provedores de LLM.

    Implementações devem fornecer chat() e declarar capacidades.
    """

    @abstractmethod
    async def chat(
        self,
        messages: List[Message],
        **kwargs
    ) -> ChatResponse:
        """
        Envia mensagens ao LLM e retorna resposta.

        Args:
            messages: Lista de mensagens (user/assistant/system)
            **kwargs: Parâmetros específicos do provider

        Returns:
            ChatResponse com content, model, usage

        Raises:
            ProviderError: Erro de comunicação com LLM
            AuthenticationError: Credenciais inválidas
        """
        pass

    @property
    @abstractmethod
    def supports_tool_calling(self) -> bool:
        """Indica se provider suporta tool calling nativo."""
        pass

    @property
    @abstractmethod
    def supports_streaming(self) -> bool:
        """Indica se provider suporta streaming."""
        pass
```

### Padrão de Design: Strategy (Fallback)

```mermaid
classDiagram
    class ToolCallingHandler {
        -provider: Provider
        -fallback_strategy: FallbackStrategy
        +execute_tool(tool, args) ToolResult
    }

    class FallbackStrategy {
        <<interface>>
        +execute(tool, args, messages) ToolResult
    }

    class NativeToolCalling {
        +execute(tool, args, messages) ToolResult
    }

    class EmulatedToolCalling {
        -llm: Provider
        +execute(tool, args, messages) ToolResult
    }

    ToolCallingHandler --> FallbackStrategy
    FallbackStrategy <|-- NativeToolCalling
    FallbackStrategy <|-- EmulatedToolCalling
```

**Lógica de seleção**:
```python
class ToolCallingHandler:
    def execute_tool(self, tool: Tool, args: dict) -> ToolResult:
        if self.provider.supports_tool_calling:
            strategy = NativeToolCalling(self.provider)
        else:
            strategy = EmulatedToolCalling(self.provider)
            self.logger.info("Using fallback strategy: emulated")

        return strategy.execute(tool, args, self.messages)
```

---

## Módulo: SymClient HTTP Server

### Estrutura de Rotas (FastAPI)

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="SymClient HTTP API")

class ChatRequest(BaseModel):
    provider: str
    model: str
    messages: List[dict]
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    content: str
    model: str
    usage: dict

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Chat endpoint - expõe Forge SDK via HTTP.

    Flow:
    1. Validar request (Pydantic)
    2. Instanciar Forge com config
    3. Chamar forge.chat()
    4. Retornar response
    """
    forge = Forge(provider=request.provider, model=request.model)
    response = await forge.chat(request.messages)
    return ChatResponse(
        content=response.content,
        model=response.model,
        usage=response.usage
    )
```

### Middleware: Correlation ID

```mermaid
sequenceDiagram
    participant Client
    participant Middleware as CorrelationMiddleware
    participant Endpoint as /chat
    participant Logger

    Client->>Middleware: Request
    Middleware->>Middleware: Generate UUID
    Middleware->>Logger: log("request", correlation_id)
    Middleware->>Endpoint: Request + correlation_id
    Endpoint->>Middleware: Response
    Middleware->>Logger: log("response", correlation_id)
    Middleware->>Client: Response + X-Correlation-ID header
```

**Implementação**:
```python
import uuid
from starlette.middleware.base import BaseHTTPMiddleware

class CorrelationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        correlation_id = str(uuid.uuid4())
        request.state.correlation_id = correlation_id

        logger.info(f"Request received", extra={
            "correlation_id": correlation_id,
            "method": request.method,
            "path": request.url.path
        })

        response = await call_next(request)
        response.headers["X-Correlation-ID"] = correlation_id

        logger.info(f"Response sent", extra={
            "correlation_id": correlation_id,
            "status_code": response.status_code
        })

        return response
```

---

## Módulo: Configuration Management

### Precedência de Configuração

```mermaid
graph LR
    ENV[Environment Variables] -->|Highest Priority| MERGE[Config Merge]
    FILE[Config File .forgerc] -->|Medium Priority| MERGE
    DEFAULT[Defaults] -->|Lowest Priority| MERGE

    MERGE --> FINAL[Final Config]

    style ENV fill:#4CAF50
    style FILE fill:#FFC107
    style DEFAULT fill:#9E9E9E
    style FINAL fill:#2196F3
```

**Implementação**:
```python
from dataclasses import dataclass
from typing import Optional
import os
import json

@dataclass
class Config:
    provider: str = "echo"
    api_key: Optional[str] = None
    model: str = "default"

    @classmethod
    def load(cls) -> "Config":
        # 1. Start with defaults
        config = cls()

        # 2. Merge from file (if exists)
        # Opções: .forgerc (JSON), .env, ou pyproject.toml [tool.forge]
        if os.path.exists(".forgerc"):
            with open(".forgerc") as f:
                file_config = json.load(f)
                for key, value in file_config.items():
                    setattr(config, key, value)

        # 3. Override with env vars (highest priority)
        if env_provider := os.getenv("FORGE_PROVIDER"):
            config.provider = env_provider
        if env_key := os.getenv("FORGE_API_KEY"):
            config.api_key = env_key

        # 4. Validate
        config.validate()
        return config

    def validate(self):
        if self.provider == "openrouter" and not self.api_key:
            raise ConfigurationError(
                "API key obrigatória para provedor openrouter"
            )
```

---

## Padrões de Erro

### Hierarquia de Exceções

```mermaid
classDiagram
    class ForgeError {
        <<Exception>>
        +message: str
        +context: dict
    }

    class ConfigurationError {
        +missing_field: str
    }

    class AuthenticationError {
        +provider: str
    }

    class ProviderError {
        +provider: str
        +status_code: int
    }

    class SessionNotFoundError {
        +session_id: str
    }

    class ToolNotFoundError {
        +tool_name: str
        +available_tools: List[str]
    }

    ForgeError <|-- ConfigurationError
    ForgeError <|-- AuthenticationError
    ForgeError <|-- ProviderError
    ForgeError <|-- SessionNotFoundError
    ForgeError <|-- ToolNotFoundError
```

**Tratamento centralizado**:
```python
@app.exception_handler(ForgeError)
async def forge_error_handler(request, exc: ForgeError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.__class__.__name__,
            "message": exc.message,
            "context": exc.context
        }
    )
```
```

**Elementos de um bom LLD**:
- ✅ Diagrama de classes (UML)
- ✅ Interfaces e ABCs documentadas
- ✅ Padrões de design aplicados (Strategy, Factory, etc)
- ✅ Fluxos de dados detalhados (sequência)
- ✅ Estrutura de pastas e módulos
- ✅ Hierarquia de erros
- ✅ Exemplos de código (pseudo-código ou Python)

---

### Saídas da Subetapa 1

- ✅ `specs/roadmap/TECH_STACK.md` — Stack completo documentado
- ✅ `specs/roadmap/ADR.md` — Índice de ADRs
- ✅ `specs/roadmap/adr/ADR-001.md` até `ADR-00N.md` — Decisões individuais
- ✅ `specs/roadmap/HLD.md` — High Level Design (arquitetura macro) ⭐ **NOVO**
- ✅ `specs/roadmap/LLD.md` — Low Level Design (classes, interfaces, fluxos) ⭐ **NOVO**
- ✅ Consenso técnico entre tech lead e time

**Próximo passo**: Subetapa 2 (Análise de Dependências) já sabendo COMO vamos implementar.

---

## 🔹 Subetapa 2: Análise de Dependências

### Objetivo
Identificar quais features dependem de outras para definir ordem técnica obrigatória.

### Processo

1. **Listar todas as features** de `specs/bdd/tracks.yml`
2. **Identificar dependências técnicas**:
   - `config.feature` é pré-requisito de TODAS (configuração base)
   - `chat.feature` é pré-requisito de `sessao.feature` (contexto depende de chat)
   - `chat_http.feature` depende de `chat.feature` (exposição via HTTP)
   - `errors.feature` pode ser paralelo
   - etc.

3. **Criar grafo de dependências** (Mermaid)

### Saída
`specs/roadmap/dependency_graph.md`

**Exemplo**:
```mermaid
graph TD
    CONFIG[config.feature] --> CHAT[chat.feature]
    CONFIG --> HTTP[chat_http.feature]
    CONFIG --> STDIO[ping_chat.feature]

    CHAT --> SESSION[sessao.feature]
    CHAT --> HTTP
    CHAT --> STDIO

    CHAT --> STREAMING[streaming.feature]
    CHAT --> TOOLCALLING[tool_calling_fallback.feature]

    HTTP --> HTTP_ERR[errors.feature HTTP]
    STDIO --> STDIO_ERR[errors.feature STDIO]

    CHAT --> LOGS[logs_metrics.feature]
    LOGS --> REDACT[redaction.feature]
```

---

## 🔹 Subetapa 2: Quebra de Features (Feature Breakdown)

### Objetivo
Dividir features grandes (> 3 cenários ou > 5 dias de esforço) em tarefas implementáveis.

### Processo

1. **Revisar cada feature** de `specs/bdd/`
2. **Identificar features complexas** que precisam quebra:
   - `tool_calling_fallback.feature` → pode ser quebrado em "tool calling nativo" + "fallback emulado"
   - `marketplace.feature` → pode ser quebrado em "conexão MCP" + "invocar serviços"

3. **Quebrar em tarefas** mantendo rastreabilidade:

**Exemplo** (`tool_calling_fallback.feature`):
```markdown
### Feature: tool_calling_fallback.feature

**Tarefas derivadas**:
1. [TASK-001] Implementar interface `Tool` base
2. [TASK-002] Implementar executor de tool calling nativo (OpenRouter)
3. [TASK-003] Implementar estratégia de fallback (prompt engineering)
4. [TASK-004] Registrar métricas de fallback
5. [TASK-005] Integrar com step definitions BDD
```

### Saída
Seção "Feature Breakdown" em `specs/roadmap/BACKLOG.md`

---

## 🔹 Subetapa 3: Estimativa e Priorização

### Objetivo
Estimar esforço de cada item e ordenar por:
1. **Dependências técnicas** (bloqueadores)
2. **Valor de negócio** (ValueTrack vs SupportTrack)
3. **Risco técnico** (complexidade)

### Processo

1. **Estimar esforço** (Planning Poker, T-shirt sizes, ou pontos):
   - XS: < 1 dia
   - S: 1-2 dias
   - M: 3-5 dias
   - L: 1-2 semanas
   - XL: > 2 semanas (QUEBRAR!)

2. **Aplicar framework de priorização**:

| Feature | Dependências | Valor | Risco | Esforço | Prioridade |
|---------|--------------|-------|-------|---------|------------|
| config.feature | NENHUMA | CRÍTICO | Baixo | S | P0 (Sprint 1) |
| chat.feature | config | ALTO | Baixo | M | P0 (Sprint 1) |
| sessao.feature | chat | MÉDIO | Médio | M | P1 (Sprint 2) |
| tool_calling_fallback | chat | ALTO | ALTO | L | P2 (Sprint 3) |

3. **Definir sprints/fases**:
   - **Sprint 1 (P0)**: MVP funcional (config + chat básico)
   - **Sprint 2 (P1)**: Robustez (sessão + errors)
   - **Sprint 3 (P2)**: Capacidades avançadas (fallback + streaming)
   - **Sprint 4 (P3)**: Ecossistema (MCP + Broker)

### Saída
`specs/roadmap/estimates.yml`

**Exemplo**:
```yaml
features:
  - id: config.feature
    effort: S (1-2 dias)
    risk: LOW
    dependencies: []
    sprint: 1
    priority: P0

  - id: chat.feature
    effort: M (3-5 dias)
    risk: LOW
    dependencies: [config.feature]
    sprint: 1
    priority: P0

  - id: tool_calling_fallback.feature
    effort: L (1-2 semanas)
    risk: HIGH
    dependencies: [chat.feature]
    sprint: 3
    priority: P2
    tasks:
      - TASK-001: Interface Tool base (S)
      - TASK-002: Tool calling nativo (M)
      - TASK-003: Fallback strategy (L)
      - TASK-004: Métricas (XS)
```

---

## 🔹 Subetapa 4: Criação do Roadmap e Backlog

### Objetivo
Gerar documentos executáveis que guiam a implementação TDD.

### Processo

1. **Criar ROADMAP.md** (visão executiva para stakeholders):
   - Timeline visual (Gantt)
   - Marcos (milestones)
   - Critérios de conclusão por fase
   - Riscos e mitigações

2. **Criar BACKLOG.md** (guia operacional para desenvolvedores):
   - Lista priorizada de tarefas
   - Links para features BDD
   - Critérios de aceitação (DoD)
   - Responsáveis

### Saída

#### `specs/roadmap/ROADMAP.md`
```markdown
# TDD Roadmap — forgeLLMClient

## Timeline

**Sprint 1 (Semanas 1-2)**: MVP Funcional
- ✅ config.feature → Configuração base
- ✅ chat.feature → Chat SDK Python
- ✅ chat_http.feature → Exposição HTTP
- ✅ ping_chat.feature → Exposição STDIO

**Milestone 1**: Desenvolvedor consegue enviar mensagem e receber resposta

**Sprint 2 (Semanas 3-4)**: Robustez
- ✅ sessao.feature → Contexto multi-turn
- ✅ errors.feature (HTTP/STDIO) → Tratamento de erros

**Milestone 2**: Sistema robusto com sessões e erros claros

## Riscos

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| Integração com llama.cpp complexa | MÉDIA | ALTO | Começar com echo provider, adiar llama.cpp |
| Fallback de tool calling difícil | ALTA | MÉDIO | Spike técnico na semana 2 |
```

#### `specs/roadmap/BACKLOG.md`
```markdown
# Backlog de Implementação — forgeLLMClient

## Sprint 1: MVP Funcional

### P0 - CRÍTICO

#### [FEATURE-001] config.feature
**Track**: `value_forge_symclient_baseline`
**Esforço**: S (1-2 dias)
**Responsável**: @dev-team
**Feature BDD**: `specs/bdd/10_forge_core/config.feature`

**Tarefas**:
- [ ] [TASK-001.1] Implementar `forge/config.py` com precedência env > file > defaults
- [ ] [TASK-001.2] Implementar validação de credenciais (ConfigurationError)
- [ ] [TASK-001.3] Remover @skip de cenários BDD
- [ ] [TASK-001.4] Fazer testes passarem (Green)
- [ ] [TASK-001.5] Refatorar (se necessário)

**DoD**:
- [x] Todos os cenários de `config.feature` passam
- [x] Código segue padrões (linting, typing)
- [x] PR criado com template de HANDOFF.md

---

#### [FEATURE-002] chat.feature
**Track**: `value_forge_symclient_baseline`
**Esforço**: M (3-5 dias)
**Dependências**: FEATURE-001
**Responsável**: @dev-team
**Feature BDD**: `specs/bdd/10_forge_core/chat.feature`

**Tarefas**:
- [ ] [TASK-002.1] Implementar `forge/chat.py` com método `chat()`
- [ ] [TASK-002.2] Implementar provider `echo` (mock)
- [ ] [TASK-002.3] Implementar `ChatResponse` dataclass
- [ ] [TASK-002.4] Remover @skip de cenários BDD
- [ ] [TASK-002.5] TDD: Red → Green → Refactor

**DoD**:
- [x] `pytest -m "ci_fast and sdk"` passa
- [x] Echo provider funcional
- [x] Logs registram status "success"
```

---

## 📊 Checklist de Qualidade do Roadmap Planning

Antes de entregar o Roadmap Planning para TDD, validar:

### ✅ Subetapa 1: Arquitetura e Stack
- [ ] `TECH_STACK.md` criado com todas as bibliotecas e versões
- [ ] `ADR.md` (índice) criado
- [ ] ADRs individuais criados para decisões principais:
  - [ ] ADR-001: Framework HTTP (FastAPI/Flask/etc)
  - [ ] ADR-002: Plugin architecture
  - [ ] ADR-003: Framework de testes (pytest-bdd)
  - [ ] ADR-004: Gerenciamento de dependências
  - [ ] ADR-005: Monorepo vs Multi-repo
  - [ ] Outros conforme necessário
- [ ] `HLD.md` criado com:
  - [ ] Diagrama C4 Context
  - [ ] Diagrama de componentes principais
  - [ ] Diagrama de sequência (fluxo principal)
  - [ ] Integrações externas documentadas
- [ ] `LLD.md` criado com:
  - [ ] Diagrama de classes (UML)
  - [ ] Interfaces documentadas (Provider, etc)
  - [ ] Padrões de design identificados (Strategy, etc)
  - [ ] Hierarquia de erros
  - [ ] Exemplos de código
- [ ] Estrutura de pastas definida (`src/forge/`, `src/symclient/`)
- [ ] Consenso técnico alcançado com tech lead

### ✅ Subetapa 2: Dependências
- [ ] Grafo de dependências criado (`dependency_graph.md`)
- [ ] Todas as features mapeadas
- [ ] Dependências técnicas identificadas
- [ ] Ordem de implementação clara

### ✅ Subetapa 3: Quebra
- [ ] Features > L quebradas em tarefas
- [ ] Rastreabilidade mantida (TASK-XXX → FEATURE-YYY)
- [ ] Tarefas granulares (< 2 dias cada)

### ✅ Subetapa 4: Estimativa
- [ ] Todas as features estimadas
- [ ] Riscos identificados e documentados
- [ ] Priorização clara (P0, P1, P2, P3)
- [ ] Sprints definidos com critérios de conclusão

### ✅ Subetapa 5: Documentação
- [ ] `ROADMAP.md` criado (visão executiva)
- [ ] `BACKLOG.md` criado (backlog operacional)
- [ ] `estimates.yml` criado (dados estruturados)
- [ ] `dependency_graph.md` criado (visualização)
- [ ] Stakeholder revisou e aprovou

---

## 🔄 Roadmap Planning é Vivo

**IMPORTANTE**: O roadmap NÃO é estático!

Durante TDD:
- ✅ **Atualizar** conforme features são concluídas
- ✅ **Ajustar** estimativas baseado em aprendizados
- ✅ **Re-priorizar** se necessário (mudanças de negócio)
- ✅ **Quebrar** novas tarefas conforme complexidade emerge

**Regra de ouro**: ROADMAP.md e BACKLOG.md refletem SEMPRE o estado atual do projeto.

---

## 🎯 Handoff para TDD

Ao concluir Roadmap Planning:

1. **Apresentar ROADMAP.md** para stakeholders (aprovação executiva)
2. **Apresentar BACKLOG.md** para time de desenvolvimento (clareza operacional)
3. **Confirmar** que primeira task (normalmente TASK-001.1 de config.feature) está clara
4. **Iniciar TDD** com ciclo Red-Green-Refactor

**Próxima fase**: TDD (Implementação guiada por testes)

**Referências**:
- Processo TDD: `process/execution/tdd/TDD_PROCESS.md` (a criar)
- Handoff BDD: `specs/bdd/HANDOFF.md`
- Features BDD: `specs/bdd/**/*.feature`

---

## 📚 Templates

Templates disponíveis em `process/execution/roadmap_planning/templates/`:
- `template_roadmap.md` — Estrutura de ROADMAP.md
- `template_backlog.md` — Estrutura de BACKLOG.md
- `template_estimates.yml` — Estrutura de estimates.yml
- `template_dependency_graph.md` — Exemplo de grafo Mermaid

---

**Autor**: Equipe Forge Process
**Versão**: 1.0
**Data**: 2025-11-05
