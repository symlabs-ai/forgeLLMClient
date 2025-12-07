# Instalacao

## Requisitos

- Python 3.12 ou superior
- pip, uv, ou poetry

## Instalacao Rapida

=== "pip"

    ```bash
    pip install forge-llm
    ```

=== "uv"

    ```bash
    uv add forge-llm
    ```

=== "poetry"

    ```bash
    poetry add forge-llm
    ```

## Instalacao do Codigo Fonte

```bash
# Clone o repositorio
git clone https://github.com/symlabs-ai/forgellmclient.git
cd forgellmclient

# Crie um ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows

# Instale em modo editavel
pip install -e .
```

## Dependencias Opcionais

### Para desenvolvimento completo

```bash
pip install forge-llm[dev]
```

Inclui:
- pytest, pytest-asyncio, pytest-cov (testes)
- mypy (type checking)
- ruff (linting)

### Para documentacao

```bash
pip install forge-llm[docs]
```

Inclui:
- mkdocs-material
- mkdocstrings

### Instalacao completa

```bash
pip install forge-llm[dev,docs]
```

## Configuracao de API Keys

### Via Variaveis de Ambiente (Recomendado)

Crie um arquivo `.env` na raiz do projeto:

```bash
# .env
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
OPENROUTER_API_KEY=sk-or-...
```

Ou exporte diretamente:

```bash
# OpenAI
export OPENAI_API_KEY="sk-..."

# Anthropic
export ANTHROPIC_API_KEY="sk-ant-..."

# OpenRouter
export OPENROUTER_API_KEY="sk-or-..."
```

### Via Codigo

```python
from forge_llm import Client

client = Client(
    provider="openai",
    api_key="sk-..."  # Nao recomendado em producao
)
```

!!! warning "Seguranca"
    Nunca commite API keys no codigo. Use variaveis de ambiente ou secrets managers.

## Verificando a Instalacao

### Via Python

```python
import forge_llm
print(f"ForgeLLM v{forge_llm.__version__}")

# Listar exports disponiveis
print(forge_llm.__all__)
```

### Via CLI

```bash
# Verificar versao
forge-llm --version

# Listar providers disponiveis
forge-llm providers

# Testar chat (requer API key)
forge-llm chat "Hello!" --provider openai
```

## Estrutura de Arquivos

Apos instalacao, voce tera acesso a:

```python
from forge_llm import (
    # Client principal
    Client,

    # Entidades
    ChatResponse,
    Conversation,
    ToolCall,

    # Value Objects
    Message,
    TokenUsage,
    ToolDefinition,

    # Excecoes
    ForgeError,
    ProviderError,
    ValidationError,

    # Observabilidade
    ObservabilityManager,
    LoggingObserver,

    # MCP
    MCPClient,
    MCPServerConfig,
)
```

## Solucao de Problemas

### Erro: ModuleNotFoundError

```bash
# Verifique se o pacote esta instalado
pip show forge-llm

# Reinstale se necessario
pip install --force-reinstall forge-llm
```

### Erro: Python version incompatible

```bash
# Verifique sua versao do Python
python --version  # Deve ser >= 3.12

# Use pyenv para gerenciar versoes
pyenv install 3.12
pyenv local 3.12
```

### Erro: API Key invalida

```python
from forge_llm import Client, AuthenticationError

try:
    client = Client(provider="openai", api_key="invalid")
    await client.chat("test")
except AuthenticationError as e:
    print(f"Erro de autenticacao: {e}")
```

## Proximos Passos

- [Quick Start](quickstart.md) - Comece a usar o ForgeLLM
- [Exemplos](../examples/basic-chat.md) - Veja exemplos de codigo
- [Arquitetura](../advanced/architecture.md) - Entenda a estrutura do SDK
