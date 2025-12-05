# ForgeLLMClient

SDK Python para interface unificada com multiplos provedores de LLM.

## Caracteristicas

- **Interface unificada** para OpenAI, Anthropic, Google Gemini, AWS Bedrock, Ollama, LiteLLM, OpenRouter
- **Tool calling** padronizado entre providers
- **Streaming** com async iterators
- **Retry automatico** com exponential backoff
- **Auto-fallback** entre providers para alta disponibilidade
- **Integracao MCP** para tools externas
- **Observabilidade** com logging, metricas e callbacks
- **Type hints** completos e validacao em runtime

## Instalacao

```bash
pip install forge-llm
```

## Quick Start

```python
import asyncio
from forge_llm import Client

async def main():
    # Criar client
    client = Client(provider="openai", api_key="sk-...")

    # Chat simples
    response = await client.chat("Ola! Como voce esta?")
    print(response.content)

    # Ver tokens usados
    print(f"Tokens: {response.usage.total_tokens}")

asyncio.run(main())
```

## Providers Suportados

| Provider | Nome | API Key |
|----------|------|---------|
| OpenAI | `openai` | `OPENAI_API_KEY` |
| Anthropic | `anthropic` | `ANTHROPIC_API_KEY` |
| Google Gemini | `gemini` | `GEMINI_API_KEY` |
| AWS Bedrock | `bedrock` | AWS credentials |
| Ollama | `ollama` | - (local) |
| LiteLLM | `litellm` | Varia |
| OpenRouter | `openrouter` | `OPENROUTER_API_KEY` |

```python
# OpenAI
client = Client(provider="openai", api_key="sk-...")

# Anthropic
client = Client(provider="anthropic", api_key="sk-ant-...")

# OpenRouter
client = Client(provider="openrouter", api_key="sk-or-...")

# Ollama (local)
client = Client(provider="ollama", model="llama2")
```

## Exemplos

### Conversas

```python
# Conversa com historico persistente
conv = client.create_conversation(
    system="Voce e um assistente prestativo",
    max_messages=20
)

r1 = await conv.chat("Qual a capital do Brasil?")
r2 = await conv.chat("E quantos habitantes tem?")  # Mantem contexto
```

### Streaming

```python
async for chunk in client.chat_stream("Conte uma historia"):
    if chunk["delta"]["content"]:
        print(chunk["delta"]["content"], end="")
```

### Tool Calling

```python
tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Obter clima de uma cidade",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string"}
            },
            "required": ["city"]
        }
    }
}]

response = await client.chat("Qual o clima em SP?", tools=tools)

if response.has_tool_calls:
    for tc in response.tool_calls:
        print(f"Chamar: {tc.name}({tc.arguments})")
```

### Auto-Fallback

```python
from forge_llm.providers.auto_fallback_provider import AutoFallbackProvider

# Se OpenAI falhar (rate limit), tenta Anthropic
provider = AutoFallbackProvider(
    providers=["openai", "anthropic"],
    api_keys={"openai": "sk-...", "anthropic": "sk-ant-..."},
)

client = Client(provider=provider)
response = await client.chat("Ola!")
print(f"Respondido por: {provider.last_provider_used}")
```

### Observabilidade

```python
from forge_llm import Client, ObservabilityManager, LoggingObserver

obs = ObservabilityManager()
obs.add_observer(LoggingObserver())

client = Client(
    provider="openai",
    api_key="sk-...",
    observability=obs
)

# Todas as chamadas sao logadas automaticamente
response = await client.chat("Ola!")
```

### Integracao MCP

```python
from forge_llm import MCPClient, MCPServerConfig

mcp = MCPClient()
await mcp.connect(MCPServerConfig(
    name="filesystem",
    command="npx",
    args=["-y", "@modelcontextprotocol/server-filesystem", "/tmp"],
))

tools = mcp.get_tool_definitions()
response = await client.chat("Liste arquivos", tools=tools)
```

## Documentacao

- [Guia de Uso do Client](docs/guides/client-usage.md)
- [Modelo de Dominio](docs/guides/domain-model.md)
- [Tratamento de Erros](docs/guides/error-handling.md)
- [Criando Providers](docs/guides/creating-providers.md)
- [Observabilidade](docs/guides/observability.md)
- [Integracao MCP](docs/guides/mcp-integration.md)
- [Auto-Fallback](docs/guides/auto-fallback.md)

## Desenvolvimento

```bash
# Clone
git clone https://github.com/seu-usuario/forgellmclient.git
cd forgellmclient

# Instalar dependencias
pip install -e ".[dev]"

# Rodar testes
pytest

# Lint e type check
ruff check src/
mypy src/
```

## Licenca

MIT

## Versao

0.1.0
