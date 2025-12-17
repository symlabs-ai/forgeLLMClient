#!/bin/bash
# E2E Tests Runner - Cycle 02 (Sprint 2 Features)
# Run all E2E tests for Sprint 2 deliverables

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
EVIDENCE_DIR="$SCRIPT_DIR/evidence"

echo "=========================================="
echo "E2E Tests - Cycle 02 (Sprint 2 Features)"
echo "=========================================="
echo ""

# Create evidence directory if not exists
mkdir -p "$EVIDENCE_DIR"

# Timestamp for evidence files
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

cd "$PROJECT_ROOT"

# Activate virtual environment if exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

echo "Running E2E tests..."
echo ""

# Run pytest with verbose output and save to evidence
pytest tests/e2e/cycle-02/test_sprint2_features.py \
    -v \
    --tb=short \
    2>&1 | tee "$EVIDENCE_DIR/test_run_$TIMESTAMP.log"

EXIT_CODE=${PIPESTATUS[0]}

echo ""
echo "=========================================="

if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ All E2E tests passed!"
    echo "Evidence saved to: $EVIDENCE_DIR/test_run_$TIMESTAMP.log"
else
    echo "❌ Some E2E tests failed!"
    echo "Check evidence: $EVIDENCE_DIR/test_run_$TIMESTAMP.log"
fi

echo "=========================================="

exit $EXIT_CODE
