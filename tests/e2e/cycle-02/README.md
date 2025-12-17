# E2E Tests - Cycle 02 (Sprint 2 Features)

End-to-end tests validating Sprint 2 deliverables.

## Features Tested

1. **Ollama Provider** - Local LLM integration
2. **Streaming with Tools** - Tool execution during streaming
3. **SummarizeCompactor** - LLM-based context compaction
4. **Async API** - Concurrent chat operations
5. **OpenRouter Provider** - Multi-provider unified access
6. **Structured Logging** - JSON logging with correlation IDs

## Running Tests

```bash
# Run all cycle-02 E2E tests
./tests/e2e/cycle-02/run-all.sh

# Run specific test file
pytest tests/e2e/cycle-02/test_sprint2_features.py -v
```

## Prerequisites

- API keys configured in .env:
  - OPENAI_API_KEY
  - ANTHROPIC_API_KEY
  - OPENROUTER_API_KEY (optional)
- Ollama running locally (optional, for Ollama tests)

## Evidence

Test execution evidence is stored in `evidence/` directory.
