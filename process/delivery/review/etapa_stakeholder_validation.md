# Pre-Stakeholder Validation Checklist

**Purpose:** Ensure features are fully functional BEFORE presenting to stakeholder.

**When to Use:** Before ANY stakeholder demo/validation request.

---

## ⚠️ **MANDATORY GATES**

Before presenting ANY feature to stakeholder, ALL of the following must be ✅:

### 1. Demo Execution
- [ ] Demo script executed successfully (no errors)
- [ ] Demo script tested with REAL API credentials (not mocked)
- [ ] All demo scenarios completed without crashes
- [ ] Output matches expected behavior

### 2. BDD Tests
- [ ] BDD tests executed (with real API if integration tests)
- [ ] All tests pass OR explicitly skip with clear reason
- [ ] No unexpected failures

### 3. Code Quality
- [ ] Python syntax verified (`python -m py_compile`)
- [ ] No CRLF issues in bash scripts (`file *.sh` shows no CRLF)
- [ ] All imports resolve correctly
- [ ] No obvious code smells

### 4. Documentation
- [ ] Feature documented in BDD scenarios
- [ ] Demo has clear success criteria
- [ ] Known limitations documented in demo output

---

## 🔴 **FAILURE CASE: F11_MVP + F12A_MVP (2025-11-06)**

**What Went Wrong:**
- Implemented F11_MVP (Streaming) and F12A_MVP (Tool Calling)
- Created demos but did NOT execute them
- Committed code
- Presented to stakeholder
- Stakeholder found bugs immediately

**Bugs Found:**
1. **F11_MVP:** Streaming delta extraction incorrect (`event.delta.text` vs `event.delta`)
2. **F12A_MVP:** Tool schema format wrong (nested vs flat)
3. **F12A_MVP:** Tool result format wrong (text vs function_call_output)
4. **F12A_MVP:** Tool call extraction wrong (tool_calls vs output[0])

**Why It Happened:**
- No mandatory demo execution step in process
- Relied on theoretical implementation without validation
- Responses API is new (2025), formats differ from chat.completions
- No quality gate before stakeholder presentation

**Corrective Actions:**
1. ✅ Created this checklist document
2. ⏳ Update ForgeProcess to reference this checklist
3. ⏳ Add "Demo Validation" step to BDD workflow
4. ⏳ Create ADR documenting this failure and prevention

**Lessons Learned:**
- **ALWAYS execute demos before stakeholder presentation**
- **NEVER assume implementation works without real API validation**
- **Research API formats FIRST, especially for new APIs**
- **Stakeholder time is precious - don't waste it debugging**

---

## 📋 **Pre-Stakeholder Checklist Template**

Copy this checklist when preparing stakeholder demo:

```markdown
## Pre-Stakeholder Validation: [Feature Name]

**Date:** YYYY-MM-DD
**Feature:** [e.g., F11_MVP - Streaming]
**Stakeholder:** [Name]

### Execution Validation
- [ ] Demo script runs without errors: `bash examples/sprint1/run_demo_X.sh`
- [ ] All scenarios complete successfully
- [ ] Output verified manually
- [ ] Known limitations documented in demo output

### Test Validation
- [ ] BDD tests pass: `pytest tests/bdd/test_X_steps.py -v`
- [ ] Integration tests run with real API (if applicable)
- [ ] Coverage meets threshold (if applicable)

### Code Quality
- [ ] Syntax check: `python -m py_compile examples/sprint1/demo_X.py`
- [ ] Line endings: `file examples/sprint1/*.sh` (no CRLF)
- [ ] Imports resolve: `python -c "import forgellmclient; ..."`

### Readiness
- [ ] Commit message describes feature accurately
- [ ] Demo has clear acceptance criteria
- [ ] Known issues/limitations listed

**Validation Result:** ✅ PASS / ❌ FAIL

**Notes:** [Any observations, issues found during validation]

**Validated By:** [AI Agent / Human Developer]
**Date/Time:** YYYY-MM-DD HH:MM
```

---

## 🚨 **If Validation Fails**

**DO NOT present to stakeholder until:**
1. All bugs fixed
2. Demo executes successfully
3. Tests pass
4. Checklist complete

**Exception:** If stakeholder explicitly requests "WIP demo" or "early preview", clearly label as **WORK IN PROGRESS** with known issues listed.

---

## 📚 **References**

- ForgeProcess: `process/PROCESS.md`
- BDD Process: `process/bdd/BDD_PROCESS.md`
- Review Process: `process/delivery/review/REVIEW_PROCESS.md`
- Stakeholder Priority Changes: `process/delivery/sprint/stakeholder_priority_changes.md`
- ADR-010: `specs/adr/ADR-010-pre-stakeholder-validation-mandate.md`

---

**Created:** 2025-11-06
**Last Updated:** 2025-11-06
**Status:** Active
**Owner:** ForgeProcess Team
