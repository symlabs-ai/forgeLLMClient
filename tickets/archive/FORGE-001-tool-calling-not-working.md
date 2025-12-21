# FORGE-001: Tool Calling Not Working in Non-Streaming Mode

**Reporter:** SymRouter Team
**Date:** 2025-12-19
**Priority:** High
**Component:** `forge_llm.infrastructure.providers.openai_adapter.OpenAIAdapter`

---

## Summary

Tool calling (function calling) does not work when using `ChatAgent.chat()` (non-streaming mode). The `tools` parameter is passed to the agent but never forwarded to the OpenAI API.

---

## Environment

- **forge-llm version:** Latest (installed via pip)
- **Python:** 3.12
- **OpenAI model:** gpt-4o-mini
- **OS:** Linux (WSL2)

---

## Steps to Reproduce

```python
from forge_llm import ChatAgent, ToolDefinition, ChatMessage
import os

# 1. Create tool definition
tools = [
    ToolDefinition(
        name='get_weather',
        description='Get the current weather in a given location',
        parameters={
            'type': 'object',
            'properties': {
                'location': {'type': 'string', 'description': 'City name'}
            },
            'required': ['location']
        }
    )
]

# 2. Create agent with tools
agent = ChatAgent(
    provider='openai',
    api_key=os.environ.get('OPENAI_API_KEY'),
    model='gpt-4o-mini',
    tools=tools
)

# 3. Send message that should trigger tool call
messages = [ChatMessage.user('What is the weather in Tokyo?')]
response = agent.chat(messages=messages, auto_execute_tools=False)

# 4. Check response
print(f'Content: {response.message.content}')
print(f'Tool calls: {response.message.tool_calls}')
```

---

## Expected Behavior

The model should return a tool call:
```python
Content: None
Tool calls: [ToolCall(id='call_xxx', function=Function(name='get_weather', arguments='{"location":"Tokyo"}'))]
```

---

## Actual Behavior

The model returns a text response instead of calling the tool:
```python
Content: "I don't have real-time data access to provide current weather..."
Tool calls: None
```

---

## Root Cause Analysis

### 1. Direct OpenAI API Works

When calling OpenAI API directly with the same parameters, tool calling works correctly:

```python
import httpx

response = httpx.post(
    "https://api.openai.com/v1/chat/completions",
    headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    json={
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": "What is the weather in Tokyo?"}],
        "tools": [{
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get the current weather",
                "parameters": {"type": "object", "properties": {"location": {"type": "string"}}, "required": ["location"]}
            }
        }],
        "tool_choice": "auto"
    }
)
# Returns: {"choices": [{"message": {"tool_calls": [...]}, "finish_reason": "tool_calls"}]}
```

### 2. The Bug Location

**File:** `forge_llm/infrastructure/providers/openai_adapter.py`

**Method:** `send()` (lines ~70-95)

```python
def send(
    self,
    messages: list[dict[str, Any]],
    config: dict[str, Any] | None = None,
) -> dict[str, Any]:
    # ...
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        timeout=timeout,
        # BUG: 'tools' is NOT passed here!
    )
```

**Compare with `stream()` method which correctly passes tools:**

```python
def stream(self, messages, config=None):
    # ...
    tools = (config or {}).get("tools")  # Tools extracted from config

    request_params = {
        "model": model,
        "messages": messages,
        "stream": True,
        "timeout": timeout,
    }
    if tools:
        request_params["tools"] = tools  # Tools passed to API

    response = client.chat.completions.create(**request_params)
```

### 3. ChatAgent Does Pass Tools

The `ChatAgent.chat()` method correctly builds the config with tools (line ~192):

```python
config_dict["tools"] = [t.to_openai_format() for t in tool_defs]
```

But `OpenAIAdapter.send()` ignores `config["tools"]`.

---

## Proposed Fix

Update `OpenAIAdapter.send()` to pass tools to the API:

```python
def send(
    self,
    messages: list[dict[str, Any]],
    config: dict[str, Any] | None = None,
) -> dict[str, Any]:
    self.validate()
    client = self._get_client()

    model = (config or {}).get("model") or self._config.model or "gpt-4"
    timeout = (config or {}).get("timeout") or self._config.timeout
    tools = (config or {}).get("tools")  # ADD THIS

    self._logger.debug(
        "Sending request to OpenAI",
        model=model,
        message_count=len(messages),
        has_tools=tools is not None,  # ADD THIS
    )

    # Build request params
    request_params: dict[str, Any] = {
        "model": model,
        "messages": messages,
        "timeout": timeout,
    }
    if tools:
        request_params["tools"] = tools  # ADD THIS

    response = client.chat.completions.create(**request_params)

    choice = response.choices[0]
    usage = response.usage

    # Handle tool_calls in response
    result: dict[str, Any] = {
        "content": choice.message.content,
        "role": choice.message.role,
        "model": response.model,
        "provider": "openai",
        "usage": {
            "prompt_tokens": usage.prompt_tokens if usage else 0,
            "completion_tokens": usage.completion_tokens if usage else 0,
            "total_tokens": usage.total_tokens if usage else 0,
        },
    }

    # ADD: Include tool_calls if present
    if choice.message.tool_calls:
        result["tool_calls"] = [
            {
                "id": tc.id,
                "type": tc.type,
                "function": {
                    "name": tc.function.name,
                    "arguments": tc.function.arguments,
                }
            }
            for tc in choice.message.tool_calls
        ]
        result["finish_reason"] = "tool_calls"

    return result
```

---

## Secondary Issue: Streaming Tool Calls

The `stream()` method passes tools but doesn't properly yield tool_calls data. When testing with streaming and tools enabled:

```
finish_reason: "tool_calls"
tool_calls: (not present in chunks)
```

The tool call data is accumulated internally but not yielded to the caller.

---

## Impact

- **SymRouter:** Cannot provide tool calling functionality to users
- **Workaround:** Use OpenAI SDK directly, bypassing forge-llm for tool calling requests
- **Affected providers:** Likely all providers (OpenAI, Anthropic, etc.) if they follow the same pattern

---

## Suggested Tests

```python
def test_send_with_tools():
    """Tools should be passed to OpenAI API in non-streaming mode."""
    agent = ChatAgent(provider="openai", tools=[...])
    response = agent.chat(messages=[...], auto_execute_tools=False)
    assert response.message.tool_calls is not None

def test_stream_with_tools():
    """Tool calls should be yielded in streaming mode."""
    agent = ChatAgent(provider="openai", tools=[...])
    chunks = list(agent.stream_chat(messages=[...], auto_execute_tools=False))
    # At least one chunk should have tool_calls
    assert any(c.tool_calls for c in chunks)
```

---

## References

- OpenAI Function Calling: https://platform.openai.com/docs/guides/function-calling
- OpenAI API Reference: https://platform.openai.com/docs/api-reference/chat/create#chat-create-tools

---

## Resolution

**Status:** Resolved
**Date:** 2025-12-19
**Fix Version:** 0.4.1

The issue has been resolved by addressing the root causes in both `OpenAIAdapter` and `ChatAgent`.

### Applied Fixes

1.  **OpenAIAdapter (Non-Streaming Fix)**
    *   Updated `send()` method to correctly extract `tools` from the configuration and pass them to the OpenAI API client.
    *   Added logic to parse `tool_calls` from the API response and include them in the return dictionary.

2.  **ChatAgent (Streaming Fix)**
    *   Updated `_stream_with_tools()` to ensure that `tool_calls` data received from the provider is correctly included in the `ChatChunk` yielded to the caller, specifically when `auto_execute_tools=False`. This ensures tool call requests are not swallowed during streaming.

### Verification

*   Created and executed a reproduction script that confirmed both the missing tools in non-streaming mode and the missing tool call chunks in streaming mode.
*   Implemented unit tests `test_send_with_tools` and `test_stream_with_tools` in `tests/unit/test_openai_adapter.py`.
*   Verified that all tests pass successfully.

Gemini - Equipe ForgeLLM
