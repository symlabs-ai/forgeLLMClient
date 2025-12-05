# Guia: Integracao MCP (Model Context Protocol)

Este guia documenta a integracao do ForgeLLMClient com servidores MCP para uso de ferramentas externas.

---

## 1. Visao Geral

MCP (Model Context Protocol) e um protocolo padrao para conectar LLMs a ferramentas externas. O ForgeLLMClient suporta conexao com servidores MCP para descoberta e execucao de ferramentas.

```
┌─────────────────────────────────────────────────────────┐
│                    ForgeLLMClient                        │
│  ┌─────────────────────────────────────────────────┐   │
│  │                   MCPClient                      │   │
│  │  ┌───────────────────────────────────────────┐  │   │
│  │  │  connect() / disconnect() / list_tools()  │  │   │
│  │  │  call_tool() / get_tool_definitions()     │  │   │
│  │  └───────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────┘   │
│                         │                               │
│         ┌───────────────┼───────────────┐              │
│         ▼               ▼               ▼              │
│  ┌───────────┐   ┌───────────┐   ┌───────────┐        │
│  │ Filesystem│   │  GitHub   │   │  Custom   │        │
│  │  Server   │   │  Server   │   │  Server   │        │
│  └───────────┘   └───────────┘   └───────────┘        │
└─────────────────────────────────────────────────────────┘
```

---

## 2. Configuracao Basica

### 2.1 Conectando a um Servidor

```python
from forge_llm import MCPClient, MCPServerConfig

# Criar cliente MCP
mcp = MCPClient()

# Configurar servidor (exemplo: filesystem)
config = MCPServerConfig(
    name="filesystem",
    command="npx",
    args=["-y", "@modelcontextprotocol/server-filesystem", "/tmp"],
)

# Conectar
await mcp.connect(config)

# Listar tools disponiveis
tools = await mcp.list_tools()
for tool in tools:
    print(f"- {tool.name}: {tool.description}")

# Desconectar quando terminar
await mcp.disconnect_all()
```

### 2.2 MCPServerConfig

Configuracao para conexao com servidor MCP.

```python
from forge_llm import MCPServerConfig

# Servidor via stdio (mais comum)
config = MCPServerConfig(
    name="meu_servidor",       # Nome unico do servidor
    command="python",          # Comando para iniciar
    args=["-m", "mcp_server"], # Argumentos
    env={"API_KEY": "..."},    # Variaveis de ambiente
    transport="stdio",         # Tipo de transporte
    timeout=30.0,              # Timeout em segundos
)

# Servidor via HTTP/SSE (futuro)
config = MCPServerConfig(
    name="remote",
    url="http://localhost:8080",
    transport="http",
)
```

**Campos:**

| Campo | Tipo | Default | Descricao |
|-------|------|---------|-----------|
| name | str | (obrigatorio) | Nome unico do servidor |
| command | str | None | Comando para iniciar (stdio) |
| args | list[str] | [] | Argumentos do comando |
| env | dict[str, str] | {} | Variaveis de ambiente |
| url | str | None | URL do servidor (http/sse) |
| transport | str | "stdio" | "stdio", "http", ou "sse" |
| timeout | float | 30.0 | Timeout para requests |

---

## 3. Trabalhando com Tools

### 3.1 Listar Tools

```python
# Listar todas as tools de todos os servidores
all_tools = await mcp.list_tools()

# Listar tools de um servidor especifico
fs_tools = await mcp.list_tools(server="filesystem")

# Inspecionar uma tool
for tool in all_tools:
    print(f"Nome: {tool.name}")
    print(f"Descricao: {tool.description}")
    print(f"Servidor: {tool.server}")
    print(f"Schema: {tool.input_schema}")
```

### 3.2 Executar Tool

```python
# Chamar tool por nome (auto-detecta servidor)
result = await mcp.call_tool(
    name="read_file",
    arguments={"path": "/tmp/test.txt"},
)

# Chamar tool em servidor especifico
result = await mcp.call_tool(
    name="read_file",
    arguments={"path": "/tmp/test.txt"},
    server="filesystem",
)

# Processar resultado
if result.is_error:
    print(f"Erro: {result.content}")
else:
    print(f"Sucesso: {result.content}")
```

### 3.3 MCPTool e MCPToolResult

```python
# MCPTool - Tool descoberta
tool.name          # str: Nome da tool
tool.description   # str: Descricao
tool.input_schema  # dict: JSON Schema dos parametros
tool.server        # str: Nome do servidor de origem

# MCPToolResult - Resultado de execucao
result.content    # str | list: Conteudo retornado
result.is_error   # bool: Se houve erro
```

---

## 4. Integracao com Client

### 4.1 Usando Tools MCP com Chat

```python
from forge_llm import Client, MCPClient, MCPServerConfig

# Configurar MCP
mcp = MCPClient()
await mcp.connect(MCPServerConfig(
    name="filesystem",
    command="npx",
    args=["-y", "@modelcontextprotocol/server-filesystem", "/tmp"],
))

# Obter definicoes das tools em formato OpenAI
tool_defs = mcp.get_tool_definitions()

# Criar client
client = Client(provider="openai", api_key="sk-...")

# Fazer chat com tools
response = await client.chat(
    message="Liste os arquivos em /tmp",
    tools=tool_defs,
)

# Processar tool calls
if response.tool_calls:
    for tool_call in response.tool_calls:
        # Executar via MCP
        result = await mcp.call_tool(
            name=tool_call.name,
            arguments=tool_call.arguments,
        )
        print(f"Resultado: {result.content}")

# Cleanup
await mcp.disconnect_all()
await client.close()
```

### 4.2 MCPToolAdapter

O adapter converte tools MCP para diferentes formatos:

```python
from forge_llm import MCPToolAdapter

# Obter tools
tools = await mcp.list_tools()

# Converter para ToolDefinition do ForgeLLM
definitions = MCPToolAdapter.to_tool_definitions(tools)

# Converter para formato OpenAI
openai_format = MCPToolAdapter.to_openai_format(tools)

# Converter para formato Anthropic
anthropic_format = MCPToolAdapter.to_anthropic_format(tools)

# Extrair dados de tool call (OpenAI)
name, args = MCPToolAdapter.from_openai_tool_call(tool_call)

# Extrair dados de tool use (Anthropic)
name, args = MCPToolAdapter.from_anthropic_tool_use(tool_use)
```

---

## 5. Multiplos Servidores

```python
from forge_llm import MCPClient, MCPServerConfig

mcp = MCPClient()

# Conectar a multiplos servidores
await mcp.connect(MCPServerConfig(
    name="filesystem",
    command="npx",
    args=["-y", "@modelcontextprotocol/server-filesystem", "/tmp"],
))

await mcp.connect(MCPServerConfig(
    name="github",
    command="npx",
    args=["-y", "@modelcontextprotocol/server-github"],
    env={"GITHUB_TOKEN": "ghp_..."},
))

# Ver servidores conectados
print(mcp.connected_servers)  # ["filesystem", "github"]

# Listar todas as tools
all_tools = await mcp.list_tools()

# Listar tools de servidor especifico
fs_tools = await mcp.list_tools(server="filesystem")
gh_tools = await mcp.list_tools(server="github")

# Chamar tool (auto-detecta servidor)
await mcp.call_tool("read_file", {"path": "/tmp/x"})  # -> filesystem
await mcp.call_tool("list_repos", {"org": "my-org"})  # -> github

# Desconectar servidor especifico
await mcp.disconnect("github")

# Desconectar todos
await mcp.disconnect_all()
```

---

## 6. Tratamento de Erros

### 6.1 Tipos de Excecao

```python
from forge_llm import (
    MCPError,              # Erro base
    MCPConnectionError,    # Falha de conexao
    MCPToolNotFoundError,  # Tool nao encontrada
    MCPToolExecutionError, # Erro na execucao
    MCPServerNotConnectedError,  # Servidor desconectado
)
```

### 6.2 Exemplos de Tratamento

```python
from forge_llm import (
    MCPClient,
    MCPServerConfig,
    MCPConnectionError,
    MCPToolNotFoundError,
    MCPToolExecutionError,
)

mcp = MCPClient()

# Erro de conexao
try:
    await mcp.connect(MCPServerConfig(
        name="invalid",
        command="comando_inexistente",
    ))
except MCPConnectionError as e:
    print(f"Falha ao conectar: {e}")
    print(f"Servidor: {e.server_name}")
    print(f"Causa: {e.cause}")

# Tool nao encontrada
try:
    await mcp.call_tool("tool_inexistente", {})
except MCPToolNotFoundError as e:
    print(f"Tool nao encontrada: {e.tool_name}")
    print(f"Disponiveis: {e.available_tools}")

# Erro de execucao
try:
    await mcp.call_tool("read_file", {"path": "/arquivo/inexistente"})
except MCPToolExecutionError as e:
    print(f"Erro ao executar: {e.tool_name}")
    print(f"Mensagem: {e}")
    print(f"Servidor: {e.server_name}")
```

---

## 7. Servidores MCP Populares

### 7.1 Filesystem

Acesso ao sistema de arquivos.

```python
config = MCPServerConfig(
    name="filesystem",
    command="npx",
    args=["-y", "@modelcontextprotocol/server-filesystem", "/path/to/dir"],
)

# Tools: read_file, write_file, list_directory, etc.
```

### 7.2 GitHub

Integracao com GitHub.

```python
config = MCPServerConfig(
    name="github",
    command="npx",
    args=["-y", "@modelcontextprotocol/server-github"],
    env={"GITHUB_TOKEN": "ghp_..."},
)

# Tools: list_repos, create_issue, search_code, etc.
```

### 7.3 PostgreSQL

Acesso a banco de dados.

```python
config = MCPServerConfig(
    name="postgres",
    command="npx",
    args=["-y", "@modelcontextprotocol/server-postgres"],
    env={"DATABASE_URL": "postgresql://..."},
)

# Tools: query, list_tables, describe_table, etc.
```

### 7.4 Servidor Customizado

```python
# Servidor Python customizado
config = MCPServerConfig(
    name="meu_servidor",
    command="python",
    args=["-m", "meu_mcp_server"],
    env={"CONFIG_PATH": "/path/to/config.json"},
)
```

---

## 8. Boas Praticas

### 8.1 Context Manager Pattern

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def mcp_session(*configs: MCPServerConfig):
    """Gerencia conexoes MCP automaticamente."""
    mcp = MCPClient()
    try:
        for config in configs:
            await mcp.connect(config)
        yield mcp
    finally:
        await mcp.disconnect_all()

# Uso
async with mcp_session(fs_config, gh_config) as mcp:
    tools = await mcp.list_tools()
    result = await mcp.call_tool("read_file", {"path": "/tmp/x"})
```

### 8.2 Logging

O MCPClient usa logging interno. Configure para debug:

```python
import logging

logging.getLogger("forge_llm.mcp").setLevel(logging.DEBUG)

# Logs:
# DEBUG - Starting subprocess: npx -y @modelcontextprotocol/server-filesystem
# DEBUG - MCP server 'filesystem' initialized successfully
# INFO - Connected to MCP server 'filesystem'. Discovered 5 tools
# DEBUG - Calling tool 'read_file' on server 'filesystem'
```

### 8.3 Timeout e Resiliencia

```python
# Timeout customizado
config = MCPServerConfig(
    name="slow_server",
    command="...",
    timeout=60.0,  # 60 segundos
)

# Verificar conexao antes de usar
if "filesystem" in mcp.connected_servers:
    result = await mcp.call_tool("read_file", {"path": "/tmp/x"})
```

---

## 9. Imports

```python
from forge_llm import (
    # Cliente
    MCPClient,
    MCPServerConfig,

    # Tipos
    MCPTool,
    MCPToolResult,

    # Adapter
    MCPToolAdapter,

    # Excecoes
    MCPError,
    MCPConnectionError,
    MCPToolNotFoundError,
    MCPToolExecutionError,
    MCPServerNotConnectedError,
)
```

---

## Recursos Adicionais

- [Guia de Uso do Client](client-usage.md) - Uso basico do SDK
- [Guia de Tratamento de Erros](error-handling.md) - Excecoes e retry
- [MCP Specification](https://modelcontextprotocol.io/) - Especificacao oficial

---

**Versao**: ForgeLLMClient 0.1.0
