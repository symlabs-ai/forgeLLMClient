# ForgeLLM

[![Tests](https://img.shields.io/badge/tests-377%20passing-brightgreen)]()
[![Coverage](https://img.shields.io/badge/coverage-80%25-green)]()
[![Python](https://img.shields.io/badge/python-3.11%2B-blue)]()
[![Version](https://img.shields.io/badge/version-0.2.0-blue)]()
[![License](https://img.shields.io/badge/license-MIT-lightgrey)]()

Unified LLM client with provider portability. Write once, run on any provider.

## Features

- **Provider Portability**: Same code works with OpenAI, Anthropic, Ollama, and OpenRouter
- **Async Support**: Non-blocking async/await API for high-throughput applications
- **Tool Calling**: Define custom tools that LLMs can invoke automatically
- **Session Management**: Automatic context window management with compaction strategies
- **Streaming**: Real-time response streaming with tool support
- **Structured Logging**: JSON logging with correlation IDs for observability
- **Type Safety**: Full mypy strict type checking support

## Installation

```bash
# Clone the repository
git clone <repo-url>
cd forge_llm

# Install with Poetry
poetry install

# Or with pip
pip install -e .
```

## Quick Start

### Basic Chat

```python
from forge_llm import ChatAgent

# Create agent with OpenAI
agent = ChatAgent(provider="openai", api_key="sk-...")

# Simple chat
response = agent.chat("Hello, how are you?")
print(response.content)
print(f"Tokens used: {response.token_usage.total_tokens}")
```

### Streaming

```python
from forge_llm import ChatAgent

agent = ChatAgent(provider="anthropic", api_key="sk-ant-...")

for chunk in agent.stream_chat("Tell me a story"):
    print(chunk.content, end="", flush=True)
```

### Async API

```python
import asyncio
from forge_llm.application.agents import AsyncChatAgent
from forge_llm.domain.entities import ProviderConfig

async def main():
    config = ProviderConfig(provider="openai", api_key="sk-...", model="gpt-4o")
    agent = AsyncChatAgent(config)

    # Single async call
    response = await agent.chat("Hello!")

    # Concurrent requests
    tasks = [agent.chat(q) for q in ["Q1?", "Q2?", "Q3?"]]
    responses = await asyncio.gather(*tasks)

asyncio.run(main())
```

### Session Management

```python
from forge_llm import ChatAgent, ChatSession, TruncateCompactor

agent = ChatAgent(provider="openai", api_key="sk-...")

# Session with auto-compaction
session = ChatSession(
    system_prompt="You are a helpful assistant",
    max_tokens=4000,
    compactor=TruncateCompactor(),
)

# Chat maintains context
agent.chat("My name is John", session=session)
response = agent.chat("What's my name?", session=session)
print(response.content)  # "Your name is John"
```

### Tool Calling

```python
from forge_llm import ChatAgent, ToolRegistry

registry = ToolRegistry()

@registry.tool
def get_weather(location: str) -> str:
    """Get weather for a location."""
    return f"Sunny, 25C in {location}"

agent = ChatAgent(provider="openai", api_key="sk-...", tools=registry)

# Tools are automatically called
response = agent.chat("What's the weather in London?")
print(response.content)  # Uses get_weather tool
```

### OpenRouter (Multi-Provider Access)

```python
from forge_llm import ChatAgent

# Access any model through OpenRouter
agent = ChatAgent(
    provider="openrouter",
    api_key="sk-or-...",  # OpenRouter API key
    model="anthropic/claude-3-haiku",  # Or openai/gpt-4, meta-llama/llama-3, etc.
)

response = agent.chat("Hello!")
```

### Local LLMs with Ollama

```python
from forge_llm import ChatAgent

# Use local models via Ollama
agent = ChatAgent(
    provider="ollama",
    model="llama3",
    base_url="http://localhost:11434",
)

response = agent.chat("Write a haiku about coding")
```

### Structured Logging

```python
from forge_llm.infrastructure.logging import LogService, configure_logging

# Configure JSON logging
configure_logging(json_output=True, log_level="INFO")

logger = LogService("my_app")

# Use correlation IDs for request tracing
with LogService.correlation_context() as correlation_id:
    logger.info("Processing request", user_id="123")

    # Time operations
    with LogService.timed("llm_call", provider="openai"):
        response = agent.chat("Hello")
```

## Supported Providers

| Provider | Models | Notes |
|----------|--------|-------|
| OpenAI | gpt-4, gpt-4-turbo, gpt-4o, gpt-4o-mini, gpt-3.5-turbo, o1-preview, o1-mini | Direct API |
| Anthropic | claude-3-opus, claude-3-sonnet, claude-3-haiku, claude-3-5-sonnet | Direct API |
| Ollama | llama3, mistral, codellama, and any Ollama model | Local deployment |
| OpenRouter | 100+ models from OpenAI, Anthropic, Google, Meta, Mistral | Unified API |

## Architecture

ForgeLLM follows Clean/Hexagonal Architecture:

```
src/forge_llm/
├── domain/                 # Business logic, no external dependencies
│   ├── entities/          # ChatMessage, ChatConfig, ToolDefinition, etc.
│   ├── value_objects/     # ChatResponse, TokenUsage, ResponseMetadata
│   └── exceptions.py      # Domain-specific errors
├── application/           # Use cases and orchestration
│   ├── agents/           # ChatAgent, AsyncChatAgent
│   ├── ports/            # Interfaces (ILLMProviderPort, IAsyncLLMProviderPort)
│   ├── session/          # ChatSession, TruncateCompactor, SummarizeCompactor
│   └── tools/            # ToolRegistry
└── infrastructure/        # External integrations
    ├── providers/        # OpenAIAdapter, AnthropicAdapter, OllamaAdapter, etc.
    ├── logging.py        # Structured JSON logging with structlog
    └── resilience.py     # Retry with exponential backoff
```

## Examples

See the `examples/` directory for complete examples:

- `basic_chat.py` - Getting started with basic chat
- `async_chat.py` - Async/await patterns
- `tool_calling.py` - Custom tool definitions
- `openrouter_usage.py` - Multi-provider access
- `session_compaction.py` - Context management strategies
- `structured_logging.py` - Production logging setup

## Development

```bash
# Run tests
pytest tests/ -v

# Run with coverage
pytest --cov=forge_llm --cov-report=html

# Type checking
mypy src/forge_llm --strict

# Linting
ruff check src/ tests/
```

## License

MIT
