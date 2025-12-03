# Sprint Ceremony Schedule - ForgeProcess Practice
**Version**: 1.0
**Date**: 2025-11-07
**Author**: Jorge the Forge (symbiota de processo)
**Authority**: SPRINT_PROCESS.md lines 318-332
**Classification**: 🔴 **MANDATORY PRACTICE**
**Purpose**: Define REQUIRED sprint ceremonies and prevent process violations

---

## PURPOSE

This document defines the **MANDATORY** ceremonies for all ForgeProcess sprints. It exists because:

1. **Sprint 6 was REJECTED** (0.0/10 closure) - Assistant suggested Sprint Review was "optional"
2. **Sprint 5 had low compliance** (6.2/10) - Retroactive planning, ad-hoc execution
3. **Trust was broken** - User stated: "you tried to deceive me or you're not capable"

**This practice makes it IMPOSSIBLE for assistants to misunderstand what's mandatory.**

---

## CEREMONY CLASSIFICATION (MANDATORY vs OPTIONAL)

### Source of Truth: SPRINT_PROCESS.md Lines 318-332

```markdown
## 🎯 Sprint Success Criteria (SPRINT_PROCESS.md lines 318-332)

Uma sprint é considerada **DONE** quando:

- [ ] Todas as features planejadas implementadas
- [ ] Todos os testes passando (100%)
- [ ] Coverage ≥ 80%
- [ ] Lint e type check sem erros
- [ ] **Bill-review aprovado** (validação técnica)         ← OBRIGATÓRIO ✅
- [ ] **Jorge the Forge aprovado** (validação de processo) ← NOVO OBRIGATÓRIO ✅
- [ ] Documentação atualizada
- [ ] Demo validado pelo stakeholder
- [ ] Review e retrospective documentados                   ← OBRIGATÓRIO ✅
- [ ] Process improvements implementados (se aprovados pelo stakeholder)
```

### Interpretation Table

| Item | Classification | Can Skip? | Consequences of Skipping |
|------|----------------|-----------|--------------------------|
| **Bill-review aprovado** | 🔴 OBRIGATÓRIO | ❌ NO | Sprint REJECTION, 0.0/10 closure score |
| **Jorge the Forge aprovado** | 🔴 OBRIGATÓRIO | ❌ NO | Sprint REJECTION, 0.0/10 closure score |
| **Review e retrospective documentados** | 🔴 OBRIGATÓRIO | ❌ NO | Sprint REJECTION, 0.0/10 closure score |

**Critical Rule**: If SPRINT_PROCESS.md lines 318-332 list it as a success criterion → it is **MANDATORY**, not optional.

---

## MANDATORY CEREMONIES (ALL SPRINTS)

### 1. Sprint Planning (OBRIGATÓRIO)

**Authority**: SPRINT_PROCESS.md lines 56-89
**When**: BEFORE sprint start (Day 0)
**Duration**: 3-4 hours
**Who**: Assistant + Stakeholder

**What Happens**:
1. Select features from backlog
2. Estimate story points
3. Define acceptance criteria
4. Identify risks
5. Plan sessions
6. Create `project/sprints/sprint-N/planning.md`

**Deliverable**: `planning.md` created **BEFORE** Session 1

**Failure to Complete**: Sprint cannot start (no planning = ad-hoc execution)

---

### 2. Session Checkpoints (OBRIGATÓRIO)

**Authority**: SPRINT_PROCESS.md lines 92-136
**When**: AFTER EACH session
**Duration**: 15-30 minutes per session
**Who**: Assistant

**What Happens**:
1. Update `project/sprints/sprint-N/progress.md` with:
   - Session number, date
   - Features worked on (status)
   - Story points completed
   - Time spent
   - Commits made
   - Blockers (if any)
   - Next session plan

**Frequency**: After EVERY session (not at end of sprint)

**Template**:
```markdown
## Session N (YYYY-MM-DD)

### Features Worked On
- [ ] F_XXX (X pts) - [STATUS]

### Tasks Completed
- ✅ Task 1
- ✅ Task 2

### Story Points Progress
- Completed this session: X pts
- Total completed: Y/Z pts (%)

### Commits
- `hash` - description

### Blockers
- [None / List blockers]

### Next Session Plan
- [Plan for next session]
```

**Failure to Complete**: Process violation (-2.0 pts in Jorge review)

---

### 3. Session Review (OBRIGATÓRIO)

**Authority**: SPRINT_PROCESS.md lines 108-118
**When**: END of each session
**Duration**: 15-30 minutes per session
**Who**: Assistant + Stakeholder

**What Happens**:
1. Demo feature implemented
2. Stakeholder validates acceptance criteria
3. Stakeholder makes approval decision:
   - ✅ APPROVED → Create commit
   - ❌ REJECTED → Document feedback, iterate
   - 🔄 NEEDS CHANGES → Adjust and re-present

**Critical Rule**: Commit ONLY AFTER stakeholder approval

**Failure to Complete**: Commit without approval = process violation

---

### 4. 3-Day Review Cycle (OBRIGATÓRIO - Most Critical)

**Authority**: SPRINT_PROCESS.md lines 173-250, 318-332
**When**: After ALL implementation sessions complete
**Duration**: 6-9 hours (split over 3 days)
**Who**: bill-review symbiota, Jorge the Forge symbiota, Stakeholder

**This is the ceremony that caused Sprint 6 rejection.**

#### DAY 1: Technical Review (bill-review) - OBRIGATÓRIO

**Duration**: 2-3 hours
**Who**: bill-review symbiota

**What Happens**:
1. Invoke bill-review agent
2. Validate technical compliance:
   - All features implemented
   - All tests passing (100%)
   - Coverage ≥ 80%
   - Lint clean (0 errors)
   - Type check clean (0 errors)
   - Clean Architecture compliance
   - Code quality

3. Create `project/sprints/sprint-N/review.md`
4. **Decision**: APROVADO / CONDICIONAL / REJEITADO

**Target Score**: ≥9.0/10

**Deliverable**: `review.md` created

**Failure**: Sprint cannot proceed to Day 2

---

#### DAY 2: Process Review (Jorge the Forge) - OBRIGATÓRIO

**Duration**: 2-3 hours
**Who**: Jorge the Forge symbiota

**What Happens**:
1. Invoke Jorge the Forge process review
2. Validate ForgeProcess compliance:
   - Planning phase quality
   - MDD phase execution
   - Real-time progress tracking
   - TDD/BDD adherence
   - Session workflow
   - Artifact quality

3. Create `project/sprints/sprint-N/jorge-process-review.md`
4. **Decision**: APPROVED / CONDITIONAL / NEEDS IMPROVEMENT

**Target Score**: ≥7.0/10 (≥8.0/10 for redemption sprints)

**Deliverable**: `jorge-process-review.md` created

**Failure**: Sprint closure delayed until improvements made

---

#### DAY 3: Stakeholder Presentation & Retrospective - OBRIGATÓRIO

**Duration**: 2-3 hours
**Who**: Stakeholder + Assistant

**Part A: Stakeholder Presentation** (1-1.5h)

1. Present bill-review findings (15 min)
2. Present Jorge findings (15 min)
3. Execute interactive demos (30 min)
4. Obtain final stakeholder approval (15 min):
   - ✅ APPROVED → Sprint marked DONE
   - 🔄 CONDITIONAL → Minor fixes, then approved
   - ❌ REJECTED → Sprint incomplete

**Part B: Retrospective** (1-1.5h)

5. Retrospective discussion (45 min):
   - What went well ✅
   - What didn't go well ❌
   - Action items 🎯

6. Document retrospective (30 min):
   - Create `project/sprints/sprint-N/retrospective.md`

7. Update artifacts (15 min):
   - Update BACKLOG.md
   - Update ROADMAP.md
   - Update progress.md (final status)

8. Implement approved process improvements

**Deliverable**: `retrospective.md` created

**Failure**: Sprint NOT DONE (per line 329)

---

## DEFINITION OF DONE (DoD)

**Sprint is DONE when ALL checkboxes are checked:**

### Technical Criteria (OBRIGATÓRIO)
- [ ] All features implemented (100% story points)
- [ ] All tests passing (100%)
- [ ] Coverage ≥ 80%
- [ ] Lint errors: 0
- [ ] Type check errors: 0
- [ ] Documentation updated
- [ ] Demo functional

### Process Criteria (OBRIGATÓRIO - Lines 326-329)
- [ ] **Bill-review aprovado** (line 326)
- [ ] **Jorge the Forge aprovado** (line 327)
- [ ] **review.md documented** (line 329)
- [ ] **retrospective.md documented** (line 329)
- [ ] Demo validated by stakeholder
- [ ] Process improvements implemented (if approved)

### Artifact Checklist (OBRIGATÓRIO)
- [ ] planning.md (created BEFORE sprint)
- [ ] design.md (created Session 1 - MDD phase)
- [ ] progress.md (updated AFTER EACH session)
- [ ] review.md (created Day 1)
- [ ] jorge-process-review.md (created Day 2)
- [ ] retrospective.md (created Day 3)

**Missing ANY item = Sprint NOT DONE**

---

## ASSISTANT INSTRUCTIONS

### MANDATORY Process Consultation Gate

**BEFORE suggesting ANY sprint closure approach, assistant MUST:**

```python
def pre_closure_consultation_gate():
    """MANDATORY gate before suggesting sprint closure."""

    # Step 1: READ process documentation
    sprint_process = read_file("process/delivery/sprint/SPRINT_PROCESS.md", lines=(318, 332))

    # Step 2: IDENTIFY mandatory gates
    mandatory_gates = [
        "Bill-review aprovado",
        "Jorge the Forge aprovado",
        "Review e retrospective documentados"
    ]

    # Step 3: VERIFY all gates completed
    for gate in mandatory_gates:
        assert gate_completed(gate) == True, f"BLOCKER: {gate} not complete"

    # Step 4: CITE specific process documentation
    # Step 5: NEVER suggest shortcuts
```

### Response Template (MANDATORY)

When user asks: **"What remains to finish sprint?"**

**CORRECT Response**:
```
Para finalizar Sprint X, devemos executar o ciclo de 3 dias conforme
SPRINT_PROCESS.md linhas 318-332 (Sprint Success Criteria):

**OBRIGATÓRIO** (mandatory):
- [ ] Bill-review aprovado (validação técnica) - Day 1
      ↳ Target: ≥9.0/10
      ↳ Duration: 2-3 hours

- [ ] Jorge the Forge aprovado (validação de processo) - Day 2
      ↳ Target: ≥7.0/10 (or ≥8.0/10 for redemption)
      ↳ Duration: 2-3 hours

- [ ] Review e retrospective documentados - Day 3
      ↳ Stakeholder presentation + retrospective
      ↳ Duration: 2-3 hours

**Este ciclo de 3 dias é NON-NEGOTIABLE.** Não há atalhos permitidos.
```

**FORBIDDEN Phrases** (NEVER say these):
- ❌ "Sprint Review is optional"
- ❌ "You can skip X if..."
- ❌ "We can finish in 30-60 minutes"
- ❌ "Let's just commit and call it done"

### User Challenge Protocol

**If user challenges a process suggestion:**

1. ✅ STOP immediately (don't defend)
2. ✅ Consult SPRINT_PROCESS.md lines 318-332
3. ✅ Admit error (if suggestion was incorrect)
4. ✅ Cite correct process (with line numbers)
5. ✅ Thank user (for catching the error)

---

## CEREMONY TIMELINE (VISUAL)

### Typical 2-Week Sprint

```
WEEK 1: Implementation Phase
┌─────────────────────────────────────────────────────────────┐
│ Day 1     │ Day 2-7                                          │
├─────────────────────────────────────────────────────────────┤
│ ✅ Sprint │ Implementation Sessions (2-3 sessions)           │
│ Planning  │ - Session checkpoints AFTER EACH ✅              │
│ (BEFORE   │ - Session reviews END of EACH ✅                 │
│ start)    │ - Update progress.md AFTER EACH ✅               │
└─────────────────────────────────────────────────────────────┘

WEEK 2: Implementation + Review Cycle
┌─────────────────────────────────────────────────────────────┐
│ Day 1-5                  │ Day 6-8 (3-DAY REVIEW CYCLE)     │
├─────────────────────────────────────────────────────────────┤
│ Implementation Sessions  │ 🔴 DAY 1: bill-review (MANDATORY)│
│ (1-2 sessions)           │ 🔴 DAY 2: Jorge review (MANDATORY)│
│ - Checkpoints ✅         │ 🔴 DAY 3: Retrospective (MANDATORY)│
│ - Reviews ✅             │                                   │
└─────────────────────────────────────────────────────────────┘

🔴 = OBRIGATÓRIO (non-negotiable)
✅ = Checkpoint required
```

---

## CEREMONY DURATION SUMMARY

| Ceremony | Frequency | Duration/Instance | Total |
|----------|-----------|-------------------|-------|
| Sprint Planning | Once (start) | 3-4h | 3-4h |
| Session Checkpoints | Per session (4-5×) | 15-30 min | 1-2.5h |
| Session Reviews | Per session (4-5×) | 15-30 min | 1-2.5h |
| **3-Day Review Cycle** | **Once (end)** | **6-9h** | **6-9h** 🔴 |
| - Day 1: bill-review | Once | 2-3h | 2-3h 🔴 |
| - Day 2: Jorge review | Once | 2-3h | 2-3h 🔴 |
| - Day 3: Retrospective | Once | 2-3h | 2-3h 🔴 |
| **Total Ceremony Time** | --- | --- | **11-18h** |

**Implementation Time**: 12-20h (sessions)
**Total Sprint Time**: 23-38h (implementation + ceremonies)

---

## FREQUENTLY ASKED QUESTIONS (FAQ)

### Q: "Can we skip bill-review since code is clean?"

**A**: No. Bill-review is "OBRIGATÓRIO" (MANDATORY) per SPRINT_PROCESS.md line 326. It cannot be skipped regardless of code quality.

---

### Q: "Can we combine review days into one day?"

**A**: No. The 3-day review cycle is structured as 3 SEPARATE days per SPRINT_PROCESS.md. Each day has distinct objectives and reviewers. This is NON-NEGOTIABLE per lines 326-327.

---

### Q: "Is retrospective.md mandatory or recommended?"

**A**: Retrospective is MANDATORY (OBRIGATÓRIO). Evidence: SPRINT_PROCESS.md line 329 states "Review e retrospective documentados" under Sprint Success Criteria. Missing retrospective.md = Sprint NOT DONE.

---

### Q: "Can we start next sprint before completing retrospective?"

**A**: No. Current sprint must be formally CLOSED (retrospective.md created) before next sprint planning begins. No overlapping sprints.

---

## INCIDENT PREVENTION

### Red Flags (STOP and Consult Documentation)

**If assistant is about to say ANY of these, STOP IMMEDIATELY:**

- [ ] ❌ "Sprint Review is optional"
- [ ] ❌ "You can skip X if..."
- [ ] ❌ "Let's shortcut by..."
- [ ] ❌ "We can finish in 30-60 minutes"
- [ ] ❌ "bill-review isn't needed for small changes"
- [ ] ❌ "Jorge review is overkill"

**Action**: Read SPRINT_PROCESS.md lines 318-332, rewrite response citing documentation.

---

### Green Flags (Good Process Communication)

- [ ] ✅ "Per SPRINT_PROCESS.md lines 318-332..."
- [ ] ✅ "This is OBRIGATÓRIO (MANDATORY), not optional"
- [ ] ✅ "The 3-day review cycle is NON-NEGOTIABLE"
- [ ] ✅ "No shortcuts are permitted for mandatory gates"

---

## COMPLIANCE SCORING

### How Jorge Evaluates Ceremony Adherence

**Phase Weights**:
- Planning Phase: 30%
- Execution Phase: 30%
- Closure Phase: 40% ← Where Sprint 6 failed (0.0/10)

**Closure Phase Scoring** (40% of total):
- 3-day review cycle executed: 30% (3.0/10)
- bill-review completed: 20% (2.0/10)
- Jorge review completed: 20% (2.0/10)
- Retrospective documented: 15% (1.5/10)
- No shortcuts suggested: 15% (1.5/10)

**If assistant suggests "optional" review → INSTANT 0.0/10 closure score**

---

## SUMMARY TABLE (ONE-PAGE REFERENCE)

| # | Ceremony | When | Duration | Classification | Can Skip? |
|---|----------|------|----------|----------------|-----------|
| 1 | Sprint Planning | Before start | 3-4h | 🔴 OBRIGATÓRIO | ❌ NO |
| 2 | Session Checkpoints | After EACH session | 15-30 min | 🔴 OBRIGATÓRIO | ❌ NO |
| 3 | Session Reviews | End EACH session | 15-30 min | 🔴 OBRIGATÓRIO | ❌ NO |
| 4 | 3-Day Review Cycle | After all sessions | 6-9h | 🔴 OBRIGATÓRIO | ❌ NO |
|   | └─ bill-review | Day 1 | 2-3h | 🔴 OBRIGATÓRIO | ❌ NO |
|   | └─ Jorge review | Day 2 | 2-3h | 🔴 OBRIGATÓRIO | ❌ NO |
|   | └─ Retrospective | Day 3 | 2-3h | 🔴 OBRIGATÓRIO | ❌ NO |

**Authority**: SPRINT_PROCESS.md lines 318-332
**Violation Consequence**: Sprint rejection (0.0/10 closure)

---

## SIGNATURE

**Document Type**: ForgeProcess Practice (MANDATORY)
**Version**: 1.0
**Date Created**: 2025-11-07
**Author**: Jorge the Forge (symbiota de processo)
**Reviewed By**: Stakeholder
**Status**: ✅ **ACTIVE** - Binding for ALL sprints

**Usage**:
- Assistants MUST consult this document before suggesting sprint closure
- Users MAY challenge assistants using this document as authority
- This practice supersedes any conflicting informal guidance

**Next Review**: After Sprint 7 completion (validate practice effectiveness)

---

*"ForgeProcess exists to protect trust. Violating process breaks trust. Rebuilding trust requires transparency, accountability, and sustained excellence."*

— Jorge the Forge

---

**END OF CEREMONY SCHEDULE PRACTICE**
