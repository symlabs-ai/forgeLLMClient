# Review Guidelines - Code & Sprint Review

**Subprocesso do Delivery Process – validação técnica, de processo e de negócio.**

**Project (exemplo)**: forgeLLMClient
**Team**: Agent Coders (Claude Code primary)
**Last Updated**: 2025-11-06
**Methodology**: bill-review (technical) + Jorge the Forge (process) + stakeholder review

---

## 🎯 Overview

Este documento define critérios e processos para **três tipos de review**:

1. **Check-in Técnico e Demo** - Validação técnica e de alinhamento por sessão/feature
2. **Sprint Review (Technical)** - bill-review agent valida código, arquitetura, testes
3. **Sprint Review (Process)** - Jorge the Forge valida ForgeProcess compliance **← NOVO**

**Comparação dos Reviewers**:

| Aspecto | bill-review | Jorge the Forge |
|---------|-------------|-----------------|
| **Foco** | Código, arquitetura, qualidade técnica | Processo, metodologia, documentação |
| **Valida** | Clean Architecture, Forgebase, testes | ForgeProcess, TDD, BDD, Sprint workflow |
| **Output** | Technical review (CODE compliance) | Process review (PROCESS compliance) |
| **Quando** | End of sprint (Day 1) | End of sprint (Day 2) **← Após bill-review** |
| **Artefato** | `project/sprints/sprint-N/review.md` | `project/sprints/sprint-N/jorge-process-review.md` |

---

## 🔍 Check-in Técnico e Demo (Por Sessão/Feature)

Este processo ocorre ao final de cada sessão de implementação para garantir alinhamento e qualidade contínua.

### 1. Pré-Voo Técnico (Auto-validação) ⚠️ OBRIGATÓRIO

Antes de apresentar qualquer resultado, o desenvolvedor/agente **deve** completar a validação técnica local, conforme **ADR-010**. O objetivo é garantir que a feature está funcional e estável.

**Checklist de Pré-Voo (Resumo do ADR-010):**
- **Execução da Demo:** O script de demo (`examples/...`) roda sem erros com credenciais reais.
- **Testes BDD:** Os testes BDD para a feature passam (`pytest tests/bdd/...`).
- **Qualidade do Código:** Sem erros de sintaxe ou import.
- **Documentação:** A feature está documentada nos cenários BDD.

**🔴 BLOQUEIO INTERNO**: Se qualquer item falhar, o código não deve ser apresentado. Corrija primeiro.

### 2. Demo para Feedback (com Stakeholder)

Com o pré-voo aprovado, a demo é apresentada ao stakeholder, conforme descrito no **SPRINT_PROCESS.md**.

- **Foco:** Coletar feedback rápido, não obter aprovação final.
- **Formato:** Síncrono (ao vivo) ou assíncrono (vídeo).
- **Resultado:** Feedback é documentado. O commit da feature pode prosseguir, usando a tag `[needs-final-review]` para sinalizar que a aprovação final de negócio está pendente para a Sprint Review.

Esta abordagem separa a validação técnica (obrigatória na sessão) da aprovação de negócio (formalizada na Sprint Review).

## 📋 Sprint Review (End of Sprint)

### Objetivos

- Validar **todas** as features da sprint
- Verificar compliance com padrões (técnicos e processo)
- Decidir se sprint está **DONE**
- Apresentar resultados ao stakeholder

### Processo

#### 1. Preparação (1 dia antes)

- [ ] Consolidar todos os commits da sprint
- [ ] Executar suite completa de testes
- [ ] Gerar relatório de cobertura
- [ ] Revisar todos os bill-review reports

#### 2. bill-review Sprint Validation (Day 1 - Technical)

Invocar **bill-review** para **validação técnica da sprint completa**.

```
Prompt: "Realize uma Sprint Review completa da Sprint N para validar conformidade com:
1. Forgeprocess Standards
2. Clean Architecture Principles
3. Orthogonal Architecture
4. Forgebase Framework Usage

Arquivos para revisar:
- src/forgellmclient/** (implementação)
- tests/** (testes)
- specs/bdd/** (features)
- project/sprints/sprint-N/** (documentação)

Forneça:
1. Análise de conformidade
2. Pontos fortes
3. Problemas identificados
4. Recomendações
5. Aprovação: SIM/NÃO/CONDICIONAL"
```

**Output**: `project/sprints/sprint-N/review.md`

##### **Execução Manual / Fallback**
Se o symbiota `bill-review` não estiver disponível, a revisão técnica deve ser feita manualmente, seguindo o `Code Review Checklist` e o `Technical Compliance` checklist no final deste documento. As perguntas chave são:
- **Conformidade com Arquitetura:** O código adere aos princípios de Clean/Orthogonal Architecture?
- **Padrões do Framework:** Os padrões específicos do Forgebase foram usados corretamente?
- **Qualidade dos Testes:** A cobertura de testes da sprint é ≥ 80%?
- **Qualidade do Código:** O código está livre de erros de lint e tipo?

#### 3. Jorge the Forge Process Review (Day 2 - Process) **← NOVO OBRIGATÓRIO**

Invocar **Jorge the Forge** para **validação de processo da sprint completa**.

**Agent**: `Jorge the Forge` (symbiota definido em `process/symbiotes/jorge_forge/prompt.md`)
**Referência Completa**: Ver `process/delivery/review/etapa_jorge_process_review.md`

**Jorge valida**:
- ForgeProcess compliance (TDD, BDD, Sprint workflow)
- Process gaps identification
- Process improvements proposals
- Artifact quality (planning, progress, review, retrospective)
- ADR documentation quality

**Output**: `project/sprints/sprint-N/jorge-process-review.md`

##### **Execução Manual / Fallback**
Se o agente `Jorge the Forge` não estiver disponível, a auditoria de processo deve ser feita manualmente, seguindo o `Process Compliance` checklist no final deste documento. As perguntas chave são:
- **Aderência ao Processo:** O ciclo TDD e o fluxo de sprint baseado em sessão foram respeitados?
- **Qualidade dos Artefatos:** Os documentos da sprint (`planning.md`, etc.) estão completos?
- **Rastreabilidade:** Os commits e PRs fazem referência aos IDs dos Tracks do BDD?
- **Melhoria Contínua:** Decisões importantes foram documentadas em ADRs?

**Ordem Importa**:
1. **bill-review primeiro** (valida o que foi construído)
2. **Jorge segundo** (valida como foi construído)
3. **Retrospective terceiro** (incorpora ambos os reviews)

#### 4. Criar Sprint Review Document

Template de `project/sprints/sprint-N/review.md`:

```markdown
# Sprint N Review

**Data**: YYYY-MM-DD
**Reviewer**: bill-review agent + [Nome Stakeholder]
**Status**: ✅ APROVADO / 🔄 CONDICIONAL / ❌ REJEITADO

## Features Completadas

| Feature | Story Points | Coverage | Status |
|---------|--------------|----------|--------|
| F01 (config) | 3 | 94% | ✅ |
| F02 (llm) | 5 | 87% | ✅ |
| ... | ... | ... | ... |

## Métricas Gerais

| Métrica | Target | Atual | Status |
|---------|--------|-------|--------|
| Test Coverage | ≥80% | 91% | ✅ |
| Lint Errors | 0 | 0 | ✅ |
| Type Errors | 0 | 0 | ✅ |
| BDD Scenarios | 100% | 100% | ✅ |

## Conformidade

### Forgeprocess ✅
- TDD Red-Green-Refactor seguido em todas as features
- VCR.py usado para testes de integração
- Commits bem estruturados

### Clean Architecture ✅
- Separação clara: Entities, Use Cases, Adapters
- Dependency inversion aplicada

### Forgebase Compliance ✅
- BaseModelData usado para entities
- Protocols para interfaces

## Problemas Identificados

### Críticos (Blocker)
- Nenhum

### Importantes (Resolver próxima sprint)
- [ ] Adicionar edge case tests para YAML inválido

### Nice to Have
- [ ] Melhorar documentação de API

## Aprovação

**Decisão**: ✅ APROVADO

**Condições**:
1. Criar issues para problemas importantes
2. Adicionar edge cases na Sprint N+1

**Aprovado por**: [Nome Stakeholder]
**Data**: YYYY-MM-DD
```

#### 4. Demo para Stakeholder

Apresentar:

1. **Features completadas** (demos interativas)
2. **Métricas de qualidade** (coverage, lint, etc.)
3. **Conformidade** (bill-review report)
4. **Próximos passos** (backlog atualizado)

#### 5. Obter Aprovação Final

Stakeholder decide:

- ✅ **APROVADO**: Sprint completa, pode iniciar próxima
- 🔄 **CONDICIONAL**: Ajustes menores requeridos
- ❌ **REJEITADO**: Problemas críticos, não pode prosseguir

---

## ✅ Code Review Checklist

### Funcionalidade

- [ ] Feature implementa todos os cenários BDD?
- [ ] Comportamento está correto (testes manuais)?
- [ ] Edge cases cobertos?
- [ ] Error handling adequado?

### Testes

- [ ] Todos os testes passando?
- [ ] Coverage ≥ 80%?
- [ ] Testes seguem padrão Given-When-Then?
- [ ] VCR.py usado para API calls?
- [ ] Testes são rápidos (< 10s)?

### Código

- [ ] Lint sem erros (ruff)?
- [ ] Type check sem erros (mypy)?
- [ ] Nomes claros e descritivos?
- [ ] Sem código comentado?
- [ ] Sem TODOs (ou criados como issues)?

### Arquitetura

- [ ] Forgebase patterns aplicados?
- [ ] Separação de responsabilidades clara?
- [ ] Dependency injection usado?
- [ ] Sem acoplamento desnecessário?

### Documentação

- [ ] Docstrings em classes/funções públicas?
- [ ] README atualizado (se necessário)?
- [ ] Examples atualizados (se necessário)?
- [ ] CHANGELOG.md atualizado?

---

## 🏆 Sprint Review Checklist

### Planejamento

- [ ] Todas as features planejadas completadas?
- [ ] Story points bateram com estimativa?
- [ ] Velocity calculado para próxima sprint?

### Qualidade

- [ ] Coverage geral ≥ 80%?
- [ ] Lint e type check sem erros?
- [ ] Todos os BDD scenarios passando?
- [ ] Sem regressões (features antigas ainda funcionam)?

### Technical Compliance (bill-review)

- [ ] bill-review executado para a sprint completa?
- [ ] Forgebase patterns aplicados consistentemente?
- [ ] Clean Architecture mantida?
- [ ] Orthogonal Architecture score ≥8/10?
- [ ] Documentação técnica completa?

### Process Compliance (Jorge the Forge) **← NOVO OBRIGATÓRIO**

- [ ] Jorge the Forge process review executado?
- [ ] TDD cycle seguido em ≥80% das features?
- [ ] BDD scenarios completos (100% das features)?
- [ ] Sprint artifacts completos (planning, progress, review, retrospective)?
- [ ] ADRs criados para decisões importantes?
- [ ] Pre-stakeholder validation checklist seguido (ADR-010)?
- [ ] Process improvements propostos documentados?

### Processo

- [ ] Sessions documentadas em progress.md?
- [ ] Decisões técnicas documentadas?
- [ ] Retrospective incorpora findings de bill + Jorge?

### Entrega

- [ ] Features deployáveis?
- [ ] Breaking changes documentadas?
- [ ] Migration guides criados (se necessário)?
- [ ] Stakeholder aprovou?
- [ ] Process improvements implementados (se aprovados)?

---

## 🚫 Common Review Failures

### 1. Cobertura Insuficiente

**Problema**: Coverage < 80%

**Ação**:
- Identificar código não coberto
- Adicionar testes unit ou integration
- Re-executar review

### 2. Forgebase Non-Compliance

**Problema**: Entity não usa BaseModelData

**Ação**:
- Refatorar para usar BaseModelData
- Atualizar testes
- Re-executar bill-review

### 3. Testes Frágeis

**Problema**: Testes falham aleatoriamente

**Ação**:
- Identificar race conditions
- Adicionar fixtures apropriados
- Garantir isolamento de testes

### 4. Documentação Faltando

**Problema**: Docstrings ausentes

**Ação**:
- Adicionar docstrings em classes/funções públicas
- Atualizar README se API mudou
- Re-executar review

---

## 📊 Review Metrics

Track em `project/sprints/sprint-N/review.md`:

| Métrica | Sprint 1 | Sprint 2 | Sprint 3 | Target |
|---------|----------|----------|----------|--------|
| **Features Completadas** | 4 | ? | ? | 100% |
| **Coverage** | 94% | ? | ? | ≥80% |
| **Lint Errors** | 0 | ? | ? | 0 |
| **Type Errors** | 0 | ? | ? | 0 |
| **bill-review Issues** | 2 (minor) | ? | ? | 0 critical |
| **Rework Rate** | 5% | ? | ? | <10% |

---

## 🔗 Related Documents

- **TDD Process**: `process/execution/tdd/TDD_PROCESS.md`
- **Sprint Process**: `process/delivery/sprint/SPRINT_PROCESS.md`
- **Jorge the Forge**: `process/delivery/review/etapa_jorge_process_review.md` **← NOVO**
- **Pre-Stakeholder Validation**: `process/delivery/review/etapa_stakeholder_validation.md` (ADR-010)
- **Backlog**: `specs/roadmap/BACKLOG.md`
- **Example Reviews**:
  - Technical: `project/sprints/sprint-1/review.md`
  - Process: `project/sprints/sprint-1/jorge-process-review.md` (será criado)

---

**Last Updated**: 2025-11-06
**Status**: Sprint 1 complete - bill-review done, Jorge review pending
**Next Review**: Sprint 2 (bill-review + Jorge the Forge)
