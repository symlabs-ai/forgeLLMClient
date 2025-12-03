# Roadmap — ForgeLLMClient

> **Versao:** 1.0
> **Data:** 2025-12-03
> **Status:** Em Planejamento

---

## Visao Geral

O ForgeLLMClient e um SDK Python que fornece interface unificada para multiplos provedores de LLM (OpenAI, Anthropic, etc.) seguindo Clean Architecture e padroes ForgeBase.

---

## Fases do Projeto

```mermaid
flowchart TB
    subgraph Phase1["FASE 1: FUNDACAO"]
        Sprint1["Sprint 1: Core SDK<br/>- Estrutura de pacotes (src layout)<br/>- Domain: Entidades, Value Objects, Exceptions<br/>- Application: Ports, UseCases base<br/>- config.feature implementado<br/>- chat.feature implementado (sync + streaming)"]
    end

    subgraph Phase2["FASE 2: PROVIDERS MOCK"]
        Sprint2["Sprint 2: MockProvider + Features Core<br/>- MockProvider completo (testes)<br/>- response.feature implementado<br/>- tokens.feature implementado<br/>- tools.feature implementado"]
    end

    subgraph Phase3["FASE 3: PROVIDERS REAIS"]
        Sprint3["Sprint 3: OpenAI Provider<br/>- OpenAI Responses API (NUNCA ChatCompletions)<br/>- openai.feature implementado<br/>- Testes de integracao (@ci_int)"]
        Sprint4["Sprint 4: Anthropic Provider<br/>- Anthropic Messages API<br/>- anthropic.feature implementado<br/>- Testes de integracao (@ci_int)"]
    end

    subgraph Phase4["FASE 4: RECURSOS AVANCADOS"]
        Sprint5["Sprint 5: AutoFallback + MCP<br/>- AutoFallbackProvider<br/>- MCP Client (implementacao propria)<br/>- Documentacao final"]
    end

    Phase1 --> Phase2 --> Phase3 --> Phase4

    style Phase1 fill:#e8f5e9
    style Phase2 fill:#fff3e0
    style Phase3 fill:#e3f2fd
    style Phase4 fill:#f3e5f5
```

---

## Timeline Visual

```mermaid
gantt
    title Roadmap ForgeLLMClient
    dateFormat  YYYY-MM-DD
    section Fase 1
    Sprint 1 - Core SDK           :s1, 2025-01-01, 14d
    section Fase 2
    Sprint 2 - MockProvider       :s2, after s1, 10d
    section Fase 3
    Sprint 3 - OpenAI             :s3, after s2, 10d
    Sprint 4 - Anthropic          :s4, after s3, 10d
    section Fase 4
    Sprint 5 - AutoFallback + MCP :s5, after s4, 14d
```

---

## Marcos (Milestones)

```mermaid
flowchart LR
    M1["M1: MVP Core<br/>- Estrutura de pacotes<br/>- Domain layer<br/>- MockProvider"]
    M2["M2: Features Completas<br/>- Todos BDD features<br/>- Cobertura >= 80%"]
    M3["M3: OpenAI Integrado<br/>- Responses API<br/>- Tool calling"]
    M4["M4: Anthropic Integrado<br/>- Paridade de features"]
    M5["M5: Release 1.0<br/>- AutoFallback<br/>- MCP Client"]

    M1 --> M2 --> M3 --> M4 --> M5

    style M1 fill:#c8e6c9
    style M2 fill:#fff9c4
    style M3 fill:#bbdefb
    style M4 fill:#f8bbd9
    style M5 fill:#d1c4e9
```

### M1: MVP Core
- Estrutura de pacotes criada
- Domain layer completo
- Application layer com ports definidos
- MockProvider funcional
- Testes BDD passando (config, chat)

### M2: Features Completas
- Todos os features BDD implementados
- MockProvider com cobertura total
- response, tokens, tools funcionais
- Cobertura >= 80%

### M3: OpenAI Integrado
- OpenAI Provider usando Responses API
- Testes de integracao passando
- Chat sync e streaming funcionais
- Tool calling funcional

### M4: Anthropic Integrado
- Anthropic Provider funcional
- Testes de integracao passando
- Paridade de features com OpenAI

### M5: Release 1.0
- AutoFallbackProvider
- MCP Client
- Documentacao completa
- Package publicavel

---

## Caminho Critico

```mermaid
flowchart LR
    config["config.feature"] --> chat["chat.feature"] --> tools["tools.feature"]
    tools --> openai["openai.feature"]
    tools --> anthropic["anthropic.feature"]

    style config fill:#ffcdd2
    style chat fill:#ffcdd2
    style tools fill:#ffcdd2
    style openai fill:#ffcdd2
    style anthropic fill:#ffcdd2
```

Todas as features no caminho critico devem ser implementadas sequencialmente.

---

## Prioridades

| Prioridade | Descricao | Features |
|------------|-----------|----------|
| **P0** (Critico) | Essencial para MVP | config, chat, tools |
| **P1** (Alto) | Necessario para uso real | openai, anthropic, response, tokens |
| **P2** (Medio) | Recursos avancados | autofallback, mcp |
| **P3** (Baixo) | Nice-to-have | metricas, observabilidade |

---

## Metodologia

### TDD Mandatorio

```mermaid
flowchart LR
    RED["RED<br/>Escrever teste<br/>que falha"] --> GREEN["GREEN<br/>Implementar<br/>minimo"] --> REFACTOR["REFACTOR<br/>Melhorar<br/>codigo"]
    REFACTOR --> RED

    style RED fill:#ffcdd2
    style GREEN fill:#c8e6c9
    style REFACTOR fill:#bbdefb
```

1. **Testes SEMPRE escritos antes do codigo**
2. Cenarios BDD guiam os testes
3. Cobertura minima: 80%
4. CI falha se cobertura cair

### BDD como Especificacao

- Features em `specs/bdd/*.feature`
- Steps em `tests/bdd/`
- Cenarios com `@skip` removidos conforme implementacao

---

## Estrutura de Entregas

### Por Sprint

1. Codigo fonte implementado
2. Testes passando (unit + BDD)
3. Documentacao atualizada
4. Cobertura mantida

### Por Milestone

1. Release notes
2. Changelog
3. Documentacao de API
4. Exemplos de uso

---

## Riscos e Mitigacoes

| Risco | Impacto | Mitigacao |
|-------|---------|-----------|
| OpenAI muda Responses API | Alto | Abstrair em adapter, testes de integracao |
| ForgeBase incompativel | Medio | Versao fixa, testes de regressao |
| Performance streaming | Medio | Benchmarks, async otimizado |

---

## Proximos Passos

1. [ ] Stakeholder aprova roadmap
2. [ ] Iniciar Sprint 1 (Fundacao)
3. [ ] Criar estrutura de pacotes
4. [ ] Implementar primeiro teste BDD

---

## Referencias

- `specs/roadmap/BACKLOG.md` - Backlog detalhado
- `specs/roadmap/dependency_graph.md` - Grafo de dependencias
- `specs/roadmap/TECH_STACK.md` - Stack tecnologico
- `specs/roadmap/HLD.md` - Design de alto nivel
- `specs/roadmap/LLD.md` - Design de baixo nivel

---

*Documento gerado pelo Roadmap Planning Process*
