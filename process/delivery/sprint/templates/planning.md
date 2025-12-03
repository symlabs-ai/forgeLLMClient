# Sprint [N] - Planning

**Project**: forgeLLMClient
**Sprint Number**: [N]
**Sprint Duration**: [Start Date] - [End Date] (typically 2 weeks)
**Planning Date**: YYYY-MM-DD
**Team**: Agent Coders (Claude Code primary)
**Stakeholder**: [Stakeholder Name]

---

## 📊 Sprint Overview

### Sprint Goals

**Primary Goal**: [Main objective of this sprint - what value are we delivering?]

**Secondary Goals** (if applicable):
- [Goal 2]
- [Goal 3]

**Success Criteria**:
- [ ] [Specific measurable outcome 1]
- [ ] [Specific measurable outcome 2]
- [ ] [Specific measurable outcome 3]

---

## 📈 Capacity Planning

### Velocity Baseline

**Previous Sprint(s) Velocity**:
- Sprint [N-1]: [X] pts / [Y] sessions = [Z] pts/session
- Sprint [N-2]: [X] pts / [Y] sessions = [Z] pts/session (if applicable)

**Adjusted Velocity** (for this sprint):
- [X] pts/session (considering [factors: MVP vs Full, complexity, etc.])

### Capacity Calculation

**Sessions Available**: [N] sessions
- Frequency: [X] sessions/week × [Y] weeks = [N] sessions total
- Duration: [X-Y] hours per session (estimated)

**Projected Capacity**: [N sessions] × [X pts/session] = **[Total] story points**

**Buffer**: [±X%] for unknowns/risks

**Final Capacity Range**: [Min]-[Max] story points

---

## ✅ Features Selected (from BACKLOG.md)

### Committed Features

| Feature ID | Feature Name | Story Points | Priority | Status |
|------------|--------------|--------------|----------|--------|
| [F0X] | [Feature name] | [X] pts | HIGH | Committed |
| [F0Y] | [Feature name] | [Y] pts | HIGH | Committed |
| **Total Committed** | | **[XX] pts** | | |

**Rationale**: [Why these features were selected]

### Stretch Goals (Optional)

| Feature ID | Feature Name | Story Points | Priority | Status |
|------------|--------------|--------------|----------|--------|
| [F0Z] | [Feature name] | [Z] pts | MEDIUM | Stretch |
| **Total Stretch** | | **[YY] pts** | | |

**Stretch Conditions**: [Under what conditions will we tackle stretch goals?]

---

## 🔗 Dependencies & Prerequisites

### Technical Dependencies

- [ ] **Dependency 1**: [Description] (Blocks: [Feature IDs])
- [ ] **Dependency 2**: [Description] (Blocks: [Feature IDs])

### External Dependencies

- [ ] **External System 1**: [e.g., API access, credentials]
- [ ] **External System 2**: [e.g., Third-party service]

### Process Dependencies

- [ ] **Previous Sprint Artifacts Complete**: Sprint [N-1] review, retrospective done
- [ ] **Process Improvements Implemented**: [e.g., ADR-010, MVP guidelines]
- [ ] **Environment Setup**: [e.g., dev dependencies installed]

---

## ⚠️ Risks & Mitigation

### Identified Risks

#### Risk 1: [Risk Title]
- **Probability**: [Low/Medium/High]
- **Impact**: [Low/Medium/High]
- **Description**: [What could go wrong]
- **Mitigation**: [How we'll prevent or handle it]
- **Contingency**: [Fallback plan if mitigation fails]

#### Risk 2: [Risk Title]
- **Probability**: [Low/Medium/High]
- **Impact**: [Low/Medium/High]
- **Description**: [What could go wrong]
- **Mitigation**: [How we'll prevent or handle it]
- **Contingency**: [Fallback plan if mitigation fails]

### Risk Score

**Overall Risk Level**: [Low/Medium/High]

**Confidence Level**: [Low/Medium/High] - How confident are we in completing planned features?

---

## 📋 Definition of Done

### Feature-Level DoD

A feature is considered DONE when:

- [ ] **BDD Scenarios**: Complete `.feature` file exists (OR MVP exception documented)
- [ ] **Implementation**: All BDD scenarios pass (OR MVP has working demo)
- [ ] **Tests**: Coverage ≥80% (OR MVP has validation demo - ADR-010)
- [ ] **Code Quality**: Lint clean, type check clean
- [ ] **Architecture**: Clean Architecture maintained, Forgebase compliant
- [ ] **Documentation**: README updated, docstrings complete
- [ ] **Demo**: ADR-010 validation checklist complete
- [ ] **Review**: Stakeholder approval obtained
- [ ] **Commit**: Code committed with clear message

### Sprint-Level DoD

This sprint is considered DONE when:

- [ ] **All Committed Features**: 100% of committed features are DONE
- [ ] **Quality Gates**: bill-review ≥8/10, Jorge review ≥8/10
- [ ] **Test Coverage**: Overall coverage ≥80%
- [ ] **No Critical Issues**: Zero critical bugs or technical debt
- [ ] **Documentation**: Sprint artifacts complete (planning, progress, review, retrospective)
- [ ] **Process Compliance**: ADR-010 followed, BDD mandate followed (or MVP exception)
- [ ] **Stakeholder Approval**: Final sprint review approved
- [ ] **Process Improvements**: Approved improvements from previous sprint implemented

---

## 📅 Sprint Timeline

### Key Milestones

| Date | Milestone | Owner |
|------|-----------|-------|
| [YYYY-MM-DD] | Sprint Planning Complete | Team |
| [YYYY-MM-DD] | Mid-Sprint Checkpoint | Team |
| [YYYY-MM-DD] | Feature Freeze (commit deadline) | Team |
| [YYYY-MM-DD] | bill-review (Day 1) | bill-review symbiota |
| [YYYY-MM-DD] | Jorge review (Day 2) | Jorge the Forge |
| [YYYY-MM-DD] | Sprint Review & Retrospective (Day 3) | Stakeholder + Team |

### Session Frequency

**Target**: [X] sessions/week
**Typical Duration**: [Y]-[Z] hours per session

**Estimated Sessions**:
- Week 1: [N] sessions
- Week 2: [N] sessions
- **Total**: [N] sessions

---

## 🎯 Feature Breakdown

### F[XX]: [Feature Name] ([X] pts)

**Description**: [Brief description of what this feature does]

**Value**: [What value does this deliver? Which ValueTrack does it support?]

**BDD Feature File**: `specs/bdd/features/[feature].feature`

**Acceptance Criteria**:
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

**Dependencies**: [List any dependencies]

**Risks**: [Any specific risks for this feature]

**Estimated Effort**: [X] pts ([Y-Z] sessions estimated)

---

### F[YY]: [Feature Name] ([Y] pts)

[Repeat structure for each committed feature]

---

## 📝 MVP Proposals (if applicable)

### MVP-1: [Feature Name]

**Feature ID**: F[XX]_MVP
**Full Feature ID**: F[XX]_Full

**Why MVP?**: [Justification - e.g., validate feasibility, complex feature]

**MVP Delivers** ([X] pts):
- [Core use case 1]
- [Core use case 2]

**Deferred to Full** ([Y] pts):
- [Edge cases]
- [Full BDD]
- [Production hardening]

**Stakeholder Approval**:
- [ ] Stakeholder explicitly approves MVP approach
- [ ] Full Implementation planned for Sprint [N+X]
- [ ] MVP limitations documented

**Status**: ✅ APPROVED / ❌ REJECTED / ⏳ PENDING

---

## 🔄 Process Improvements (from Previous Sprint)

### Implemented Before This Sprint

- [x] **AI-1**: [Description of improvement implemented]
- [x] **AI-2**: [Description of improvement implemented]

### To Implement During This Sprint

- [ ] **Improvement 1**: [Description]
- [ ] **Improvement 2**: [Description]

---

## 📊 Comparison to Previous Sprint

| Metric | Sprint [N-1] | Sprint [N] (Planned) | Change |
|--------|--------------|----------------------|--------|
| **Story Points** | [X] pts | [Y] pts | [±Z%] |
| **Features** | [X] | [Y] | [±Z] |
| **Sessions** | [X] | [Y] | [±Z] |
| **Velocity** | [X] pts/session | [Y] pts/session | [±Z%] |

---

## ✅ Planning Sign-Off

### Team Commitment

**Team Commits To**:
- Deliver [XX] story points (committed features)
- Maintain quality standards (bill ≥8/10, Jorge ≥8/10)
- Follow ForgeProcess (TDD, BDD, ADR-010)
- Complete sprint artifacts (progress, review, retrospective)

**Team Concerns**: [Any concerns or caveats]

### Stakeholder Approval

**Stakeholder Approves**:
- [ ] Sprint goals are clear and valuable
- [ ] Feature selection aligns with priorities
- [ ] Capacity estimation is reasonable
- [ ] Risks are understood and acceptable
- [ ] DoD is clear and achievable

**Stakeholder Comments**: [Any feedback or adjustments]

**Approved By**: [Stakeholder Name]
**Date**: YYYY-MM-DD

---

## 📚 References

- **Backlog**: `specs/roadmap/BACKLOG.md`
- **Roadmap**: `specs/roadmap/ROADMAP.md`
- **Previous Sprint Review**: `project/sprints/sprint-[N-1]/review.md`
- **Previous Sprint Retrospective**: `project/sprints/sprint-[N-1]/retrospective.md`
- **ForgeProcess**: `process/PROCESS.md`
- **TDD Process**: `process/execution/tdd/TDD_PROCESS.md`
- **BDD Process**: `process/bdd/BDD_PROCESS.md`

---

**Template Version**: 1.0
**Created**: 2025-11-06
**Last Updated**: 2025-11-06
**Status**: Active for Sprint 2+
