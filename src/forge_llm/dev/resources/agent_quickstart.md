# ForgeLLM - Guia Rapido para Agentes de IA

**Publico-alvo**: Agentes de codigo de IA (Claude Code, Cursor, GitHub Copilot, Aider, etc.)

## Referencia Rapida

### Importar Tudo que Voce Precisa

```python
from forge_llm.dev.api import (
    ComponentDiscovery,
    QualityChecker,
    ScaffoldGenerator,
    TestRunner,
)
```

### Acessar Este Guia Programaticamente

```python
# Agentes de IA podem carregar este guia programaticamente
from forge_llm.dev import get_agent_quickstart

guide = get_agent_quickstart()
print(guide)  # Conteudo markdown completo deste arquivo
```

---

## API 1: Descoberta de Componentes

**Quando usar**: Antes de modificar arquitetura, entender estrutura do projeto

```python
from forge_llm.dev.api import ComponentDiscovery

discovery = ComponentDiscovery()
result = discovery.scan_project()

# Acessar componentes descobertos
print(f"Ports: {len(result.ports)}")
print(f"Entities: {len(result.entities)}")
print(f"UseCases: {len(result.usecases)}")
print(f"Adapters: {len(result.adapters)}")

for port in result.ports:
    print(f"  - {port.name} em {port.file_path}:{port.line_number}")
```

**Estrutura de Dados**:
```python
ComponentInfo(
    name="ProviderPort",
    type="port",
    file_path="application/ports/provider_port.py",
    line_number=11,
    base_class="Protocol",
    imports=["from typing import Protocol"],
    docstring="Interface para provedores de LLM"
)
```

---

## API 2: Verificacao de Qualidade

**Quando usar**: Antes de commits, durante code review

```python
from forge_llm.dev.api import QualityChecker

checker = QualityChecker()

# Executar ferramenta especifica
ruff_result = checker.run_ruff()
mypy_result = checker.run_mypy()

# Ou executar tudo
results = checker.run_all()

for tool, result in results.items():
    if not result.passed:
        for error in result.errors:
            print(f"Corrigir {error['file']}:{error['line']} - {error['code']}")
```

---

## API 3: Geracao de Codigo

**Quando usar**: Criar novos UseCases, Entities, Providers

```python
from forge_llm.dev.api import ScaffoldGenerator

generator = ScaffoldGenerator()

# Gerar novo Provider
result = generator.create_provider(
    name="AzureOpenAI",
    base_url="https://api.azure.com/openai",
)

if result.success:
    with open(result.file_path, 'w') as f:
        f.write(result.code)
```

---

## API 4: Execucao de Testes

**Quando usar**: Executar testes, analisar falhas

```python
from forge_llm.dev.api import TestRunner

runner = TestRunner()

# Executar suite especifica
unit_result = runner.run_unit_tests()
integration_result = runner.run_integration_tests()

# Ou executar tudo
results = runner.run_all()

for test_type, result in results.items():
    if not result.passed:
        for failure in result.failures:
            print(f"Falhou: {failure.test_name}")
            print(f"  Erro: {failure.message}")
```

---

## Exemplo de Workflow Completo

```python
from forge_llm.dev.api import ComponentDiscovery, QualityChecker, TestRunner

# 1. Descobrir estrutura do projeto
discovery = ComponentDiscovery()
components = discovery.scan_project()
print(f"Encontrados {components.total_components} componentes")

# 2. Verificar qualidade
checker = QualityChecker()
quality = checker.run_all()

# 3. Executar testes
runner = TestRunner()
tests = runner.run_all()

if tests["unit"].passed and quality["ruff"].passed:
    print("Pronto para commit!")
```

---

## Arquitetura do ForgeLLM

### Estrutura de Pastas

```
src/forge_llm/
    application/
        ports/          # Interfaces (ProviderPort, etc.)
        usecases/       # Casos de uso
    domain/
        entities.py     # Entidades de dominio
        value_objects.py # Value Objects
        exceptions.py   # Excecoes customizadas
    infrastructure/
        cache.py        # Cache em memoria
        rate_limiter.py # Rate limiting
        hooks.py        # Sistema de hooks
    providers/          # Implementacoes de LLM
        openai_provider.py
        anthropic_provider.py
        ollama_provider.py
        llamacpp_provider.py
        ...
    observability/      # Metricas e logging
    persistence/        # Persistencia de conversas
    mcp/                # Model Context Protocol
    dev/                # Ferramentas para agentes
    client.py           # Client principal
```

### Componentes Principais

| Componente | Descricao |
|------------|-----------|
| `Client` | Facade principal para interagir com LLMs |
| `ProviderPort` | Interface que todos providers implementam |
| `Conversation` | Gerencia historico de mensagens |
| `ChatResponse` | Resposta estruturada do LLM |
| `Message` | Value object para mensagens |
| `ToolCall` | Value object para chamadas de ferramentas |

### Providers Disponiveis

| Provider | Descricao |
|----------|-----------|
| `openai` | OpenAI GPT-4, GPT-3.5 |
| `anthropic` | Claude 3.5, Claude 3 |
| `ollama` | Modelos locais via Ollama |
| `llamacpp` | Modelos GGUF locais |
| `gemini` | Google Gemini |
| `openrouter` | Multiplos providers via OpenRouter |
| `auto-fallback` | Fallback automatico entre providers |

---

## Guia de Decisao para Agentes de IA

### Quando Usar Qual API?

| Tarefa | API | Metodo |
|--------|-----|--------|
| "Que providers existem?" | ComponentDiscovery | `scan_project()` |
| "Quais sao as interfaces?" | ComponentDiscovery | `result.ports` |
| "Verificar codigo" | QualityChecker | `run_all()` |
| "Corrigir linting" | QualityChecker | `run_ruff()` |
| "Executar testes" | TestRunner | `run_all()` |
| "Criar novo provider" | ScaffoldGenerator | `create_provider()` |

---

## Boas Praticas para Agentes de IA

### FACA:
1. **Use APIs Python** - Importe e chame diretamente
2. **Verifique qualidade antes de commit** - `QualityChecker.run_all()`
3. **Descubra antes de modificar** - `ComponentDiscovery.scan_project()`
4. **Execute testes apos mudancas** - `TestRunner.run_all()`

### NAO FACA:
1. **Nao parsear output CLI** - Use as APIs estruturadas
2. **Nao adivinhar localizacoes** - Use discovery
3. **Nao commitar sem verificar** - Execute qualidade e testes

---

**Versao**: ForgeLLM 0.1.1
**Para**: Agentes de Codigo de IA
