# Sprint Workflow - Session-Based Development

**Subprocesso do Delivery Process – como organizar o trabalho em sprints e sessões.**

**Project (exemplo)**: forgeLLMClient
**Team**: Agent Coders (Claude Code primary)
**Last Updated**: 2025-11-07
**Methodology**: Session-based sprints (não daily standups)

**⚠️ MANDATORY**: See `process/delivery/sprint/ceremonies/CEREMONY_SCHEDULE.md` for REQUIRED sprint ceremonies

---

## 🎯 Overview

Este processo documenta como conduzir sprints com **agent coders** usando modelo **session-based**, diferente de times humanos com daily standups.

### Diferenças Chave: Agent Coders vs. Human Teams

| Aspecto | Human Teams | Agent Coders |
|---------|-------------|--------------|
| **Trabalho** | Diário (8h/dia) | On-demand (sessões quando stakeholder disponível) |
| **Sincronização** | Daily standups (assíncronos) | Review na mesma sessão (síncrono) |
| **Commits** | Múltiplos/dia | 1 commit = 1 feature (após aprovação) |
| **Planning** | Sprint planning meeting | Início de cada sessão |
| **Review** | End of sprint | End of session + End of sprint |

---

## 📋 Sprint Structure

### Sprint Overview

```
Sprint (2 semanas típico)
    ↓
┌─────────────────────────────────────┐
│  Sessão 1 (2-3h)                    │
│  ├─ Mini-planning                   │
│  ├─ Implementar 1-2 features        │
│  └─ Session review + commit         │
├─────────────────────────────────────┤
│  Sessão 2 (2-3h)                    │
│  ├─ Mini-planning                   │
│  ├─ Implementar 1-2 features        │
│  └─ Session review + commit         │
├─────────────────────────────────────┤
│  ... (3-4 sessões/semana)           │
└─────────────────────────────────────┘
    ↓
Sprint Review (Day 1): bill-review agent (technical)
    ↓
Sprint Review (Day 2): Jorge the Forge (process) ← NOVO
    ↓
Sprint Retrospective (Day 3)
```

---

## 🚀 Sprint Planning (Início da Sprint)

### Objetivos
- Definir features da sprint (do backlog)
- Estimar story points
- Definir frequência de sessões
- Identificar riscos

### Processo

1. **Review do Backlog**
   - Ler `specs/roadmap/BACKLOG.md`
   - Identificar próximas features (ordem de prioridade)

2. **Capacity Planning**
   - Estimar sessões disponíveis (ex: 3-4 sessões/semana x 2 semanas = 6-8 sessões)
   - Estimar story points/sessão (baseado em sprints anteriores)
   - Total capacity = sessões × pts/sessão

3. **Feature Selection**
   - Selecionar features que cabem na capacity
   - Validar dependências (dependency graph)
   - Confirmar com stakeholder

4. **Documentar Planning**
   - Criar `project/sprints/sprint-N/planning.md`
   - Use template: `process/delivery/sprint/templates/planning.md` ✅
   - Listar features selecionadas
   - Definir critérios de aceitação
   - Document capacity, dependencies, risks, DoD

**Template**: `process/delivery/sprint/templates/planning.md` ✅ (Available since Sprint 1 retrospective)
**Example**: `project/sprints/sprint-1/planning.md` (retroactive documentation)

---

## 💻 Session Workflow (Durante Sprint)

### Estrutura de uma Sessão (2-3h típico)

```
1. Session Start (5min)
   ├─ Review última sessão
   ├─ Escolher próxima feature
   └─ Confirmar critérios de aceitação

2. Implementation (90-120min)
   ├─ 🔴 RED: Escrever testes
   ├─ 🟢 GREEN: Implementar
   ├─ 🔵 REFACTOR: Melhorar
   └─ 📼 VCR: Gravar API (se aplicável)

3. Session Demo & Technical Check-in (15-30min)
   ├─ ✅ **Executar Pré-Voo Técnico Local:** Antes de qualquer demo, rodar o checklist de validação local (lint, types, testes unitários e o script de demo). Ver `process/delivery/review/etapa_stakeholder_validation.md`.
   ├─ 💬 **Apresentar Demo ao Stakeholder (Síncrona ou Assíncrona):**
   │  ├─ **Recomendado (Síncrono):** Apresentar a demo ao vivo para feedback imediato.
   │  └─ **Alternativa (Assíncrona):** Se o stakeholder não estiver disponível, gravar um vídeo curto da demo, enviar o link, e prosseguir.
   ├─ 📝 **Documentar Feedback:** Registrar o feedback (ou a pendência dele) em `progress.md`.
   └─ **Nota:** O objetivo desta etapa é validar o direcionamento técnico e obter feedback rápido. A aprovação formal do negócio ocorre na Sprint Review.

4. Commit (5min)
   ├─ 💾 Criar commit com a feature implementada.
   └─ 꼬 Usar `[needs-final-review]` no corpo da mensagem de commit se o feedback do stakeholder estiver pendente ou se houver ajustes a serem validados na Sprint Review.

5. Session Close (5min)
   ├─ Atualizar progress.md
   └─ Planejar próxima sessão
```

### Frequência Recomendada

| Sprint Complexity | Sessões/Semana | Total Sessões (2 weeks) |
|-------------------|----------------|-------------------------|
| **Baixa** (≤22 pts) | 2-3 | 4-6 |
| **Média** (23-28 pts) | 3 | 6 |
| **Alta** (>28 pts) | 3-4 | 6-8 |

**Nota**: Sprint 3 do forgeLLMClient tem 36 pts → requer 3-4 sessões/semana

---

## 📊 Progress Tracking

### Durante Sprint

Atualizar `project/sprints/sprint-N/progress.md` após cada sessão:

```markdown
# Sprint N - Progress

## Sessão 1 (2025-11-05)
- ✅ F01 (config.feature) - 3 pts - DONE
- Tempo: 2.5h
- Commits: `2cd0ee2`

## Sessão 2 (2025-11-06)
- 🔄 F02 (llm.feature) - 5 pts - IN PROGRESS
- Tempo: 2h (incompleto, continuar próxima sessão)

## Sessão 3 (2025-11-07)
- ✅ F02 (llm.feature) - 5 pts - DONE
- Tempo: 1h (finalização)
- Commits: `abc1234`
```

### Métricas

Track em `progress.md`:
- Story points completados
- Horas por feature
- Velocity (pts/sessão)
- Blockers encontrados

---

## 🔍 Sprint Review (Final da Sprint)

### Objetivos
- Validar todas as features implementadas
- Executar bill-review agent (compliance técnica)
- **Executar Jorge the Forge (compliance de processo)** **← NOVO OBRIGATÓRIO**
- Apresentar resultados ao stakeholder
- Decidir se sprint está DONE

### Processo

#### Day 1: Technical Review (bill-review)

1. **Executar bill-review (symbiota técnico)**
   ```
   Invocar bill-review para validação técnica da sprint completa
   ```

2. **Consolidar Technical Review**
   - Criar `project/sprints/sprint-N/review.md`
   - Incluir:
     - Features completadas
     - Métricas (coverage, lint, types)
     - Compliance (Forgebase, Clean Arch, Orthogonal Arch)
     - Decisão: APROVADO / CONDICIONAL / REJEITADO

##### **Execução Manual / Fallback**
Se o symbiota `bill-review` não estiver disponível, a revisão técnica deve ser feita manualmente, seguindo este checklist:
- **Conformidade com Arquitetura:** O código adere aos princípios de Clean Architecture e Orthogonal Architecture? As responsabilidades (Entities, UseCases, Adapters) estão bem separadas?
- **Padrões do Framework:** Os padrões específicos do Forgebase (BaseModelData, Protocols) foram usados corretamente?
- **Qualidade dos Testes:** A cobertura de testes da sprint é ≥ 80%? Os testes são robustos e cobrem os cenários BDD?
- **Qualidade do Código:** O código está livre de erros de lint e tipo? A complexidade é gerenciada?
- **Documentação:** Docstrings e READMEs foram atualizados?

**Template**: Ver exemplo em `project/sprints/sprint-1/review.md`

#### Day 2: Process Review (Jorge the Forge) **← NOVO OBRIGATÓRIO**

3. **Executar Jorge the Forge Process Review** (MANDATORY)
   ```
   # Invocar Jorge the Forge (symbiota de processo)
   # Via Task tool com prompt específico para Sprint Review
   ```

   **Agent**: `Jorge the Forge` (symbiota de processo)
   **Location (projeto alvo)**: `process/symbiotes/jorge_forge/prompt.md`

4. **Consolidar Process Review**
   - Criar `project/sprints/sprint-N/jorge-process-review.md`
   - Incluir:
     - ForgeProcess compliance (TDD, BDD, Sprint workflow)
     - Process gaps identified
     - Process improvements proposed
     - Artifact quality assessment
     - Decisão: APPROVED / CONDITIONAL / NEEDS IMPROVEMENT

##### **Execução Manual / Fallback**
Se o agente `Jorge the Forge` não estiver disponível, a auditoria de processo deve ser feita manualmente, respondendo às seguintes perguntas:
- **Aderência ao Processo:** O ciclo TDD (Red-Green-Refactor) foi seguido? Os cenários BDD foram usados como guia? O fluxo de sprint baseado em sessão foi respeitado?
- **Qualidade dos Artefatos:** Os documentos da sprint (`planning.md`, `progress.md`, etc.) estão completos e bem preenchidos?
- **Rastreabilidade:** Os commits e PRs fazem referência aos IDs dos Tracks do BDD?
- **Melhoria Contínua:** Decisões importantes foram documentadas em ADRs? A retrospectiva gerou ações claras?

**Referência**: Ver `process/delivery/review/etapa_jorge_process_review.md`

**O que Jorge valida (vs. bill-review)**:

| Aspecto | bill-review | Jorge the Forge |
|---------|-------------|-----------------|
| **Foco** | Código, arquitetura, qualidade técnica | Processo, metodologia, documentação |
| **Valida** | Clean Architecture, Forgebase, testes | ForgeProcess, BDD, TDD, Sprint workflow |
| **Output** | Technical review (CODE compliance) | Process review (PROCESS compliance) |

#### Day 3: Stakeholder Presentation & Retrospective

5. **Demo para Stakeholder**
   - Apresentar bill-review findings (technical)
   - Apresentar Jorge findings (process)
   - Executar demos interativas (ex: `examples/demo_*.py`)
   - Validar BDD scenarios
   - Obter aprovação final

6. **Documentar Resultados**
   - Atualizar `specs/roadmap/BACKLOG.md` (marcar features como DONE)
   - Atualizar `specs/roadmap/ROADMAP.md` (progresso)

7. **Implement Process Improvements** (Approved by Stakeholder)
   - Review Jorge's proposed improvements
   - Stakeholder approves which to implement
   - Update `/process/**/*.md` files before next sprint
   - Create templates/tools as needed

---

## 🔄 Sprint Retrospective (Final da Sprint)

### Objetivos
- Identificar o que funcionou bem
- Identificar o que pode melhorar
- Ajustar processo para próxima sprint

### Perguntas Chave

1. **What went well?**
   - Features completadas conforme estimativa?
   - TDD cycle foi seguido corretamente?
   - Comunicação stakeholder-agent foi eficiente?

2. **What didn't go well?**
   - Blockers encontrados?
   - Estimativas erradas?
   - Dívida técnica criada?

3. **Action items**
   - Ajustes no processo?
   - Ferramentas adicionais?
   - Treinamento necessário?

### Documentar

Criar `project/sprints/sprint-N/retrospective.md`:

```markdown
# Sprint N - Retrospective

## What Went Well ✅
- TDD cycle funcionou perfeitamente
- Bill-review agent economizou tempo

## What Didn't Go Well ❌
- Estimativa de F03 foi baixa (3 pts → levou 5 pts)
- Faltou documentação de API

## Action Items 🎯
- [ ] Adicionar buffer de 20% nas estimativas
- [ ] Criar template de documentação de API
```

---

## 📝 Sprint Artifacts

### Obrigatórios

| Artefato | Quando Criar | Localização |
|----------|--------------|-------------|
| **planning.md** | Início da sprint | `project/sprints/sprint-N/` |
| **progress.md** | Após cada sessão | `project/sprints/sprint-N/` |
| **review.md** | Final da sprint | `project/sprints/sprint-N/` |
| **retrospective.md** | Final da sprint | `project/sprints/sprint-N/` |

### Opcionais

| Artefato | Quando Criar | Localização |
|----------|--------------|-------------|
| **review-FXX.md** | Após feature complexa | `project/sprints/sprint-N/` |
| **decisions.md** | Quando decisão técnica importante | `project/sprints/sprint-N/` |

---

## 🎯 Sprint Success Criteria

Uma sprint é considerada **DONE** quando:

- [ ] Todas as features planejadas implementadas
- [ ] Todos os testes passando (100%)
- [ ] Coverage ≥ 80%
- [ ] Lint e type check sem erros
- [ ] **Bill-review aprovado** (validação técnica)
- [ ] **Jorge the Forge aprovado** (validação de processo) **← NOVO OBRIGATÓRIO**
- [ ] Documentação atualizada
- [ ] Demo validado pelo stakeholder
- [ ] Review e retrospective documentados
- [ ] Process improvements implementados (se aprovados pelo stakeholder)

---

## 🚨 Handling Risks

### Sprint em Risco (Mid-Sprint Check)

Se na metade da sprint:
- Velocity abaixo do esperado
- Blockers não resolvidos
- Story points restantes > capacity restante

**Ações**:
1. **Comunicar stakeholder** imediatamente
2. **Re-priorizar** features (mover menos críticas para próxima sprint)
3. **Aumentar frequência** de sessões (se possível)
4. **Simplificar** escopo de features restantes

### Sprint Failure

Se sprint não atinge critérios de sucesso:
- **NÃO** marcar sprint como completo
- **Estender** sprint por 1 semana (excepcional)
- **Mover** features incompletas para próxima sprint
- **Documentar** lições aprendidas na retrospective

---

## 🔗 Related Documents

- **TDD Process**: `process/execution/tdd/TDD_PROCESS.md`
- **Review Guidelines**: `process/delivery/review/REVIEW_PROCESS.md`
- **Backlog**: `specs/roadmap/BACKLOG.md`
- **Roadmap**: `specs/roadmap/ROADMAP.md`

---

**Last Updated**: 2025-11-05
**Status**: Sprint 1 em andamento
**Next Sprint Planning**: Após conclusão Sprint 1
