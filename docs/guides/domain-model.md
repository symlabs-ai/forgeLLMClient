# Guia: Modelo de Dominio do ForgeLLMClient

Este guia documenta as entidades e value objects do ForgeLLMClient, seguindo principios de Domain-Driven Design.

---

## 1. Visao Geral

O modelo de dominio do ForgeLLMClient esta organizado em:

```
src/forge_llm/domain/
├── entities.py       # Entidades com identidade
├── value_objects.py  # Objetos imutaveis
└── exceptions.py     # Excecoes de dominio
```

### Diagrama de Classes

```
┌─────────────────────────────────────────────────────────┐
│                    ENTITIES                              │
├─────────────────────────────────────────────────────────┤
│  ChatResponse                                            │
│  ├── content: str                                        │
│  ├── model: str                                          │
│  ├── provider: str                                       │
│  ├── usage: TokenUsage                                   │
│  ├── tool_calls: list[ToolCall]                         │
│  └── id: str                                             │
│                                                          │
│  ToolCall                                                │
│  ├── name: str                                           │
│  ├── arguments: dict                                     │
│  └── id: str                                             │
│                                                          │
│  Conversation                                            │
│  ├── messages: list[Message]                            │
│  └── system_prompt: str                                  │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                  VALUE OBJECTS                           │
├─────────────────────────────────────────────────────────┤
│  Message (frozen)                                        │
│  ├── role: "system" | "user" | "assistant" | "tool"     │
│  ├── content: str | list[str | ImageContent]            │
│  ├── name: str | None                                    │
│  └── tool_call_id: str | None                           │
│                                                          │
│  TokenUsage (frozen)                                     │
│  ├── prompt_tokens: int                                  │
│  ├── completion_tokens: int                             │
│  └── total_tokens: int                                   │
│                                                          │
│  ImageContent (frozen)                                   │
│  ├── url: str | None                                     │
│  ├── base64_data: str | None                            │
│  └── media_type: str                                     │
│                                                          │
│  ToolDefinition (frozen)                                 │
│  ├── name: str                                           │
│  ├── description: str                                    │
│  └── parameters: dict                                    │
└─────────────────────────────────────────────────────────┘
```

---

## 2. Entidades

Entidades possuem identidade unica e ciclo de vida.

### 2.1 ChatResponse

Resposta completa de uma chamada de chat.

```python
from forge_llm.domain.entities import ChatResponse

# Atributos
response.content        # str: Texto da resposta
response.model          # str: Modelo usado (ex: "gpt-4o")
response.provider       # str: Provider (ex: "openai")
response.usage          # TokenUsage: Consumo de tokens
response.tool_calls     # list[ToolCall]: Tools chamadas
response.finish_reason  # str: Razao de termino ("stop", "tool_calls")
response.id             # str: ID unico (ex: "resp_abc123")
response.created_at     # datetime: Timestamp

# Propriedades
response.has_tool_calls  # bool: True se tem tool calls

# Metodos
response.to_dict()       # dict: Converter para dicionario
```

**Exemplo de uso:**

```python
response = await client.chat("Ola!")

print(f"Resposta: {response.content}")
print(f"Modelo: {response.model}")
print(f"Tokens: {response.usage.total_tokens}")

if response.has_tool_calls:
    for tc in response.tool_calls:
        print(f"Tool: {tc.name}({tc.arguments})")
```

### 2.2 ToolCall

Representa uma chamada de ferramenta solicitada pelo LLM.

```python
from forge_llm.domain.entities import ToolCall

# Atributos
tool_call.name       # str: Nome da funcao
tool_call.arguments  # dict: Argumentos parseados
tool_call.id         # str: ID unico (ex: "call_abc123")

# Metodos
tool_call.to_dict()  # dict: Converter para dicionario
```

**Exemplo:**

```python
# Criar manualmente
tc = ToolCall(
    name="get_weather",
    arguments={"city": "Sao Paulo", "unit": "celsius"}
)

print(tc.id)         # "call_abc123..." (gerado automaticamente)
print(tc.name)       # "get_weather"
print(tc.arguments)  # {"city": "Sao Paulo", "unit": "celsius"}
```

### 2.3 Conversation

Gerencia historico de conversas multi-turn.

```python
from forge_llm.domain.entities import Conversation

# Criar via client
conv = client.create_conversation(
    system="Voce e um assistente",
    max_messages=20
)

# Propriedades
conv.system_prompt   # str | None: System prompt
conv.messages        # list[Message]: Historico (copia)
conv.message_count   # int: Quantidade de mensagens
conv.max_messages    # int | None: Limite

# Metodos
conv.is_empty()                    # bool: Verifica se vazio
conv.add_user_message(content)     # Adicionar msg usuario
conv.add_assistant_message(content)# Adicionar msg assistant
conv.get_messages_for_api()        # Mensagens formatadas
conv.clear()                       # Limpar historico
await conv.chat(message)           # Enviar e receber
```

**Exemplo:**

```python
conv = client.create_conversation(system="Responda em portugues")

# Primeira mensagem
r1 = await conv.chat("Ola!")
print(r1.content)  # "Ola! Como posso ajudar?"

# Segunda mensagem (mantem contexto)
r2 = await conv.chat("Qual foi minha primeira mensagem?")
print(r2.content)  # "Voce disse 'Ola!'"

# Verificar historico
print(conv.message_count)  # 4 (user + assistant + user + assistant)

# Limpar
conv.clear()
print(conv.is_empty())  # True
```

---

## 3. Value Objects

Value objects sao imutaveis e comparados por valor.

### 3.1 Message

Mensagem em uma conversa. Imutavel (frozen).

```python
from forge_llm.domain.value_objects import Message

# Roles validos
"system"     # Instrucoes do sistema
"user"       # Mensagem do usuario
"assistant"  # Resposta do LLM
"tool"       # Resultado de tool call

# Atributos
message.role          # str: Role da mensagem
message.content       # str | list: Conteudo
message.name          # str | None: Nome opcional
message.tool_call_id  # str | None: ID do tool call

# Propriedades
message.has_images    # bool: Contem imagens?
message.images        # list[ImageContent]: Lista de imagens
message.text_content  # str: Apenas texto

# Metodos
message.to_dict()     # dict: Converter
```

**Exemplos:**

```python
# Mensagem simples
msg = Message(role="user", content="Ola!")

# System prompt
system = Message(role="system", content="Voce e um chef")

# Mensagem com imagem
from forge_llm.domain.value_objects import ImageContent

msg = Message(
    role="user",
    content=[
        "O que e isso?",
        ImageContent(url="https://example.com/foto.jpg")
    ]
)
print(msg.has_images)   # True
print(len(msg.images))  # 1

# Resultado de tool
tool_msg = Message(
    role="tool",
    content='{"temp": 25}',
    tool_call_id="call_abc123"
)
```

### 3.2 TokenUsage

Informacoes de consumo de tokens. Imutavel.

```python
from forge_llm.domain.value_objects import TokenUsage

# Atributos
usage.prompt_tokens      # int: Tokens do prompt
usage.completion_tokens  # int: Tokens da resposta
usage.total_tokens       # int: Total (calculado se nao fornecido)

# Metodos
usage.to_dict()          # dict: Converter
```

**Exemplo:**

```python
# Total calculado automaticamente
usage = TokenUsage(prompt_tokens=100, completion_tokens=50)
print(usage.total_tokens)  # 150

# Validacao
usage = TokenUsage(prompt_tokens=-1, completion_tokens=0)
# Raises: ValidationError("prompt_tokens nao pode ser negativo")
```

### 3.3 ImageContent

Conteudo de imagem para mensagens multimodais. Imutavel.

```python
from forge_llm.domain.value_objects import ImageContent

# Por URL
img = ImageContent(url="https://example.com/foto.jpg")

# Por Base64
img = ImageContent(
    base64_data="iVBORw0KGgo...",
    media_type="image/png"
)

# Atributos
img.url           # str | None: URL da imagem
img.base64_data   # str | None: Dados em base64
img.media_type    # str: Tipo MIME (default: "image/jpeg")

# Propriedades
img.is_url        # bool: E URL?
img.is_base64     # bool: E base64?

# Metodos
img.to_dict()     # dict: Converter
```

**Validacoes:**

```python
# URL ou base64, nunca ambos
ImageContent(url="...", base64_data="...")
# Raises: ValidationError("Usar URL ou base64_data, nao ambos")

# Pelo menos um obrigatorio
ImageContent()
# Raises: ValidationError("URL ou base64_data obrigatorio")

# Media types validos
ImageContent(url="...", media_type="image/bmp")
# Raises: ValidationError("Media type invalido: image/bmp")
# Validos: image/jpeg, image/png, image/gif, image/webp

# Limite de 20MB para base64
ImageContent(base64_data="..." * 30_000_000)
# Raises: ValidationError("Base64 excede limite de 20MB")
```

### 3.4 ToolDefinition

Definicao de uma ferramenta. Imutavel.

```python
from forge_llm.domain.value_objects import ToolDefinition

# Atributos
tool.name         # str: Nome da funcao
tool.description  # str: Descricao
tool.parameters   # dict: JSON Schema dos parametros

# Metodos
tool.to_dict()    # dict: Converter para formato OpenAI
```

**Exemplo:**

```python
tool = ToolDefinition(
    name="search_web",
    description="Buscar na internet",
    parameters={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Termo de busca"
            }
        },
        "required": ["query"]
    }
)

# Converter para formato da API
tools = [{"type": "function", "function": tool.to_dict()}]
```

---

## 4. Validacoes

Todos os objetos validam seus dados na criacao.

### 4.1 Validacoes de Message

| Campo | Regra | Erro |
|-------|-------|------|
| role | Deve ser system/user/assistant/tool | `Role invalido: {role}` |
| tool_call_id | Obrigatorio se role="tool" | `tool_call_id obrigatorio para role 'tool'` |

### 4.2 Validacoes de TokenUsage

| Campo | Regra | Erro |
|-------|-------|------|
| prompt_tokens | >= 0 | `prompt_tokens nao pode ser negativo` |
| completion_tokens | >= 0 | `completion_tokens nao pode ser negativo` |

### 4.3 Validacoes de ImageContent

| Campo | Regra | Erro |
|-------|-------|------|
| url/base64 | Um ou outro | `URL ou base64_data obrigatorio` |
| url+base64 | Nao ambos | `Usar URL ou base64_data, nao ambos` |
| media_type | jpeg/png/gif/webp | `Media type invalido: {type}` |
| base64_data | <= 20MB | `Base64 excede limite de 20MB` |

### 4.4 Validacoes de ToolCall

| Campo | Regra | Erro |
|-------|-------|------|
| name | Obrigatorio | `Nome da tool e obrigatorio` |
| arguments | Deve ser dict | `Argumentos devem ser um dicionario` |

### 4.5 Validacoes de ChatResponse

| Campo | Regra | Erro |
|-------|-------|------|
| model | Obrigatorio | `Modelo e obrigatorio` |
| provider | Obrigatorio | `Provider e obrigatorio` |

---

## 5. Conversao para Dicionario

Todos os objetos possuem metodo `to_dict()`:

```python
# Message
Message(role="user", content="Ola").to_dict()
# {"role": "user", "content": "Ola"}

# TokenUsage
TokenUsage(prompt_tokens=10, completion_tokens=5).to_dict()
# {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15}

# ImageContent
ImageContent(url="https://...").to_dict()
# {"type": "url", "url": "https://...", "media_type": "image/jpeg"}

# ToolCall
ToolCall(name="f", arguments={"x": 1}).to_dict()
# {"id": "call_...", "name": "f", "arguments": {"x": 1}}
```

---

## 6. Imutabilidade

Value objects sao frozen (imutaveis):

```python
msg = Message(role="user", content="Ola")

# Isso gera erro
msg.content = "Outro"  # FrozenInstanceError

# Criar nova instancia em vez de modificar
new_msg = Message(role="user", content="Outro")
```

---

## 7. Igualdade

Value objects sao comparados por valor:

```python
# Duas mensagens iguais
msg1 = Message(role="user", content="Ola")
msg2 = Message(role="user", content="Ola")

print(msg1 == msg2)  # True
print(hash(msg1) == hash(msg2))  # True

# Podem ser usados em sets/dicts
messages = {msg1, msg2}
print(len(messages))  # 1 (sao iguais)
```

---

## 8. Imports

```python
# Entidades
from forge_llm.domain.entities import (
    ChatResponse,
    ToolCall,
    Conversation,
)

# Value Objects
from forge_llm.domain.value_objects import (
    Message,
    TokenUsage,
    ImageContent,
    ToolDefinition,
)

# Excecoes
from forge_llm.domain.exceptions import (
    ValidationError,
    # ... outras
)
```

---

## Recursos Adicionais

- [Guia de Uso do Client](client-usage.md) - Como usar o SDK
- [Guia de Tratamento de Erros](error-handling.md) - Excecoes
- [Guia de Criacao de Providers](creating-providers.md) - Novos providers

---

**Versao**: ForgeLLMClient 0.1.0
