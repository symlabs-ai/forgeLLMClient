# MVP Exception Policy - ForgeProcess Guidelines

**Version**: 1.0
**Created**: 2025-11-06
**Status**: Active
**Authority**: Approved by Jorge the Forge (process review) + Stakeholder

---

## 🎯 Purpose

This document defines when MVP (Minimum Viable Product) features are acceptable as an exception to the standard ForgeProcess BDD mandate.

**Standard Rule**: ALL features MUST have complete BDD scenarios (`.feature` files) before implementation.

**MVP Exception**: Under specific conditions, features may be delivered as MVP with reduced BDD coverage.

---

## ⚠️ Why This Policy Exists

**Sprint 1 Experience (2025-11-06)**:
- F11_MVP (Streaming) and F12A_MVP (Tool Calling) were delivered as MVPs
- **Trade-off**: Faster delivery (5 pts MVP vs 13+ pts Full) but violated BDD mandate
- **Result**: Stakeholder approved value, but Jorge flagged process violation
- **Lesson**: MVP strategy works in practice but needs formal guidelines

**Jorge's Assessment** (7.8/10 - CONDITIONAL):
> "MVP features bypassed BDD (SEVERITY: HIGH). Need explicit guideline for when MVP is acceptable."

---

## ✅ When MVP is Acceptable

An MVP feature is acceptable if **ALL** of the following criteria are met:

### 1. Stakeholder Approval (MANDATORY)
- [ ] **Stakeholder explicitly approves MVP approach** (documented in planning)
- [ ] **Stakeholder understands trade-offs**: Faster delivery vs. incomplete testing
- [ ] **Stakeholder prioritizes speed over full validation** for this specific feature

**Documentation**: Record approval in `project/sprints/sprint-N/planning.md` or meeting notes

---

### 2. Value Validation (MANDATORY)
- [ ] **Interactive demo validates core value** (ADR-010 checklist)
- [ ] **Demo uses real API/integration** (not mocked)
- [ ] **Core use case works end-to-end**
- [ ] **Known limitations documented** in demo output

**Documentation**: Demo script in `examples/sprint[N]/run_demo_[feature]_mvp.sh`

---

### 3. Full Implementation Planned (MANDATORY)
- [ ] **Full Implementation tracked in BACKLOG.md** with story points
- [ ] **Target sprint identified** (e.g., "F11_Full in Sprint 2")
- [ ] **Full Implementation includes**:
  - Complete BDD scenarios (`.feature` file)
  - Full test coverage (unit + integration)
  - Edge case handling
  - Production-ready error handling

**Documentation**: BACKLOG.md shows `F[XX]_MVP` + `F[XX]_Full` with separate story points

---

### 4. Incomplete Status Documented (MANDATORY)
- [ ] **Feature marked as MVP in BACKLOG.md** (e.g., `F11_MVP - Streaming (MVP)`)
- [ ] **Known limitations listed** in feature documentation
- [ ] **Not production-ready** label clear
- [ ] **Full Implementation linked** in documentation

**Documentation**: README, feature docs, BACKLOG.md all reference MVP status

---

## ❌ When MVP is NOT Acceptable

**Never use MVP approach for:**

1. **Core/Critical Features**
   - Authentication, authorization, security features
   - Data integrity features (writes, updates, deletes)
   - Payment processing, financial features
   - Features with compliance requirements

2. **Simple Features**
   - Features < 3 story points (just implement fully)
   - Features that can be completed in 1 session
   - Features without external dependencies

3. **Bug Fixes**
   - All bug fixes must have regression tests (BDD)
   - MVP doesn't apply to fixes

4. **Refactorings**
   - Refactorings must maintain test coverage
   - MVP doesn't apply to refactoring

---

## 📋 MVP Proposal Template

Use this template when proposing an MVP feature:

```markdown
## MVP Proposal: [Feature Name]

**Feature ID**: F[XX]_MVP
**Full Feature ID**: F[XX]_Full
**Proposed by**: [Developer/Agent]
**Date**: YYYY-MM-DD

### Justification

**Why MVP?**
[Explain why MVP approach is needed - e.g., validate technical feasibility, get early feedback, complex feature]

**Value Delivered (MVP)**:
- [Core use case 1]
- [Core use case 2]

**Value Deferred (Full)**:
- [Edge cases]
- [Full BDD scenarios]
- [Production hardening]

### Criteria Checklist

- [ ] 1. Stakeholder approval obtained
- [ ] 2. Interactive demo validates value
- [ ] 3. Full Implementation planned (F[XX]_Full in Sprint [N])
- [ ] 4. Incomplete status will be documented

### Story Points

- **MVP**: [X] pts (demo + basic implementation)
- **Full**: [Y] pts (BDD + tests + edge cases)
- **Total**: [X+Y] pts
- **Time Saved**: [Y] pts deferred to Sprint [N]

### Stakeholder Decision

**Decision**: ✅ APPROVED / ❌ REJECTED

**Approved by**: [Stakeholder Name]
**Date**: YYYY-MM-DD
**Conditions**: [Any conditions for approval]

---

**If APPROVED**:
- Add F[XX]_MVP to current sprint backlog ([X] pts)
- Add F[XX]_Full to Sprint [N] backlog ([Y] pts)
- Mark MVP as "incomplete" in BACKLOG.md

**If REJECTED**:
- Implement full feature (F[XX]) with complete BDD
- Allocate [X+Y] pts in current sprint or defer entirely
```

---

## 🔄 MVP → Full Implementation Workflow

### Phase 1: MVP Delivery

1. **Propose MVP** (use template above)
2. **Get stakeholder approval** (documented)
3. **Implement MVP**:
   - Core functionality only
   - Demo script (ADR-010 compliant)
   - Minimal tests (optional BDD scenarios)
4. **Validate with stakeholder** (interactive demo)
5. **Mark as incomplete** in BACKLOG.md
6. **Commit with clear MVP label**

### Phase 2: Full Implementation (Future Sprint)

1. **Create complete BDD scenarios** (`.feature` file)
2. **Implement step definitions** (tests/bdd/)
3. **Add edge case handling**
4. **Add error handling** (production-ready)
5. **Achieve ≥80% coverage**
6. **Update documentation** (remove MVP label)
7. **Run full review** (bill-review + Jorge)

---

## 📊 MVP Examples from Sprint 1

### Example 1: F11_MVP - Streaming Support ✅

**Why MVP?**
- Streaming is complex (13 pts full)
- Needed to validate OpenAI streaming API works
- Stakeholder wanted early feedback on UX

**MVP Delivered** (5 pts):
- Basic streaming demo working
- Real OpenAI API integration
- Interactive demo validated

**Full Implementation Deferred** (8 pts):
- Complete BDD scenarios
- Error handling (network failures, partial streams)
- Fallback to non-streaming
- Integration tests

**Status**: ✅ MVP approved, F11_Full planned for Sprint 2

---

### Example 2: F12A_MVP - Tool Calling Support ✅

**Why MVP?**
- Tool calling is complex (8+ pts full)
- Needed to validate OpenAI Functions API works
- Stakeholder wanted proof of concept

**MVP Delivered** (5 pts):
- Basic tool calling demo working
- Weather function example
- Real OpenAI API integration
- Interactive demo validated

**Full Implementation Deferred** (3 pts):
- Complete BDD scenarios
- Multiple tool examples
- Tool registry system
- Error handling

**Status**: ✅ MVP approved, F12B_Full planned for Sprint 2

---

## 🚨 Process Compliance

### Jorge's Validation Criteria

For MVP features to pass Jorge's process review (≥8/10):

1. **MVP exception policy exists** (this document) ✅
2. **Stakeholder approval documented** for each MVP
3. **Full Implementation planned** in BACKLOG.md
4. **ADR-010 compliance** (demo validation mandatory)
5. **MVP status clearly marked** in all documentation

### bill-review Validation Criteria

For MVP features to pass bill-review (≥8/10):

1. **Core functionality works** (demo validated)
2. **Clean Architecture maintained** (even in MVP)
3. **No technical debt** (MVP ≠ bad code)
4. **Documentation exists** (README, comments)
5. **Minimal tests** (at least demo script)

---

## 📝 Documentation Requirements

### BACKLOG.md Format

```markdown
## Sprint N

### Features

- [ ] **F11_MVP**: Streaming support (MVP) - 5 pts ⚠️ INCOMPLETE
  - **Status**: MVP delivered, Full Implementation pending
  - **Full**: F11_Full in Sprint 2 (8 pts)
  - **Limitations**: No error handling, no BDD scenarios
  - **Demo**: `examples/sprint1/run_demo_streaming_mvp.sh`

### Sprint N+1

- [ ] **F11_Full**: Streaming support (Full Implementation) - 8 pts
  - **Depends on**: F11_MVP (completed)
  - **Adds**: BDD scenarios, error handling, fallbacks
  - **Completes**: F11 feature fully
```

### README.md Format

```markdown
## Features

### Streaming Support ⚠️ MVP

**Status**: Minimum Viable Product (not production-ready)

**What Works**:
- Basic streaming from OpenAI
- Real-time token-by-token output

**Known Limitations**:
- No error handling for network failures
- No fallback to non-streaming
- No BDD test coverage

**Full Implementation**: Planned for Sprint 2 (F11_Full)
```

---

## 🔗 References

- **ForgeProcess**: `process/PROCESS.md`
- **BDD Process**: `process/bdd/BDD_PROCESS.md`
- **ADR-010**: Pre-Stakeholder Validation Mandate
- **Sprint 1 Retrospective**: `project/sprints/sprint-1/retrospective.md`
- **Jorge's Review**: `project/sprints/sprint-1/jorge-process-review.md`

---

## ✅ Approval

**Policy Approved By**: Jorge the Forge (process review)
**Stakeholder Approved By**: Rodrigo Palhano
**Date**: 2025-11-06
**Status**: Active for Sprint 2+

**Key Takeaway**: MVP is a valid strategy when used responsibly with stakeholder approval, clear documentation, and planned full implementation. This policy formalizes what worked in Sprint 1 while ensuring process compliance.

---

**Version History**:
- v1.0 (2025-11-06): Initial version based on Sprint 1 learnings and Jorge's recommendations
