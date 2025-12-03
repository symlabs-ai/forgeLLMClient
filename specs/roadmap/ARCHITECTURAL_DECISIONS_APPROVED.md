# Decisoes Arquiteturais Aprovadas — ForgeLLMClient

> **Data de Aprovacao:** 2025-12-03
> **Aprovador:** Stakeholder
> **Status:** Aprovado

---

## Resumo das Decisoes

| ID | Decisao | Escolha Aprovada |
|----|---------|------------------|
| 1 | Linguagem | Python 3.12+ |
| 2 | Arquitetura Provedores | Abstract Base Class (Orthogonal Architecture ForgeBase) |
| 3 | Provedores MVP | OpenAI + Anthropic + MockProvider |
| 4 | Estrutura Projeto | Monorepo com src layout |
| 5 | Nome Pacote | `forge-llm` |
| 6 | Gerenciamento Deps | pyproject.toml + pip |
| 7 | HTTP Client | httpx (async) |
| 8 | API OpenAI | Responses API (NUNCA ChatCompletions) |
| 9 | Validacao Dados | Seguir padrao ForgeBase |
| 10 | MCP Client | Implementacao propria |
| 11 | Metodologia | TDD (Testes ANTES do codigo) |

---

## Decisao 1: Linguagem e Runtime

**Escolha:** Python 3.12+

**Justificativa:**
- Requisito explicito do produto
- Compatibilidade com ForgeBase
- Type hints avancados
- Ecossistema maduro para LLM

---

## Decisao 2: Arquitetura de Provedores

**Escolha:** Abstract Base Class respeitando Orthogonal Architecture do ForgeBase

**Justificativa:**
- Alinhamento com Clean + Hexagonal Architecture do ForgeBase
- Permite HotSwap de provedores em runtime
- Facilita implementacao de AutoFallback
- Testabilidade via MockProvider

**Provedores no MVP:**
1. OpenAI (usando nova Responses API)
2. Anthropic
3. MockProvider (para testes)

---

## Decisao 3: Estrutura de Projeto

**Escolha:** Monorepo com src layout

```
forgeLLMClient/
├── src/
│   └── forge_llm/           # Pacote principal
│       ├── __init__.py
│       ├── domain/          # Entidades, VOs, Exceptions
│       ├── application/     # UseCases, Ports, DTOs
│       ├── infrastructure/  # Repositories, Config
│       ├── adapters/        # CLI, HTTP (futuro)
│       └── providers/       # OpenAI, Anthropic, Mock
├── tests/
│   ├── unit/
│   ├── integration/
│   └── bdd/
├── specs/
│   ├── bdd/
│   └── roadmap/
└── pyproject.toml
```

**Nome do pacote PyPI:** `forge-llm`

---

## Decisao 4: Gerenciamento de Dependencias

**Escolha:** pyproject.toml + pip

**Justificativa:**
- Padrao PEP 621
- Compativel com ForgeBase
- Simples e direto

---

## Decisao 5: HTTP Client

**Escolha:** httpx (async)

**Justificativa:**
- Async nativo (requisito para streaming)
- API moderna
- Suporte HTTP/2
- Timeout e retry configuraveis

---

## Decisao 6: API OpenAI

**Escolha:** Responses API (MANDATORIO: NUNCA usar ChatCompletions)

**Justificativa:**
- API mais recente e recomendada
- Melhor suporte a streaming
- Funcionalidades avancadas

**Restricao:** O uso de ChatCompletions e PROIBIDO neste projeto.

---

## Decisao 7: Validacao de Dados

**Escolha:** Seguir padrao ForgeBase

**Componentes a usar:**
- `EntityBase` para entidades
- `ValueObjectBase` para objetos de valor
- `ValidationError`, `BusinessRuleViolation` para excecoes
- `DTOBase` para DTOs

---

## Decisao 8: MCP Client

**Escolha:** Implementacao propria

**Justificativa:**
- ValueTrack fundamental
- Controle total sobre implementacao
- Sem dependencia externa

---

## Decisao 9: Metodologia de Desenvolvimento

**Escolha:** TDD (Test-Driven Development)

**Regra:** Testes SEMPRE escritos ANTES do codigo fonte.

**Fluxo:**
1. Escrever teste (Red)
2. Implementar minimo para passar (Green)
3. Refatorar (Refactor)

---

## Alinhamento com ForgeBase

O ForgeLLMClient seguira rigorosamente:

### Arquitetura de Camadas
```
Domain ← Application ← Infrastructure
                    ← Adapters
```

### Regras de Dependencia
| Camada | Pode importar | NAO pode importar |
|--------|---------------|-------------------|
| Domain | Nada externo | Application, Infrastructure, Adapters |
| Application | Domain, Ports | Infrastructure, Adapters |
| Infrastructure | Domain, Application | Adapters |
| Adapters | Domain, Application | Infrastructure (via Ports) |

### Classes Base ForgeBase
| Componente | Camada | Base Class |
|------------|--------|------------|
| Entidade | Domain | `EntityBase` |
| Value Object | Domain | `ValueObjectBase` |
| UseCase | Application | `UseCaseBase` |
| Port | Application | `PortBase` / ABC |
| Adapter | Adapters | `AdapterBase` |

### Excecoes de Dominio
```python
from forgebase.domain.exceptions import (
    DomainException,
    ValidationError,
    InvariantViolation,
    BusinessRuleViolation,
    EntityNotFoundError,
)
```

### Observabilidade
- LogService para logging estruturado
- TrackMetrics para metricas
- Decorators para instrumentacao automatica

---

## Proximos Passos

1. Criar ADRs individuais para cada decisao
2. Criar HLD (High Level Design)
3. Criar LLD (Low Level Design)
4. Criar TECH_STACK.md
5. Criar dependency_graph.md
6. Criar ROADMAP.md e BACKLOG.md

---

*Documento gerado pelo Roadmap Planning Process*
*Aprovado em: 2025-12-03*
