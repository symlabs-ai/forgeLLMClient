# 🔹 BDD Subetapa 5: Skeleton de Automação

## 🎯 Propósito

Criar a **infraestrutura de testes BDD** que permitirá ao time de desenvolvimento:
- Começar o ciclo TDD imediatamente (Red-Green-Refactor)
- Executar features Gherkin como testes automatizados
- Validar comportamentos conforme implementação avança

Esta etapa **NÃO implementa** os testes — apenas prepara o esqueleto.

---

## ⚙️ Entradas e Saídas

| Tipo | Artefato | Descrição |
|------|----------|-----------|
| **Entrada** | `specs/bdd/**/*.feature` | Features Gherkin finalizadas |
| **Saída** | `tests/bdd/test_*_steps.py` | Step definitions (vazias) |
| **Saída** | `tests/bdd/conftest.py` | Fixtures pytest |
| **Saída** | `pytest.ini` | Configuração de marcadores |
| **Saída** | `requirements-dev.txt` | Dependências de teste |

---

## 🧩 Componentes do Skeleton

### 1. **Step Definitions** (`test_*_steps.py`)

Arquivos que vinculam steps Gherkin a código Python.

**Estrutura base:**

```python
# tests/bdd/test_forge_chat_steps.py

import pytest
from pytest_bdd import scenarios, given, when, then, parsers

# ===========================
# IMPORTANTE: Marcar como skip
# ===========================
pytestmark = pytest.mark.skip("BDD (Forge chat) pendente de implementação")

# ===========================
# Vincular feature Gherkin
# ===========================
scenarios("../../specs/bdd/10_forge_core/chat.feature")

# ===========================
# Step Definitions (vazias)
# ===========================

@given('que o Forge está configurado com o provedor "echo"', target_fixture="forge_client")
def forge_with_echo_provider():
    """
    TODO (TDD): Implementar configuração do Forge com provedor echo.

    Quando implementar:
    1. Remover pytest.mark.skip do topo do arquivo
    2. Importar ForgeClient
    3. Retornar instância configurada

    Exemplo:
        from forge import ForgeClient
        return ForgeClient(provider="echo")
    """
    pytest.skip("Aguardando implementação (TDD)")

@when(parsers.parse('envio a mensagem "{message}"'), target_fixture="response")
def send_message(forge_client, message):
    """
    TODO (TDD): Implementar envio de mensagem.

    Quando implementar:
        return forge_client.chat(message)
    """
    pytest.skip("Aguardando implementação (TDD)")

@then(parsers.parse('recebo uma resposta contendo "{text}"'))
def check_response_contains(response, text):
    """
    TODO (TDD): Validar conteúdo da resposta.

    Quando implementar:
        assert text in response.content
    """
    pytest.skip("Aguardando implementação (TDD)")
```

**Convenções de nomenclatura:**

```
Feature: specs/bdd/10_forge_core/chat.feature
  ↓
Step file: tests/bdd/test_forge_chat_steps.py

Feature: specs/bdd/20_symclient_http/errors.feature
  ↓
Step file: tests/bdd/test_symclient_http_errors_steps.py
```

---

### 2. **Fixtures Compartilhadas** (`conftest.py`)

Fixtures reutilizáveis em todos os testes BDD.

```python
# tests/bdd/conftest.py

import pytest

# ===========================
# Contexto Compartilhado
# ===========================

@pytest.fixture
def context():
    """
    Dicionário compartilhado entre steps de um cenário.

    Uso:
        @given(...)
        def some_step(context):
            context['user_id'] = 123

        @then(...)
        def another_step(context):
            assert context['user_id'] == 123
    """
    return {}

# ===========================
# Configurações de Teste
# ===========================

@pytest.fixture
def forge_config():
    """
    Configuração padrão do Forge para testes.

    TODO (TDD): Ajustar conforme implementação real.
    """
    return {
        "provider": "echo",
        "timeout": 30,
        "log_level": "DEBUG"
    }

@pytest.fixture
def symclient_http_url():
    """
    URL base do SymClient HTTP para testes.

    Assume que SymClient está rodando localmente.
    """
    return "http://localhost:8000"

@pytest.fixture
def symclient_stdio_process():
    """
    TODO (TDD): Iniciar processo SymClient STDIO para testes.

    Quando implementar:
        import subprocess
        process = subprocess.Popen(["symclient", "stdio"])
        yield process
        process.terminate()
    """
    pytest.skip("SymClient STDIO não implementado ainda")

# ===========================
# Hooks de Teste
# ===========================

def pytest_bdd_before_scenario(request, feature, scenario):
    """
    Executado antes de cada cenário.
    Útil para logging ou setup global.
    """
    print(f"\n▶️  Cenário: {scenario.name}")

def pytest_bdd_after_scenario(request, feature, scenario):
    """
    Executado após cada cenário.
    Útil para cleanup ou métricas.
    """
    print(f"✅ Cenário concluído: {scenario.name}")

def pytest_bdd_step_error(request, feature, scenario, step, step_func, step_func_args, exception):
    """
    Executado quando um step falha.
    """
    print(f"❌ Step falhou: {step.name}")
    print(f"   Erro: {exception}")
```

---

### 3. **Configuração pytest** (`pytest.ini`)

Define marcadores (tags) e comportamento dos testes.

```ini
# pytest.ini

[pytest]
# ===========================
# Marcadores (Tags)
# ===========================
markers =
    # Tiers de execução
    ci_fast: Testes rápidos (mocks, sem deps externas)
    ci_int: Testes de integração (provedores locais)
    e2e: Testes end-to-end (deps externas)

    # Domínios
    sdk: Forge SDK Python
    server: SymClient (HTTP ou STDIO)
    http: Protocolo HTTP
    stdio: Protocolo STDIO/JSON-RPC

    # Capacidades
    contexto: Gestão de sessão/contexto
    streaming: Respostas em stream
    capability_tool_calling: Tool calling / function calling
    fallback: Estratégias de fallback

    # Integrações
    mcp: Integração MCP Tecnospeed
    broker: Roteamento via LLM Broker
    tecnospeed: Ecossistema Tecnospeed

    # Categorias
    observabilidade: Logs, métricas, traces
    seguranca: Auth, redaction, rate limit
    erro: Cenários de tratamento de erro

# ===========================
# Comportamento de Testes
# ===========================
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

# Opções padrão
addopts =
    -v
    --strict-markers
    --tb=short
    --disable-warnings

# ===========================
# BDD Específico
# ===========================
bdd_features_base_dir = specs/bdd/
```

---

### 4. **Dependências de Teste** (`requirements-dev.txt`)

```txt
# requirements-dev.txt

# Framework de testes
pytest>=7.4.0
pytest-cov>=4.1.0
pytest-html>=3.2.0

# BDD
pytest-bdd>=6.1.1

# Linting e formatação
black>=23.0.0
flake8>=6.0.0
mypy>=1.4.0

# Type stubs
types-requests>=2.31.0

# Utilitários de teste
faker>=19.0.0           # Geração de dados fake
responses>=0.23.0       # Mock de requisições HTTP
pytest-mock>=3.11.0     # Mocking avançado
```

---

## 📋 Checklist de Criação de Skeleton

### Para Cada Feature Gherkin

```markdown
- [ ] Criar arquivo `tests/bdd/test_[nome]_steps.py`
- [ ] Adicionar `pytestmark = pytest.mark.skip(...)`
- [ ] Vincular feature: `scenarios("../../specs/bdd/[path]/[feature].feature")`
- [ ] Criar step definitions vazias para cada DADO/QUANDO/ENTÃO
- [ ] Adicionar docstrings com TODO e exemplos
- [ ] Testar que arquivo roda sem erros: `pytest tests/bdd/test_[nome]_steps.py -v`
```

---

## 🧪 Validação do Skeleton

### Teste 1: Arquivos Reconhecidos

```bash
# Pytest deve descobrir todos os testes BDD
pytest --collect-only tests/bdd/

# Saída esperada:
# <Module tests/bdd/test_forge_chat_steps.py>
#   <Function test_enviar_mensagem_simples[...]>
# <Module tests/bdd/test_forge_sessao_steps.py>
#   <Function test_preservar_contexto[...]>
# ...
```

### Teste 2: Execução com Skip

```bash
# Todos os testes devem ser pulados (ainda não implementados)
pytest tests/bdd/ -v

# Saída esperada:
# tests/bdd/test_forge_chat_steps.py::test_enviar... SKIPPED (BDD pendente)
# tests/bdd/test_forge_sessao_steps.py::test_preservar... SKIPPED (BDD pendente)
# ...
# =================== X skipped in 0.5s ===================
```

### Teste 3: Marcadores Funcionando

```bash
# Filtrar por tag
pytest -m ci_fast tests/bdd/ --collect-only

# Deve listar apenas features com @ci-fast
```

---

## 🎯 Exemplo: Skeleton para Feature de Sessão

**Feature:**
```gherkin
# specs/bdd/10_forge_core/sessao.feature

@sdk @contexto @ci-fast
FUNCIONALIDADE: Gestão de sessões
  ...

  CENÁRIO: Preservar histórico na sessão
    DADO um session_id "abc123"
    E o Forge configurado com provedor "echo"
    QUANDO envio mensagem "Olá"
    E envio mensagem "Tudo bem?"
    ENTÃO a resposta final considera o histórico
```

**Skeleton:**
```python
# tests/bdd/test_forge_sessao_steps.py

import pytest
from pytest_bdd import scenarios, given, when, then, parsers

pytestmark = pytest.mark.skip("BDD (sessão) pendente de implementação")

scenarios("../../specs/bdd/10_forge_core/sessao.feature")

@given(parsers.parse('um session_id "{session_id}"'), target_fixture="session_id")
def create_session_id(session_id):
    """TODO: Retornar session_id para uso nos próximos steps."""
    pytest.skip("Aguardando implementação")

@given('o Forge configurado com provedor "echo"', target_fixture="forge_client")
def forge_with_echo(session_id):
    """TODO: Retornar ForgeClient configurado com session_id."""
    pytest.skip("Aguardando implementação")

@when(parsers.parse('envio mensagem "{message}"'))
def send_message_to_session(forge_client, message, context):
    """
    TODO: Enviar mensagem e guardar resposta em context.

    Quando implementar:
        response = forge_client.chat(message)
        context.setdefault('responses', []).append(response)
    """
    pytest.skip("Aguardando implementação")

@then('a resposta final considera o histórico')
def check_response_has_context(context):
    """
    TODO: Validar que a última resposta tem contexto das anteriores.

    Quando implementar:
        responses = context['responses']
        assert len(responses) >= 2
        # Validar que segunda resposta menciona primeira mensagem
    """
    pytest.skip("Aguardando implementação")
```

---

## ✅ Critérios de Qualidade (DoD)

- [ ] Step file criado para cada feature Gherkin
- [ ] Todos os steps têm docstrings com TODO
- [ ] Todos marcados com `pytest.mark.skip`
- [ ] `conftest.py` criado com fixtures base
- [ ] `pytest.ini` configurado com marcadores
- [ ] `requirements-dev.txt` atualizado
- [ ] Validação: `pytest --collect-only tests/bdd/` funciona
- [ ] Validação: `pytest tests/bdd/ -v` mostra todos skipped

---

## 🔄 Próximo Passo

Com o skeleton pronto, avance para:

**Subetapa 6: Handoff para TDD** (`etapa_06_handoff_tdd.md`)

---

**Author**: Forge Framework Team
**Version**: 1.0
**Date**: 2025-11-04
