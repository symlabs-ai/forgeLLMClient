# Pre-Stakeholder Validation Checklist (ADR-010)

**Feature:** [Feature ID and Name, e.g., F02 - Chat Integration]
**Date:** YYYY-MM-DD
**Validator:** [Agent Coder / Developer Name]
**Stakeholder:** [Stakeholder Name]

---

## ⚠️ IMPORTANT: ADR-010 is NOT the final gate

**ADR-010 validates**: Demo works technically (no crashes, tests pass)
**Session Review validates**: Stakeholder approves the feature (meets requirements)

**After ADR-010 passes**:
→ **DO NOT COMMIT YET**
→ **NEXT STEP**: Present to stakeholder (Step 3 of Session Workflow)
→ **ONLY COMMIT**: After stakeholder gives explicit approval

**See**: `process/delivery/sprint/templates/session-review-checklist.md` for full workflow

---

## ⚠️ MANDATORY GATES (ADR-010)

Before presenting this feature to stakeholder, ALL checkboxes must be ✅.

### 1. Demo Execution ✅

- [ ] **Demo script exists**: `examples/sprint[N]/run_demo_[feature].sh`
- [ ] **Demo executed successfully**: No crashes, no errors
- [ ] **Real API credentials used**: Not mocked (if integration feature)
- [ ] **All scenarios completed**: Every demo path tested
- [ ] **Output verified manually**: Matches expected behavior
- [ ] **Known limitations documented**: In demo output or comments

**Demo Command:**
```bash
bash examples/sprint[N]/run_demo_[feature].sh
```

**Execution Notes:**
[Add notes about demo execution results]

---

### 2. BDD Tests ✅

- [ ] **BDD tests exist**: `tests/bdd/test_[feature]_steps.py`
- [ ] **Feature file exists**: `specs/bdd/features/[feature].feature`
- [ ] **All tests pass**: OR explicitly skip with reason
- [ ] **Integration tests run**: With real API (if applicable)
- [ ] **No unexpected failures**: All failures documented

**Test Command:**
```bash
pytest tests/bdd/test_[feature]_steps.py -v
```

**Test Results:**
- Passing: [N] scenarios
- Skipped: [N] scenarios (reasons: [list])
- Failed: [N] scenarios (documented: Y/N)

---

### 3. Code Quality ✅

- [ ] **Python syntax validated**: All files compile
- [ ] **No CRLF issues**: Bash scripts have correct line endings
- [ ] **Imports resolve**: No import errors
- [ ] **No obvious code smells**: Code is clean

**Validation Commands:**
```bash
# Syntax check
python -m py_compile examples/**/*.py src/**/*.py

# Line endings check
file examples/**/*.sh

# Import check
python -c "import forgellmclient; ..."
```

**Quality Notes:**
[Add notes about code quality checks]

---

### 4. Documentation ✅

- [ ] **BDD scenarios complete**: `.feature` file describes all behaviors
- [ ] **Demo has success criteria**: Clear expected outcomes
- [ ] **Known limitations listed**: Documented in demo or README
- [ ] **Commit message clear**: Describes feature accurately

**Documentation Notes:**
[Add notes about documentation completeness]

---

## 🎯 Validation Result

**Overall Status:** ✅ PASS / ❌ FAIL

**If FAIL:**
- [ ] Issues identified and listed below
- [ ] Fix plan created
- [ ] Re-validation scheduled

**Issues Found:**
1. [Issue description]
2. [Issue description]

---

## 📝 Additional Notes

**Observations:**
[Any observations during validation]

**Blockers:**
[Any blockers that prevented full validation]

**Recommendations:**
[Any recommendations for stakeholder demo]

---

## ✅ Sign-Off

**Validated By:** [Name/Agent ID]
**Validation Date:** YYYY-MM-DD HH:MM
**Stakeholder Demo Scheduled:** YYYY-MM-DD HH:MM

**Declaration:**
- [ ] I confirm all mandatory gates are ✅
- [ ] I confirm demo is ready for stakeholder presentation
- [ ] I confirm known issues are documented

---

## 🚨 Exception Handling

**If stakeholder requests WIP/early preview:**

- [ ] Stakeholder explicitly requested WIP demo
- [ ] Feature clearly labeled as **WORK IN PROGRESS**
- [ ] Known issues listed prominently
- [ ] Expected completion date communicated

**Exception Approved By:** [Stakeholder Name]
**Exception Date:** YYYY-MM-DD

---

**Template Version:** 1.0
**Created:** 2025-11-06 (ADR-010)
**Last Updated:** 2025-11-06
**Reference:** `process/delivery/review/etapa_stakeholder_validation.md`
