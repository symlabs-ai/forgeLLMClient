# Guia: Usando o ForgeLLMClient

Este guia explica como usar o ForgeLLMClient para interagir com diferentes provedores de LLM.

---

## 1. Instalacao

```bash
pip install forge-llm
```

Ou para desenvolvimento:

```bash
pip install -e ".[dev]"
```

---

## 2. Uso Basico

### 2.1 Chat Simples

```python
import asyncio
from forge_llm import Client

async def main():
    # Criar cliente com provider
    client = Client(provider="openai", api_key="sk-...")

    # Enviar mensagem simples
    response = await client.chat("Ola! Como voce esta?")

    print(response.content)
    print(f"Tokens usados: {response.usage.total_tokens}")

asyncio.run(main())
```

### 2.2 Providers Disponiveis

| Provider | Nome | Requer API Key |
|----------|------|----------------|
| OpenAI | `openai` | `OPENAI_API_KEY` |
| Anthropic | `anthropic` | `ANTHROPIC_API_KEY` |
| Google Gemini | `gemini` | `GEMINI_API_KEY` |
| AWS Bedrock | `bedrock` | AWS credentials |
| Ollama | `ollama` | Nao (local) |
| LiteLLM | `litellm` | Varia |
| OpenRouter | `openrouter` | `OPENROUTER_API_KEY` |

### 2.3 Configurando Modelo

```python
# Modelo especifico na inicializacao
client = Client(
    provider="openai",
    api_key="sk-...",
    model="gpt-4o"
)

# Ou por chamada
response = await client.chat("Ola!", model="gpt-4o-mini")
```

---

## 3. Mensagens Estruturadas

### 3.1 Usando Message Objects

```python
from forge_llm.domain.value_objects import Message

# System prompt + user message
messages = [
    Message(role="system", content="Voce e um assistente prestativo"),
    Message(role="user", content="Qual a capital do Brasil?"),
]

response = await client.chat(messages)
```

### 3.2 Conversas Multi-turn

```python
# Simular conversa com historico
messages = [
    Message(role="system", content="Voce e um professor de matematica"),
    Message(role="user", content="Quanto e 2+2?"),
    Message(role="assistant", content="2+2 = 4"),
    Message(role="user", content="E 4+4?"),
]

response = await client.chat(messages)
# "4+4 = 8"
```

### 3.3 Usando Conversation Helper

```python
# Criar conversa com contexto persistente
conv = client.create_conversation(
    system="Voce e um assistente de culinaria",
    max_messages=10  # Limite de historico
)

# Primeira mensagem
r1 = await conv.chat("Como fazer arroz?")
print(r1.content)

# Segunda mensagem (mantem contexto)
r2 = await conv.chat("E se eu quiser para 4 pessoas?")
print(r2.content)

# Limpar historico
conv.clear()
```

---

## 4. Streaming

### 4.1 Streaming Basico

```python
async for chunk in client.chat_stream("Conte uma historia"):
    content = chunk["delta"]["content"]
    if content:
        print(content, end="", flush=True)
```

### 4.2 Streaming com Progresso

```python
full_response = ""

async for chunk in client.chat_stream("Explique fotossintese"):
    content = chunk["delta"]["content"]
    if content:
        full_response += content
        print(content, end="", flush=True)

    # Verificar fim
    if chunk.get("finish_reason") == "stop":
        print("\n--- Fim ---")

print(f"Total: {len(full_response)} caracteres")
```

---

## 5. Tool Calling (Function Calling)

### 5.1 Definindo Tools

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Obter clima atual de uma cidade",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "Nome da cidade"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "Unidade de temperatura"
                    }
                },
                "required": ["city"]
            }
        }
    }
]

response = await client.chat(
    "Qual o clima em Sao Paulo?",
    tools=tools
)
```

### 5.2 Processando Tool Calls

```python
if response.has_tool_calls:
    for tool_call in response.tool_calls:
        print(f"Tool: {tool_call.name}")
        print(f"Args: {tool_call.arguments}")

        # Executar a funcao
        if tool_call.name == "get_weather":
            result = get_weather(**tool_call.arguments)

            # Enviar resultado de volta
            messages = [
                Message(role="user", content="Qual o clima em SP?"),
                Message(role="assistant", content="", tool_calls=[tool_call]),
                Message(
                    role="tool",
                    content=str(result),
                    tool_call_id=tool_call.id
                ),
            ]

            final_response = await client.chat(messages)
```

---

## 6. Imagens (Vision)

### 6.1 Imagem por URL

```python
from forge_llm.domain.value_objects import Message, ImageContent

# Criar mensagem com imagem
messages = [
    Message(
        role="user",
        content=[
            "O que voce ve nesta imagem?",
            ImageContent(url="https://example.com/imagem.jpg")
        ]
    )
]

response = await client.chat(messages)
```

### 6.2 Imagem em Base64

```python
import base64

# Ler imagem local
with open("foto.jpg", "rb") as f:
    image_data = base64.b64encode(f.read()).decode()

messages = [
    Message(
        role="user",
        content=[
            "Descreva esta foto",
            ImageContent(
                base64_data=image_data,
                media_type="image/jpeg"
            )
        ]
    )
]

response = await client.chat(messages)
```

---

## 7. Retry Automatico

### 7.1 Configuracao Simples

```python
# Retry com exponential backoff
client = Client(
    provider="openai",
    api_key="sk-...",
    max_retries=3,
    retry_delay=1.0  # segundos
)

# Automaticamente faz retry em erros transientes
response = await client.chat("Ola!")
```

### 7.2 Configuracao Avancada

```python
from forge_llm.infrastructure.retry import RetryConfig

config = RetryConfig(
    max_retries=5,
    base_delay=1.0,
    max_delay=30.0,
    exponential_base=2.0
)

client = Client(
    provider="openai",
    api_key="sk-...",
    retry_config=config
)
```

---

## 8. Trocando de Provider

### 8.1 Reconfiguracao

```python
client = Client()

# Usar OpenAI
client.configure(provider="openai", api_key="sk-...")
r1 = await client.chat("Ola OpenAI!")

# Trocar para Anthropic
client.configure(provider="anthropic", api_key="sk-ant-...")
r2 = await client.chat("Ola Claude!")
```

### 8.2 Provider Customizado

```python
from forge_llm.providers.openai_provider import OpenAIProvider

# Criar provider manualmente
provider = OpenAIProvider(
    api_key="sk-...",
    model="gpt-4o",
    base_url="https://custom-endpoint.com/v1"
)

client = Client(provider=provider)
```

---

## 9. Parametros de Geracao

### 9.1 Temperature

```python
# Mais criativo (alta temperature)
response = await client.chat(
    "Escreva um poema",
    temperature=0.9
)

# Mais deterministico (baixa temperature)
response = await client.chat(
    "Qual e 2+2?",
    temperature=0.0
)
```

### 9.2 Max Tokens

```python
# Limitar tamanho da resposta
response = await client.chat(
    "Resuma este texto...",
    max_tokens=100
)

print(f"Tokens usados: {response.usage.completion_tokens}")
```

---

## 10. Boas Praticas

### 10.1 Gerenciar Contexto

```python
# Usar async context manager para cleanup
async def main():
    client = Client(provider="openai", api_key="sk-...")
    try:
        response = await client.chat("Ola!")
    finally:
        await client.close()
```

### 10.2 Verificar Configuracao

```python
client = Client()

if not client.is_configured:
    client.configure(provider="openai", api_key="sk-...")

print(f"Provider: {client.provider_name}")
print(f"Model: {client.model}")
```

### 10.3 Tratar Erros

```python
from forge_llm.domain.exceptions import (
    AuthenticationError,
    RateLimitError,
    ProviderError
)

try:
    response = await client.chat("Ola!")
except AuthenticationError as e:
    print(f"API key invalida: {e}")
except RateLimitError as e:
    print(f"Rate limit excedido. Aguarde {e.retry_after}s")
except ProviderError as e:
    print(f"Erro do provider {e.provider}: {e}")
```

---

## 11. Exemplos Completos

### 11.1 Chatbot Simples

```python
import asyncio
from forge_llm import Client

async def chatbot():
    client = Client(provider="openai", api_key="sk-...")
    conv = client.create_conversation(
        system="Voce e um assistente amigavel"
    )

    while True:
        user_input = input("Voce: ")
        if user_input.lower() == "sair":
            break

        response = await conv.chat(user_input)
        print(f"Bot: {response.content}")

asyncio.run(chatbot())
```

### 11.2 Assistente com Tools

```python
import asyncio
import json
from forge_llm import Client
from forge_llm.domain.value_objects import Message

# Funcoes disponiveis
def calculate(expression: str) -> str:
    return str(eval(expression))

def get_date() -> str:
    from datetime import datetime
    return datetime.now().strftime("%d/%m/%Y")

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Calcular expressao matematica",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string"}
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_date",
            "description": "Obter data atual",
            "parameters": {"type": "object", "properties": {}}
        }
    }
]

FUNCTIONS = {
    "calculate": calculate,
    "get_date": get_date,
}

async def assistant_with_tools():
    client = Client(provider="openai", api_key="sk-...")

    user_message = "Quanto e 15% de 200? E qual a data de hoje?"
    response = await client.chat(user_message, tools=TOOLS)

    while response.has_tool_calls:
        # Executar cada tool
        tool_results = []
        for tc in response.tool_calls:
            func = FUNCTIONS[tc.name]
            result = func(**tc.arguments)
            tool_results.append(Message(
                role="tool",
                content=result,
                tool_call_id=tc.id
            ))

        # Continuar conversa
        messages = [
            Message(role="user", content=user_message),
            Message(role="assistant", content=response.content or ""),
        ] + tool_results

        response = await client.chat(messages, tools=TOOLS)

    print(response.content)

asyncio.run(assistant_with_tools())
```

---

## 12. Observabilidade

### 12.1 Logging e Metricas

```python
from forge_llm import Client, ObservabilityManager, LoggingObserver, MetricsObserver

# Configurar observabilidade
obs = ObservabilityManager()
obs.add_observer(LoggingObserver())
obs.add_observer(MetricsObserver())

# Usar com client
client = Client(
    provider="openai",
    api_key="sk-...",
    observability=obs
)

# Chamadas sao logadas automaticamente
response = await client.chat("Ola!")

# Ver metricas
metrics = obs._observers[1].metrics  # MetricsObserver
print(f"Total requests: {metrics.total_requests}")
print(f"Total tokens: {metrics.total_tokens}")
```

Para mais detalhes, veja [Guia de Observabilidade](observability.md).

---

## 13. Integracao MCP

### 13.1 Usando Tools MCP

```python
from forge_llm import Client, MCPClient, MCPServerConfig

# Conectar ao servidor MCP
mcp = MCPClient()
await mcp.connect(MCPServerConfig(
    name="filesystem",
    command="npx",
    args=["-y", "@modelcontextprotocol/server-filesystem", "/tmp"],
))

# Obter tools
tool_defs = mcp.get_tool_definitions()

# Usar com client
client = Client(provider="openai", api_key="sk-...")
response = await client.chat("Liste arquivos em /tmp", tools=tool_defs)

# Processar tool calls
if response.has_tool_calls:
    for tc in response.tool_calls:
        result = await mcp.call_tool(tc.name, tc.arguments)
        print(result.content)

await mcp.disconnect_all()
```

Para mais detalhes, veja [Guia de Integracao MCP](mcp-integration.md).

---

## 14. Auto-Fallback

### 14.1 Fallback entre Providers

```python
from forge_llm import Client
from forge_llm.providers.auto_fallback_provider import AutoFallbackProvider

# Criar provider com fallback
fallback = AutoFallbackProvider(
    providers=["openai", "anthropic"],
    api_keys={
        "openai": "sk-...",
        "anthropic": "sk-ant-...",
    },
)

# Usar normalmente
client = Client(provider=fallback)
response = await client.chat("Ola!")

# Se OpenAI falhar (rate limit), tenta Anthropic automaticamente
print(f"Respondido por: {fallback.last_provider_used}")
```

Para mais detalhes, veja [Guia de Auto-Fallback](auto-fallback.md).

---

## Recursos Adicionais

- [Guia do Modelo de Dominio](domain-model.md) - Entidades e Value Objects
- [Guia de Tratamento de Erros](error-handling.md) - Excecoes e retry
- [Guia de Criacao de Providers](creating-providers.md) - Adicionar novos providers
- [Guia de Observabilidade](observability.md) - Logging e metricas
- [Guia de Integracao MCP](mcp-integration.md) - Tools externas via MCP
- [Guia de Auto-Fallback](auto-fallback.md) - Alta disponibilidade

---

**Versao**: ForgeLLMClient 0.1.0
