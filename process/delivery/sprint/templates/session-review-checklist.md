# Session Review Checklist

**Purpose**: Ensure feature is fully validated before commit
**When**: After Implementation, BEFORE Commit (Step 3 of Session Workflow)
**Duration**: 15-30min

---

## ⚠️ CRITICAL: This is a MANDATORY GATE

**DO NOT COMMIT** until ALL items below are checked ✅

**IF STAKEHOLDER IS NOT AVAILABLE**: STOP and schedule review. Do NOT commit without approval.

---

## 📋 Pre-Stakeholder Validation (Technical Gate)

### ✅ ADR-010: Pre-Stakeholder Validation Checklist

- [ ] **Demo Execution** ✅
  - [ ] Demo script executed successfully (no crashes)
  - [ ] Demo tested with REAL credentials (if applicable)
  - [ ] All scenarios completed without errors

- [ ] **BDD Tests** ✅
  - [ ] All BDD scenarios pass (pytest-bdd)
  - [ ] OR: Explicitly skip with documented reason (MVP exception)

- [ ] **Code Quality** ✅
  - [ ] Python syntax validated (no SyntaxError)
  - [ ] No CRLF issues in bash scripts
  - [ ] Lint clean (ruff)
  - [ ] Type check clean (mypy)

- [ ] **Documentation** ✅
  - [ ] BDD scenarios complete (or MVP exception documented)
  - [ ] Known limitations documented (if any)
  - [ ] Demo script created (examples/sprintN/demo_*.py)

**IF ADR-010 FAILS**: Fix issues, re-run. Do NOT proceed to stakeholder review.

---

## 🚨 Stakeholder Review (Approval Gate)

### ⚠️ STOP: Stakeholder Must Be Present/Available

**BEFORE PROCEEDING**: Ensure stakeholder is available for review.

- [ ] **Stakeholder is present/available** (synchronous session)
  - [ ] OR: Stakeholder review scheduled (async - WAIT for approval)

### 📊 Feature Presentation

- [ ] **Demo Presented to Stakeholder**
  - [ ] Ran demo script live with stakeholder watching
  - [ ] Explained what feature does
  - [ ] Showed all scenarios (happy path + edge cases)

- [ ] **Acceptance Criteria Validated WITH Stakeholder**
  - [ ] All acceptance criteria from BACKLOG.md met
  - [ ] Stakeholder confirmed feature solves intended problem
  - [ ] Edge cases discussed and validated

- [ ] **Questions & Feedback Collected**
  - [ ] Stakeholder asked questions (if any)
  - [ ] Feedback documented (if any)
  - [ ] Clarifications provided

### 🎯 Stakeholder Decision

**Stakeholder approval status** (check ONE):

- [ ] **✅ APPROVED**: Feature meets requirements, proceed to commit
- [ ] **❌ REJECTED**: Feature doesn't meet requirements, go back to implementation
- [ ] **🔄 NEEDS CHANGES**: Minor adjustments needed, fix and re-present

**IF APPROVED**: Proceed to "Optional Reviews" below, then commit.

**IF REJECTED or NEEDS CHANGES**:
1. Document feedback in `project/sprints/sprint-N/feedback-FXX.md`
2. Return to Implementation (Step 2)
3. Re-present after changes
4. DO NOT COMMIT until approved

---

## 📊 Optional Reviews (If Applicable)

### bill-review (For Complex Features >5 pts)

- [ ] **Execute bill-review symbiota** (if feature >5 pts or >200 lines)
  - [ ] bill-review score ≥ 8/10
  - [ ] OR: Address critical issues raised

**IF bill-review < 8/10**: Fix critical issues before commit.

### Coverage Check

- [ ] **Coverage ≥ 80%** for new code
  - [ ] Run: `pytest --cov=forgellmclient.module --cov-fail-under=80`
  - [ ] If <80%, add missing tests

---

## 💾 Ready to Commit

**ALL ITEMS ABOVE MUST BE ✅** before proceeding to Step 4 (Commit).

**Final Confirmation**:

- [ ] ADR-010 passed (technical validation) ✅
- [ ] Stakeholder approved feature ✅
- [ ] Optional reviews completed (if applicable) ✅
- [ ] No blockers or open issues

**→ PROCEED TO STEP 4: CREATE COMMIT**

---

## 📝 Session Review Summary

**Feature ID**: FXX
**Stakeholder**: [Name]
**Review Date**: YYYY-MM-DD
**Duration**: Xmin
**Decision**: ✅ APPROVED / ❌ REJECTED / 🔄 NEEDS CHANGES

**Notes**:
- [Add any important notes, feedback, or decisions made during review]

---

**Template Version**: 1.0
**Created**: 2025-11-06
**Last Updated**: 2025-11-06
**Related**: `process/delivery/sprint/SPRINT_PROCESS.md` (Step 3)
