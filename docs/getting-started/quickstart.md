# Quick Start

Este guia mostra como comecar a usar o ForgeLLM em 5 minutos.

## TL;DR

```python
import asyncio
from forge_llm import Client

async def main():
    client = Client(provider="openai", api_key="sk-...")
    response = await client.chat("Hello!")
    print(response.content)

asyncio.run(main())
```

## Primeiro Chat

```python
import asyncio
import os
from forge_llm import Client

async def main():
    # Crie um cliente (usa OPENAI_API_KEY do ambiente)
    client = Client(
        provider="openai",
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    # Envie uma mensagem
    response = await client.chat("What is the capital of France?")

    # Acesse a resposta
    print(f"Content: {response.content}")
    print(f"Model: {response.model}")
    print(f"Tokens: {response.usage.total_tokens}")

asyncio.run(main())
```

## Usando o CLI

```bash
# Chat simples
forge-llm chat "What is Python?"

# Com provider especifico
forge-llm chat "Hello!" --provider anthropic

# Com modelo especifico
forge-llm chat "Hello!" --provider openai --model gpt-4o

# Listar providers
forge-llm providers

# Listar modelos de um provider
forge-llm models openai
```

## Providers Suportados

### OpenAI

```python
client = Client(
    provider="openai",
    api_key="sk-...",
    model="gpt-4o-mini",  # opcional, default: gpt-4o-mini
)
```

Modelos: `gpt-4o`, `gpt-4o-mini`, `gpt-4-turbo`, `gpt-3.5-turbo`

### Anthropic

```python
client = Client(
    provider="anthropic",
    api_key="sk-ant-...",
    model="claude-3-5-haiku-latest",  # opcional
)
```

Modelos: `claude-3-5-sonnet-latest`, `claude-3-5-haiku-latest`, `claude-3-opus-latest`

### OpenRouter

```python
client = Client(
    provider="openrouter",
    api_key="sk-or-...",
    model="meta-llama/llama-3.1-8b-instruct:free",
)
```

Acesso a 100+ modelos via API unificada.

## Streaming

Receba respostas em tempo real:

```python
async def stream_example():
    client = Client(provider="openai", api_key="...")

    async for chunk in client.chat_stream("Tell me a story"):
        content = chunk.get("content", "")
        if content:
            print(content, end="", flush=True)
    print()  # Nova linha no final
```

## Conversas Multi-turno

Mantenha contexto entre mensagens:

```python
async def conversation_example():
    client = Client(provider="openai", api_key="...")

    # Crie uma conversa com system prompt
    conv = client.create_conversation(
        system="You are a helpful Python tutor."
    )

    # Primeira mensagem
    r1 = await conv.chat("What is a list?")
    print(f"Assistant: {r1.content}")

    # Segunda mensagem (tem contexto da primeira)
    r2 = await conv.chat("How do I add items to it?")
    print(f"Assistant: {r2.content}")

    # Terceira mensagem
    r3 = await conv.chat("Show me an example")
    print(f"Assistant: {r3.content}")
```

## Tool Calling (Function Calling)

Permita que o LLM chame funcoes:

```python
async def tool_example():
    client = Client(provider="openai", api_key="...")

    # Defina uma tool
    tools = [{
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get weather for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string"}
                },
                "required": ["city"]
            }
        }
    }]

    # Chat com tools
    response = await client.chat(
        "What's the weather in Paris?",
        tools=tools
    )

    # Verifique se ha tool calls
    if response.has_tool_calls:
        for call in response.tool_calls:
            print(f"Tool: {call.name}")
            print(f"Args: {call.arguments}")
```

## JSON Mode

Forcce respostas em JSON:

```python
from forge_llm import Client, ResponseFormat

async def json_example():
    client = Client(provider="openai", api_key="...")

    response = await client.chat(
        "List 3 programming languages with their year of creation",
        response_format=ResponseFormat(type="json_object")
    )

    import json
    data = json.loads(response.content)
    print(data)
```

## Retry Automatico

Configure retry para erros transientes:

```python
client = Client(
    provider="openai",
    api_key="...",
    max_retries=3,      # Numero de tentativas
    retry_delay=1.0,    # Delay base em segundos
)

# Automaticamente faz retry em:
# - RateLimitError (429)
# - APITimeoutError
# - Erros de servidor (500, 502, 503)
```

## Tratamento de Erros

```python
from forge_llm import (
    Client,
    ForgeError,
    AuthenticationError,
    RateLimitError,
    ValidationError,
)

async def error_handling():
    try:
        client = Client(provider="openai", api_key="...")
        response = await client.chat("Hello!")
    except AuthenticationError:
        print("API key invalida")
    except RateLimitError:
        print("Rate limit atingido, tente novamente")
    except ValidationError as e:
        print(f"Input invalido: {e}")
    except ForgeError as e:
        print(f"Erro geral: {e}")
```

## Exemplo Completo

```python
import asyncio
import os
from forge_llm import Client, AuthenticationError

async def main():
    # Configuracao
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Configure OPENAI_API_KEY")
        return

    # Cliente com retry
    client = Client(
        provider="openai",
        api_key=api_key,
        model="gpt-4o-mini",
        max_retries=3,
    )

    try:
        # Conversa
        conv = client.create_conversation(
            system="You are a helpful assistant."
        )

        # Chat interativo
        while True:
            user_input = input("You: ").strip()
            if user_input.lower() in ["quit", "exit"]:
                break

            response = await conv.chat(user_input)
            print(f"Assistant: {response.content}\n")

    except AuthenticationError:
        print("API key invalida")
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())
```

## Proximos Passos

| Topico | Descricao |
|--------|-----------|
| [Tool Calling](../guides/tool-calling.md) | Use ferramentas/funcoes |
| [JSON Mode](../guides/json-mode.md) | Respostas estruturadas |
| [Streaming](../guides/streaming.md) | Respostas em tempo real |
| [Error Handling](../guides/error-handling.md) | Tratamento de erros |
| [Observability](../guides/observability.md) | Logging e metricas |
| [MCP Integration](../guides/mcp-integration.md) | Model Context Protocol |
| [Architecture](../advanced/architecture.md) | Arquitetura hexagonal |
