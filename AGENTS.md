# ForgeLLMClient - Agent Discovery Guide

> **SDK Python leve para interface unificada com LLMs.**
> Fornece uma API estável e consistente para qualquer provedor de LLM.

---

## Quick Discovery Index

```yaml
project:
  name: ForgeLLMClient
  type: sdk
  language: python
  version: "0.1.0"
  architecture: hexagonal

capabilities:
  - chat_completion
  - streaming
  - tool_calling
  - vision
  - multi_provider
  - conversation_memory
  - auto_fallback
  - mcp_integration

providers:
  - openai
  - anthropic
  - openrouter

entry_points:
  sdk: "from forge_llm import Client"
  cli: "forge-llm chat"
```

---

## SDK Capability Matrix

| Capability | OpenAI | Anthropic | OpenRouter | Description |
|------------|--------|-----------|------------|-------------|
| Chat | yes | yes | yes | Basic chat completion |
| Streaming | yes | yes | yes | Real-time response streaming |
| Tool Calling | yes | yes | yes | Function/tool execution |
| Vision | yes | yes | partial | Image understanding |
| JSON Mode | yes | yes | yes | Structured output |
| Auto-Fallback | yes | yes | yes | Provider failover |

---

## Core API Reference

### Client (Entry Point)

```python
from forge_llm import Client

# Initialize
client = Client(provider="openai", api_key="sk-...")

# Chat
response = await client.chat("Hello!")
print(response.content)

# Streaming
async for chunk in client.chat_stream("Hello!"):
    print(chunk["content"], end="")

# Tools
response = await client.chat("Weather?", tools=[weather_tool])
if response.has_tool_calls:
    for call in response.tool_calls:
        print(f"{call.name}: {call.arguments}")
```

### Response Types

```python
# ChatResponse
response.content      # str - Response text
response.model        # str - Model used
response.provider     # str - Provider name
response.usage        # TokenUsage - Token counts
response.tool_calls   # list[ToolCall] - Tool calls
response.finish_reason # str - stop/tool_calls/length

# TokenUsage
usage.prompt_tokens     # int
usage.completion_tokens # int
usage.total_tokens      # int

# ToolCall
call.id         # str - Unique ID
call.name       # str - Function name
call.arguments  # dict - Arguments
```

### Conversation Management

```python
from forge_llm import Client

client = Client(provider="openai", api_key="...")
conv = client.create_conversation(system="You are helpful")

# Multi-turn chat
r1 = await conv.chat("Hello!")
r2 = await conv.chat("What did I just say?")  # Has context

# Provider hot-swap
conv.change_provider("anthropic", api_key="...")
r3 = await conv.chat("Continue")  # Same history, new provider
```

---

## File Discovery Map

### Source Code Structure

```
src/forge_llm/
├── __init__.py          # Public API (98 exports)
├── client.py            # Client facade
├── cli.py               # CLI interface
│
├── domain/
│   ├── entities.py      # ChatResponse, Conversation, ToolCall
│   ├── value_objects.py # Message, TokenUsage, ImageContent
│   └── exceptions.py    # Exception hierarchy
│
├── application/
│   └── ports/
│       ├── provider_port.py           # ProviderPort interface
│       └── conversation_client_port.py # DIP interface
│
├── providers/
│   ├── registry.py              # Provider factory
│   ├── openai_provider.py       # OpenAI adapter
│   ├── anthropic_provider.py    # Anthropic adapter
│   ├── openrouter_provider.py   # OpenRouter adapter
│   └── auto_fallback_provider.py # Fallback strategy
│
├── infrastructure/
│   ├── cache.py         # InMemoryCache, NoOpCache
│   ├── rate_limiter.py  # TokenBucketRateLimiter
│   └── retry.py         # Exponential backoff
│
├── observability/
│   ├── manager.py       # ObservabilityManager
│   ├── events.py        # Event types
│   └── observers.py     # Logging, Metrics observers
│
├── persistence/
│   ├── store.py         # ConversationStore interface
│   └── json_store.py    # JSON persistence
│
├── mcp/
│   ├── client.py        # MCP client
│   └── adapter.py       # Tool adapter
│
└── utils/
    ├── token_counter.py     # Token counting
    ├── response_validator.py # Validation
    └── summarizer.py        # Conversation summary
```

### Documentation Structure

```
docs/
├── getting-started/
│   ├── installation.md    # Setup guide
│   └── quickstart.md      # First steps
│
├── guides/
│   ├── client-usage.md        # SDK usage (14KB)
│   ├── domain-model.md        # DDD model (14KB)
│   ├── error-handling.md      # Exceptions (13KB)
│   ├── creating-providers.md  # Provider guide (13KB)
│   ├── auto-fallback.md       # Fallback (11KB)
│   ├── observability.md       # Monitoring (13KB)
│   └── mcp-integration.md     # MCP (12KB)
│
├── advanced/
│   └── architecture.md    # Hexagonal architecture + diagrams
│
└── api/
    └── *.md               # Auto-generated API docs
```

### Test Structure

```
tests/
├── unit/
│   ├── domain/           # Entity/VO tests
│   ├── providers/        # Provider tests
│   └── infrastructure/   # Cache/retry tests
│
├── integration/
│   └── test_*.py         # Integration tests
│
└── bdd/
    └── test_*_steps.py   # BDD step definitions

specs/bdd/
└── *.feature             # Gherkin specifications
```

---

## Exception Hierarchy

```
ForgeError (base)
├── ValidationError       # Invalid input
├── ConfigurationError    # Missing config
└── ProviderError (retryable base)
    ├── AuthenticationError   # 401/403
    ├── RateLimitError        # 429 (retryable)
    ├── APIError              # 4xx/5xx
    ├── APITimeoutError       # Timeout (retryable)
    └── RetryExhaustedError   # Max retries reached
```

---

## Agent Integration Patterns

### Pattern 1: Simple Agent

```python
from forge_llm import Client

class SimpleAgent:
    def __init__(self, provider: str = "openai"):
        self.client = Client(provider=provider, api_key="...")

    async def run(self, prompt: str) -> str:
        response = await self.client.chat(prompt)
        return response.content
```

### Pattern 2: Tool-Using Agent

```python
from forge_llm import Client, ToolDefinition

class ToolAgent:
    def __init__(self):
        self.client = Client(provider="openai", api_key="...")
        self.tools = [
            ToolDefinition(
                name="search",
                description="Search the web",
                parameters={"query": {"type": "string"}}
            )
        ]

    async def run(self, prompt: str) -> str:
        response = await self.client.chat(prompt, tools=self.tools)

        while response.has_tool_calls:
            results = await self._execute_tools(response.tool_calls)
            response = await self.client.chat(results)

        return response.content
```

### Pattern 3: Multi-Provider Agent

```python
from forge_llm import Client

class ResilientAgent:
    def __init__(self):
        self.client = Client(
            provider="auto",  # Auto-fallback
            providers=[
                {"provider": "openai", "api_key": "..."},
                {"provider": "anthropic", "api_key": "..."},
            ]
        )

    async def run(self, prompt: str) -> str:
        # Automatically falls back if first provider fails
        response = await self.client.chat(prompt)
        return response.content
```

### Pattern 4: Conversation Agent

```python
from forge_llm import Client

class ConversationAgent:
    def __init__(self, system: str):
        self.client = Client(provider="openai", api_key="...")
        self.conv = self.client.create_conversation(
            system=system,
            max_messages=20  # Window limit
        )

    async def chat(self, message: str) -> str:
        response = await self.conv.chat(message)
        return response.content

    def reset(self):
        self.conv.clear()
```

---

## MCP Integration

```python
from forge_llm import Client, MCPClient, MCPServerConfig

# Configure MCP server
mcp = MCPClient()
await mcp.connect(MCPServerConfig(
    name="filesystem",
    command="npx",
    args=["-y", "@modelcontextprotocol/server-filesystem", "/tmp"]
))

# Get tools from MCP
tools = await mcp.list_tools()

# Use with client
client = Client(provider="openai", api_key="...")
response = await client.chat("List files", tools=tools)
```

---

## Development Commands

```bash
# Install
pip install -e ".[dev]"

# Test
pytest tests/ -v

# Type check
mypy src/forge_llm

# Lint
ruff check src/

# Coverage
pytest --cov=src/forge_llm --cov-report=html

# Docs
mkdocs serve

# CLI
forge-llm chat "Hello!"
forge-llm providers
forge-llm models openai
```

---

## Architecture Principles

1. **Hexagonal Architecture**: Domain isolated from infrastructure
2. **Dependency Inversion**: Depend on abstractions (Ports), not implementations
3. **Single Responsibility**: Each class has one job
4. **Open/Closed**: Extend via new adapters, don't modify core

---

## Quick Reference Links

| Topic | File |
|-------|------|
| **SDK Usage** | `docs/guides/client-usage.md` |
| **Domain Model** | `docs/guides/domain-model.md` |
| **Error Handling** | `docs/guides/error-handling.md` |
| **Creating Providers** | `docs/guides/creating-providers.md` |
| **Architecture** | `docs/advanced/architecture.md` |
| **API Reference** | `docs/api/*.md` |

---

## Symbiota/Agent Rules

### Defaults

- **Clean/Hex**: Domain is pure; adapters only via ports
- **CLI-first**: Validate via CLI before TUI/HTTP
- **Offline-first**: No external network by default
- **Persistence**: Sessions/states in YAML; auto-commit Git

### Code Agents (TDD)

1. Read BDD specs in `specs/bdd/`
2. Implement steps in `tests/bdd/`
3. Write code in `src/` following layers
4. Use specific exceptions from hierarchy
5. Add observability via `ObservabilityManager`

### Handoff Protocol

When completing a task, document in:
- `project/docs/sessions/` for session logs
- Commit message with clear description
- Update AGENTS.md if API changes

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 0.1.0 | 2024-12 | Initial release with OpenAI, Anthropic, OpenRouter |
