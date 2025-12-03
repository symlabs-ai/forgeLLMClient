# Stakeholder Priority Changes - ForgeProcess Extension

**Version**: 1.0
**Last Updated**: 2025-11-06
**Status**: ACTIVE
**Related**: ADR-009, BACKLOG.md

---

## Overview

This document defines the process for handling **stakeholder-driven priority changes** during sprint execution in ForgeProcess.

**Context**: ForgeProcess operates with agent coders in session-based workflow. Unlike traditional teams with async communication, stakeholders are **present during sessions** and can request immediate priority changes.

**Purpose**: Ensure priority changes are:
1. **Documented** (via ADR)
2. **Impact-analyzed** (risks, timeline, scope)
3. **Formally approved** (stakeholder signs off on consequences)
4. **Traceable** (linked to BACKLOG, commits)

---

## When to Use This Process

### Priority Change Triggers:

**Immediate (within current sprint)**:
- Stakeholder identifies critical missing feature during demo
- Market/business requirements shift mid-sprint
- Technical discovery reveals higher-value alternative
- Blocker requires scope adjustment to unblock

**Deferred (next sprint)**:
- Feature request that doesn't impact current sprint timeline
- Nice-to-have enhancements (can wait for sprint planning)
- Exploratory features (spike needed first)

**Use this process for**: IMMEDIATE changes only.
**For deferred**: Add to BACKLOG, discuss in next sprint planning.

---

## Process Workflow

### Step 1: Stakeholder Requests Change

**During session**, stakeholder identifies need for priority change:

```
Stakeholder: "I need Streaming + Tool Calling features ASAP.
              Can we prioritize them over F04 (chat_http)?"
```

**Agent Response**:
1. Acknowledge request
2. Propose options (see Step 2)
3. **Do NOT implement immediately** (wait for formal approval)

---

### Step 2: Present Options & Impact Analysis

**Agent prepares**:

#### A. **Options Matrix**

Present 2-4 alternatives with pros/cons:

| Option | Scope | Timeline | Risk |
|--------|-------|----------|------|
| A: Follow roadmap | No change | As planned | Low |
| B: Full anticipation | Add Sprint 3 features now | +4 weeks | High |
| C: MVP Simplification | Add minimal version | +2 weeks | Medium |
| D: Other | Custom | TBD | TBD |

#### B. **Impact Analysis** (for each option)

- **Sprint duration change** (+X pts, +Y sessions)
- **Features added/deferred** (list explicitly)
- **Dependencies affected** (what breaks/changes)
- **Risks** (technical, timeline, scope creep)
- **Mitigations** (how to reduce risks)

**Example**:
```markdown
## Option C: MVP Simplification

### Added:
- F11_MVP (Streaming MVP): 5pts, OpenAI only
- F12A_MVP (Tool Calling MVP): 5pts, OpenAI only
- Total: +10pts

### Deferred:
- F04 (chat_http): 3pts → moved to Sprint 2

### Net Impact:
- Sprint 1: 22pts → 26pts (+18%)
- Estimated: +2-3 sessions

### Risks:
- MVP limitations (no fallback, single provider)
- Sprint 1 duration extends
- F04 delayed (low impact, STDIO works)

### Mitigations:
- Clear MVP scope (no feature creep)
- Stakeholder aware of limitations
- bill-review validates MVP scope compliance
```

---

### Step 3: Stakeholder Decision

**Stakeholder reviews options and selects one**:

```
Stakeholder: "Option C (MVP Simplification).
              I accept the risks and timeline adjustment."
```

**Agent confirms**:
- "You're choosing Option C"
- "This adds 10pts to Sprint 1 (26pts total)"
- "F04 will be deferred to Sprint 2"
- "MVP will be OpenAI-only, no fallback logic"
- **"Do you confirm and approve?"**

**Stakeholder**: "Yes, approved."

---

### Step 4: Document Decision (ADR)

**Agent creates ADR-XXX**:

Use template from `specs/adr/ADR-009-template.md`:

```markdown
# ADR-XXX: [Title]

**Status**: ✅ ACCEPTED
**Date**: YYYY-MM-DD
**Decider**: [Stakeholder Name]
**Context**: [Sprint/Feature context]

## Context
[Why priority change was requested]
[Business justification]

## Decision
[What is being prioritized]
[What is being deferred]
[Selected option from Step 2]

## Rationale
[Why this option vs others]
[Stakeholder's reasoning]
[Business value justification]

## Consequences

### Positive Impacts:
- [List benefits]

### Negative Impacts:
- [List drawbacks, risks]

### Mitigations:
- [How risks will be addressed]

## Implementation Plan
[Tasks breakdown]
[Updated sprint scope]
[Acceptance criteria for new features]

## Stakeholder Approval
**Stakeholder**: [Name]
**Date**: [Date]
**Decision**: APPROVED

**Stakeholder acknowledges**:
- ✅ [Impact 1]
- ✅ [Impact 2]
- ✅ [Risk 1]
- ✅ [Risk 2]

## References
- BACKLOG.md
- Related ADRs
- Related handoffs
```

**Save to**: `specs/adr/ADR-XXX-<kebab-case-title>.md`

---

### Step 5: Update BACKLOG.md

**Update affected sprint sections**:

#### A. Sprint Header Adjustment

```markdown
## 🚀 Sprint 1: Foundation MVP ⚠️ SCOPE ADJUSTED

**Goal**: [Updated goal including new features]
**Story Points**: XXpts (adjusted from YYpts per ADR-XXX)
**Status**: 🟢 IN PROGRESS

**⚠️ Scope Change**: Per ADR-XXX stakeholder decision (YYYY-MM-DD):
- ✅ ADDED: F11_MVP - 5pts
- ✅ ADDED: F12A_MVP - 5pts
- ⏸️ DEFERRED: F04 → Sprint 2
```

#### B. Add New Features

For each added feature:
- Full feature specification (tasks, scenarios, acceptance criteria)
- Mark status as ⏳ PENDING
- Reference ADR-XXX in **ADR** field
- Clearly mark **Scope**: MVP (if applicable)
- List **Out of Scope** items (what's NOT included)

#### C. Mark Deferred Features

```markdown
### F04: chat_http.feature ⏸️ DEFERRED TO SPRINT 2

**Status**: ⏸️ DEFERRED (moved to Sprint 2 per ADR-XXX)
**Reason**: Stakeholder prioritized [X] over [Y]
```

Move full feature spec to target sprint.

#### D. Update Summary Tables

At end of BACKLOG:

```markdown
### By Sprint

| Sprint | Features | Story Points | Status |
|--------|----------|--------------|--------|
| Sprint 1 (adjusted) | X/Y | A/B pts | 🟢 IN PROGRESS (C%) |
...

**Note**: Sprint 1 scope adjusted per ADR-XXX ([reason])
```

---

### Step 6: Proceed with Implementation

**After Steps 1-5 complete**:

1. **Agent confirms with stakeholder**:
   - "Priority change documented (ADR-XXX ✅)"
   - "BACKLOG updated ✅"
   - "Ready to proceed with [Feature Name]?"

2. **Stakeholder**: "Yes, proceed"

3. **Agent follows normal TDD workflow**:
   - Write BDD scenarios (Red phase)
   - Implement (Green phase)
   - Refactor (Refactor phase)
   - Demo + validation
   - bill-review (validates MVP scope compliance)

4. **Same DoD applies** (no shortcuts for priority changes)

---

## Special Cases

### Case 1: Mid-Sprint Discovery (Blocker)

**Scenario**: Technical blocker requires scope change.

**Process**:
1. Agent identifies blocker during implementation
2. Agent documents blocker (what, why, impact)
3. Agent proposes alternatives (workaround vs scope change)
4. Follow Steps 2-6 above

**Example**:
```
Agent: "F11 implementation blocked: OpenAI Responses API doesn't support streaming.
        Options:
        A) Use chat.completions API (breaks ADR-008)
        B) Defer F11_MVP to Sprint 2
        C) Implement non-streaming version only"

Stakeholder: [selects option]
Agent: [creates ADR, updates BACKLOG]
```

### Case 2: Multiple Concurrent Changes

**Scenario**: Stakeholder requests 3+ changes at once.

**Process**:
1. Agent requests **prioritization** from stakeholder
2. "Which change is #1 priority? #2? #3?"
3. **One ADR per logical change** (don't bundle unrelated changes)
4. Update BACKLOG incrementally (one change at a time)

**Example ADRs**:
- ADR-009: Prioritize Streaming + Tool Calling MVP (related features)
- ADR-010: Defer HTTP endpoint (separate decision)

### Case 3: Scope Creep Prevention

**Scenario**: MVP starts expanding ("just add fallback logic...").

**Prevention**:
1. **bill-review validates MVP scope** (part of DoD)
2. Agent reminds stakeholder: "This is out of MVP scope per ADR-XXX"
3. If stakeholder insists: Create NEW ADR (scope expansion)
4. Re-estimate story points (MVP → Full feature)

**Agent script**:
```
Agent: "Adding fallback logic would increase F11_MVP from 5pts to 13pts.
        This was explicitly marked 'Out of Scope' in ADR-009.

        Options:
        A) Keep MVP scope (5pts, no fallback)
        B) Expand to full feature (13pts, +3-4 sessions)

        Which do you prefer?"
```

---

## Quality Gates

### Before Implementation:

- [ ] ADR created and saved
- [ ] BACKLOG updated (sprint headers, features, tables)
- [ ] Stakeholder approval documented in ADR
- [ ] Impact analysis complete (timeline, risks, mitigations)
- [ ] Clear acceptance criteria (what IS and ISN'T in scope)

### During Implementation:

- [ ] Follow normal TDD workflow (no shortcuts)
- [ ] MVP scope respected (no feature creep)
- [ ] Agent proactively reminds stakeholder of scope boundaries

### After Implementation:

- [ ] bill-review validates scope compliance
- [ ] Demo shows features within documented scope
- [ ] Stakeholder validates against ADR acceptance criteria
- [ ] Commit message references ADR number

---

## Tools & Templates

### ADR Template

See: `specs/adr/ADR-009-prioritize-streaming-toolcalling-mvp.md` (reference example)

### Impact Analysis Template

```markdown
## Impact Analysis: [Change Title]

### Scope Changes:
**Added**:
- Feature X: Ypts ([description])
- ...

**Deferred**:
- Feature Z: Ypts → Sprint N ([reason])
- ...

### Timeline Impact:
- Sprint [N]: XXpts → YYpts (+ZZ%)
- Estimated sessions: +A-B sessions
- New completion date: ~[date estimate]

### Dependencies:
- Features blocked: [list or "none"]
- Features unblocked: [list or "none"]

### Risks:
1. **[Risk name]** (Probability: H/M/L, Impact: H/M/L)
   - Mitigation: [how to address]
2. ...

### Acceptance Criteria (for new features):
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] ❌ NOT in scope: [explicit exclusions]
```

---

## Metrics & Retrospectives

### Track in Sprint Retrospective:

1. **Priority changes this sprint**: Count of ADRs created
2. **Scope adjustments**: Net story points added/removed
3. **Actual vs estimated impact**: Did +10pts really take +2 sessions?
4. **Scope creep incidents**: How many times MVP expanded?
5. **Stakeholder satisfaction**: Were priority changes handled well?

### Continuous Improvement:

- **Pattern analysis**: What triggers priority changes most often?
- **Estimation accuracy**: Are impact estimates getting better?
- **Process friction**: Where does this process slow down work?

---

## References

- **ADR-009**: First example of stakeholder priority change
- **BACKLOG.md**: Sprint scope documentation
- **PROCESS.md**: Base ForgeProcess methodology
- **process/delivery/sprint/**: Sprint planning and review processes

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2025-11-06 | Initial version (ADR-009 learning) | Agent Coder |

---

**Status**: ACTIVE
**Next Review**: After Sprint 1 Retrospective
