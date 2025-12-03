# TDD Workflow

**Subprocesso do Execution Process – implementação guiada por testes.**

**Project (exemplo)**: forgeLLMClient (SymClient + Forge SDK)
**Team**: Agent Coders (Claude Code primary)
**Last Updated**: 2025-11-05
**Methodology**: BDD → TDD (Behavior-Driven Development → Test-Driven Development)

---

## 🎯 TDD Philosophy

### Red-Green-Refactor Cycle

```
┌─────────────────────────────────────────┐
│  1. RED: Write failing test             │
│     ↓                                    │
│  2. GREEN: Make test pass (minimal)     │
│     ↓                                    │
│  3. REFACTOR: Improve code quality      │
│     ↓                                    │
│  4. COMMIT: Save working state          │
└─────────────────────────────────────────┘
```

**Key Principles**:
- ✅ **Test First**: Escrever teste ANTES de implementar
- ✅ **Minimal Implementation**: Fazer teste passar com código mínimo
- ✅ **Refactor Confidence**: Melhorar código sabendo que testes cobrem
- ✅ **Fast Feedback**: Testes executam rápido (< 1 segundo)

---

## 📋 TDD Workflow (Per Feature)

### Phase 1: Seleção da Tarefa e BDD Scenarios

**Input Principal**: `specs/roadmap/BACKLOG.md` (item de trabalho priorizado)
**Input Secundário**: Feature file (ex: `specs/bdd/10_forge_core/config.feature`)

**Ações**:
1. ✅ **Selecionar Tarefa do BACKLOG.md:** Escolher a próxima tarefa priorizada do `BACKLOG.md`. Esta tarefa deve referenciar um ou mais cenários BDD a serem implementados.
2. ✅ **Revisar Feature File BDD:** Ler o(s) feature file(s) BDD completo(s) referenciado(s) pela tarefa do backlog.
3. ✅ **Entender Cenários Given/When/Then:** Compreender os comportamentos esperados do sistema.
4. ✅ **Mapear para Testes Python:** Preparar-se para traduzir os cenários para o Python (pytest-bdd).
---

### Phase 2: Test Setup (Red Phase Start)

**Goal**: Preparar ambiente de testes ANTES de implementar

**Ações**:
1. ✅ Criar arquivo de teste (ex: `tests/test_config.py`)
2. ✅ Setup pytest fixtures (se necessário)
3. ✅ Implementar step definitions (BDD steps → Python functions)
4. ✅ **RODAR TESTE** → Deve falhar (RED ❌)

**Exemplo**:
```python
# tests/test_config.py
import pytest
from pytest_bdd import scenario, given, when, then

@scenario('../specs/bdd/10_forge_core/config.feature',
          'Precedência de configuração (env > arquivo > defaults)')
def test_config_precedence():
    pass

@given('variáveis de ambiente definidas com provider="openrouter"')
def env_with_openrouter(monkeypatch):
    monkeypatch.setenv('FORGE_PROVIDER', 'openrouter')
    return {'provider': 'openrouter'}

@given('um arquivo de configuração com provider="echo"')
def config_file_with_echo(tmp_path):
    config = tmp_path / "config.yaml"
    config.write_text('provider: echo')
    return str(config)

@when('inicializo o Forge')
def initialize_forge(env_with_openrouter, config_file_with_echo):
    # Isso vai falhar porque ConfigService não existe ainda
    from forgellmclient.core.config import ConfigService
    service = ConfigService(config_file=config_file_with_echo)
    return service

@then('o provedor efetivo é "openrouter" (variável de ambiente)')
def check_provider_openrouter(initialize_forge):
    assert initialize_forge.provider == 'openrouter'

@then('o log registra "config source: environment variable"')
def check_log_source(initialize_forge, caplog):
    assert 'config source: environment variable' in caplog.text
```

**Run Test**:
```bash
pytest tests/test_config.py::test_config_precedence -v
```

**Expected Result**: ❌ **FAIL** (RED)
```
ImportError: cannot import name 'ConfigService' from 'forgellmclient.core.config'
```

**Why RED is Good**: Confirma que o teste está rodando e falhando pelo motivo correto.

---

### Phase 3: Minimal Implementation (Green Phase)

**Goal**: Fazer teste passar com **código mínimo**

**TDD Rules**:
1. ✅ Escrever APENAS código suficiente para passar o teste
2. ❌ Não adicionar features extras ("YAGNI" - You Aren't Gonna Need It)
3. ❌ Não otimizar prematuramente
4. ✅ Usar Forgebase patterns obrigatórios (EntityBase, UseCaseBase, etc.)

**Ações**:
1. ✅ Criar classes/funções mínimas (ConfigEntity, ConfigService)
2. ✅ Implementar lógica para passar o teste (config precedence)
3. ✅ **RODAR TESTE** → Deve passar (GREEN ✅)

**Exemplo**:
```python
# src/forgellmclient/core/config.py
from forgebase import EntityBase, UseCaseBase
from pydantic_settings import BaseSettings
import os

class ConfigEntity(EntityBase):
    """Config entity (Forgebase compliance)"""
    provider: str
    config_source: str  # "environment" | "file" | "default"

class ConfigService(UseCaseBase):
    """Config service (Forgebase compliance)"""

    def __init__(self, config_file: str = None, log_service=None):
        self.config_file = config_file
        self.log_service = log_service
        self._load_config()

    def _load_config(self):
        # Precedence: env > file > default
        if os.getenv('FORGE_PROVIDER'):
            self.provider = os.getenv('FORGE_PROVIDER')
            self.config_source = 'environment variable'
        elif self.config_file and os.path.exists(self.config_file):
            # Load from file (simplified)
            import yaml
            with open(self.config_file) as f:
                data = yaml.safe_load(f)
                self.provider = data['provider']
                self.config_source = 'config file'
        else:
            self.provider = 'echo'  # default
            self.config_source = 'default'

        if self.log_service:
            self.log_service.log(f'config source: {self.config_source}')
```

**Run Test Again**:
```bash
pytest tests/test_config.py::test_config_precedence -v
```

**Expected Result**: ✅ **PASS** (GREEN)
```
tests/test_config.py::test_config_precedence PASSED [100%]
```

---

### Phase 4: Refactor (Improve Quality)

**Goal**: Melhorar código mantendo testes verdes

**Refactoring Targets**:
- 🔧 Remover duplicação (DRY - Don't Repeat Yourself)
- 🔧 Melhorar nomes (variáveis, funções, classes)
- 🔧 Extrair funções complexas
- 🔧 Adicionar type hints
- 🔧 Aplicar Forgebase patterns rigorosamente

**Ações**:
1. ✅ Identificar code smells (duplicação, complexidade, etc.)
2. ✅ Refatorar código
3. ✅ **RODAR TESTES** → Devem continuar passando ✅
4. ✅ Repetir até código limpo

**Exemplo (Refactoring)**:
```python
# src/forgellmclient/core/config.py (refactored)
from forgebase import EntityBase, UseCaseBase
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal
import os
import yaml

class ConfigEntity(EntityBase):
    """Config entity (Forgebase compliance)"""
    provider: str
    config_source: Literal["environment", "file", "default"]
    api_keys: dict[str, str] = {}

class ConfigService(UseCaseBase):
    """Config service with precedence: env > file > default"""

    def __init__(self, config_file: str | None = None, log_service=None):
        self.config_file = config_file
        self.log_service = log_service
        self.config = self._load_config()

    def _load_config(self) -> ConfigEntity:
        """Load config with precedence"""
        provider, source = self._resolve_provider()

        config = ConfigEntity(
            provider=provider,
            config_source=source
        )

        self._log_config_source(source)
        return config

    def _resolve_provider(self) -> tuple[str, str]:
        """Resolve provider with precedence: env > file > default"""
        # 1. Check environment
        if env_provider := os.getenv('FORGE_PROVIDER'):
            return env_provider, 'environment'

        # 2. Check file
        if file_provider := self._load_from_file():
            return file_provider, 'file'

        # 3. Default
        return 'echo', 'default'

    def _load_from_file(self) -> str | None:
        """Load provider from config file"""
        if not self.config_file or not os.path.exists(self.config_file):
            return None

        with open(self.config_file) as f:
            data = yaml.safe_load(f)
            return data.get('provider')

    def _log_config_source(self, source: str):
        """Log config source (if logger available)"""
        if self.log_service:
            self.log_service.log(f'config source: {source}')

    @property
    def provider(self) -> str:
        """Get effective provider"""
        return self.config.provider
```

**Run Tests After Refactoring**:
```bash
pytest tests/test_config.py -v
```

**Expected Result**: ✅ **ALL PASS** (tests still green)

**Refactoring Benefits**:
- ✅ Código mais limpo (extraído 3 métodos privados)
- ✅ Type hints adicionados (`str | None`, `tuple[str, str]`)
- ✅ Walrus operator (`:=`) para reduzir duplicação
- ✅ Forgebase patterns mantidos (EntityBase, UseCaseBase)

---

### Phase 5: Additional Scenarios (Iterate)

**Goal**: Implementar cenários restantes da feature (TDD cycle completo para cada)

**Cenários Restantes** (config.feature):
1. ✅ Precedência de configuração (DONE)
2. ⏳ Usar arquivo quando env não definida
3. ⏳ Erro quando credenciais ausentes
4. ⏳ Erro quando credenciais inválidas

**Para cada cenário**:
1. 🔴 **RED**: Escrever teste (deve falhar)
2. 🟢 **GREEN**: Implementar código mínimo (teste passa)
3. 🔵 **REFACTOR**: Melhorar código (testes continuam verdes)
4. 💾 **COMMIT**: Salvar estado (1 cenário = 1 micro-commit opcional, ou 1 feature = 1 commit)

**Exemplo (Cenário 3: Erro quando credenciais ausentes)**:

```python
# tests/test_config.py (adicionar novo teste)
@scenario('../specs/bdd/10_forge_core/config.feature',
          'Erro quando credenciais ausentes')
def test_config_missing_credentials():
    pass

@given('que nenhuma credencial foi fornecida')
def no_credentials(monkeypatch):
    monkeypatch.delenv('OPENAI_API_KEY', raising=False)
    monkeypatch.delenv('ANTHROPIC_API_KEY', raising=False)
    return {}

@when('inicializo o Forge com provedor "openrouter"')
def initialize_forge_openrouter(no_credentials):
    from forgellmclient.core.config import ConfigService
    service = ConfigService()
    service.set_provider('openrouter')  # Isso deve falhar
    return service

@then('recebo um erro do tipo ConfigurationError')
def check_configuration_error(initialize_forge_openrouter):
    with pytest.raises(ConfigurationError) as exc:
        initialize_forge_openrouter.validate_credentials()
    assert 'API key obrigatória' in str(exc.value)
```

**Run Test**: ❌ **RED** (ConfigurationError não existe)

**Implement**:
```python
# src/forgellmclient/core/config.py
class ConfigurationError(Exception):
    """Raised when configuration is invalid"""
    pass

class ConfigService(UseCaseBase):
    # ... (existing code)

    def validate_credentials(self):
        """Validate that required credentials are present"""
        required_keys = {
            'openai': 'OPENAI_API_KEY',
            'anthropic': 'ANTHROPIC_API_KEY',
            'openrouter': 'OPENROUTER_API_KEY',
        }

        if self.provider in required_keys:
            env_var = required_keys[self.provider]
            if not os.getenv(env_var):
                raise ConfigurationError(
                    f'API key obrigatória para provedor {self.provider}. '
                    f'Defina a variável de ambiente {env_var}.'
                )
```

**Run Test Again**: ✅ **GREEN**

---

### Phase 6: VCR.py Recording (API Tests)

**Goal**: Gravar responses reais de APIs (OpenAI, Anthropic, etc.) para replay em CI

**When to Use VCR.py**:
- ✅ Testes que chamam APIs externas (OpenAI, Anthropic, LlamaCpp, etc.)
- ✅ Testes de integração (HTTP client, provider adapters)
- ❌ Unit tests puros (sem network calls)

**Setup**:
```python
# tests/conftest.py
import pytest
import vcr

@pytest.fixture(scope='module')
def vcr_cassette():
    """VCR.py cassette fixture"""
    my_vcr = vcr.VCR(
        cassette_library_dir='tests/cassettes',
        record_mode='once',  # Grava 1x, depois replay
        match_on=['uri', 'method'],
        filter_headers=['authorization', 'api-key'],  # Redact secrets
    )
    return my_vcr
```

**Example (OpenAI Test)**:
```python
# tests/test_openai_adapter.py
import pytest
from pytest_bdd import scenario, given, when, then

@pytest.mark.vcr()  # Use VCR.py cassette
@scenario('../specs/bdd/10_forge_core/chat.feature',
          'Enviar mensagem e receber resposta')
def test_openai_chat():
    pass

@given('que o Forge está configurado com o provedor "openai"')
def openai_provider(vcr_cassette):
    with vcr_cassette.use_cassette('openai_chat.yaml'):
        from forgellmclient.adapters.openai import OpenAIAdapter
        adapter = OpenAIAdapter(api_key=os.getenv('OPENAI_API_KEY'))
        return adapter

@when('envio a mensagem "Olá"')
def send_message(openai_provider):
    response = openai_provider.chat(messages=[{'role': 'user', 'content': 'Olá'}])
    return response

@then('recebo uma resposta contendo "Olá"')
def check_response(send_message):
    assert 'Olá' in send_message.content or 'olá' in send_message.content.lower()
```

**First Run (Recording)**:
```bash
# Grava cassette (faz chamada real para OpenAI API, custa $$$)
OPENAI_API_KEY=sk-... pytest tests/test_openai_adapter.py --record-mode=new_episodes
```

**Result**: Cassette salvo em `tests/cassettes/openai_chat.yaml`

**Subsequent Runs (Replay)**:
```bash
# Replay cassette (custo $0, instantâneo)
pytest tests/test_openai_adapter.py
```

**Result**: ✅ Teste passa usando response gravado (sem chamada real)

---

### Phase 7: Commit (Save Working State)

**Goal**: Salvar feature implementada + testada

**Commit Guidelines**:
- ✅ **1 feature = 1 commit** (ex: "feat(config): Implement config.feature (F01)")
- ✅ Todos os cenários BDD passando
- ✅ VCR.py cassettes gravados (se aplicável)
- ✅ Forgebase patterns aplicados
- ✅ Código refatorado

**Commit Message Format**:
```
feat(scope): Brief description

- Feature detail 1
- Feature detail 2
- BDD scenarios: X/X passing
- VCR.py cassettes: recorded (if applicable)
- Forgebase compliance: ✅

Story Points: X
Sprint: X
Session: YYYY-MM-DD
```

**Example**:
```bash
git add src/forgellmclient/core/config.py tests/test_config.py tests/cassettes/
git commit -m "feat(config): Implement config.feature (F01) ✅

- ConfigEntity (Forgebase EntityBase)
- ConfigService (Forgebase UseCaseBase)
- Config precedence (env > file > default)
- Credential validation (per provider)
- Custom exceptions (ConfigurationError, AuthenticationError)
- BDD scenarios: 4/4 passing
- Forgebase compliance: ✅

Story Points: 3
Sprint: 1
Session: 2025-11-05"
```

---

## 🔄 Complete TDD Cycle (Summary)

```
Feature File (BDD)
    ↓
┌─────────────────────────────────┐
│ FOR EACH SCENARIO:              │
│                                 │
│  1. 🔴 RED: Write failing test  │
│     - Setup pytest-bdd steps    │
│     - Run test → FAIL ❌        │
│                                 │
│  2. 🟢 GREEN: Minimal impl      │
│     - Write minimum code        │
│     - Run test → PASS ✅        │
│                                 │
│  3. 🔵 REFACTOR: Improve        │
│     - Clean code                │
│     - Run tests → STILL PASS ✅ │
│                                 │
│  4. 📼 VCR: Record (if API)     │
│     - First run: real API call  │
│     - Save cassette             │
│     - Next runs: replay         │
│                                 │
└─────────────────────────────────┘
    ↓
💾 COMMIT: 1 feature = 1 commit
    ↓
🔄 NEXT FEATURE (repeat cycle)
```

---

## 📊 TDD Metrics

### Test Coverage Targets

| Type | Coverage Target | Speed | Cost |
|------|----------------|-------|------|
| **Unit Tests** | 80%+ | < 1s | $0 |
| **Integration Tests (VCR.py)** | 60%+ | < 5s (replay) | $0 (replay) |
| **BDD Scenarios** | 100% | < 10s | $0 (CI replay) |
| **Manual E2E** | 10% | Variable | $5/month |

**Overall Target**: 80%+ code coverage (pytest-cov)

---

## 🚨 TDD Anti-Patterns (Avoid)

### ❌ Anti-Pattern 1: Writing Implementation First
```python
# ❌ WRONG: Implement before test
def config_service():
    return ConfigService()  # Implementei sem ter teste

# Later: "Hmm, como testo isso?"
```

**✅ Correct**:
```python
# ✅ RIGHT: Test first
def test_config_service():
    service = ConfigService()  # Teste falha (não existe)
    assert service.provider == 'echo'

# Now implement to make test pass
```

---

### ❌ Anti-Pattern 2: Testing Implementation Details
```python
# ❌ WRONG: Test internal methods
def test_config_private_method():
    service = ConfigService()
    result = service._load_from_file()  # Testing private method
    assert result == 'echo'
```

**✅ Correct**:
```python
# ✅ RIGHT: Test public behavior
def test_config_loads_from_file():
    service = ConfigService(config_file='config.yaml')
    assert service.provider == 'echo'  # Test outcome, not internals
```

---

### ❌ Anti-Pattern 3: Skipping RED Phase
```python
# ❌ WRONG: Implement and test together
class ConfigService:
    def __init__(self):
        self.provider = 'echo'

def test_config():
    assert ConfigService().provider == 'echo'  # Teste nunca falhou (RED missing)
```

**✅ Correct**:
```python
# ✅ RIGHT: RED → GREEN → REFACTOR
# 1. RED: Write test first (fails - ConfigService doesn't exist)
def test_config():
    assert ConfigService().provider == 'echo'

# 2. GREEN: Implement minimal
class ConfigService:
    def __init__(self):
        self.provider = 'echo'

# 3. REFACTOR: Improve (if needed)
```

---

### ❌ Anti-Pattern 4: Too Much Code in GREEN Phase
```python
# ❌ WRONG: Over-engineering in GREEN phase
class ConfigService:
    def __init__(self):
        self.provider = 'echo'
        self.cache = {}  # YAGNI - test doesn't need this
        self.logger = Logger()  # YAGNI
        self.validators = [...]  # YAGNI
```

**✅ Correct**:
```python
# ✅ RIGHT: Minimal code to pass test
class ConfigService:
    def __init__(self):
        self.provider = 'echo'  # Just enough to pass
```

---

## 🎯 TDD Benefits (Why It Works)

### 1. Fast Feedback Loop
- ❌ **Without TDD**: Implement → Deploy → Bug found → Fix → Re-deploy (hours/days)
- ✅ **With TDD**: Test → Implement → Test passes (seconds)

### 2. Living Documentation
- Tests são **executable documentation**
- Scenario describes behavior: `test_config_precedence_env_over_file()`

### 3. Refactoring Safety
- Testes garantem que refactoring não quebra funcionalidade
- Confiança para melhorar código

### 4. Design Improvement
- TDD força **testable design** (dependency injection, interfaces)
- Resultado: Código mais modular, Forgebase-compliant

### 5. Cost Reduction (VCR.py)
- Gravar responses reais 1x ($$)
- Replay infinitas vezes em CI ($0)
- **Savings**: $95-475/month

---

## 🔁 Feedback de Descobertas Críticas para Roadmap Planning

Durante o ciclo TDD, é possível descobrir novas informações que impactam o planejamento inicial. Quando descobertas críticas são feitas, que afetam a arquitetura, estimativas ou o backlog, é fundamental que este feedback seja formalmente canalizado de volta para a fase de **Roadmap Planning**.

### Como Escalar Descobertas Críticas:

1.  **Identificação:** Durante o RED, GREEN, ou REFACTOR, se uma suposição do planejamento se mostrar falsa, uma dependência inesperada surgir, ou a estimativa original se provar inviável.
2.  **Documentação:** Registrar a descoberta, o impacto potencial e a evidência em um ADR provisório ou em uma nota no `progress.md` da sprint.
3.  **Comunicação:** Alertar o Tech Lead / Product Owner imediatamente.
4.  **Re-avaliação:** O Tech Lead / Product Owner deve acionar uma revisão do **Roadmap Planning** para:
    *   Atualizar ADRs (`specs/roadmap/adr/ADR-XXX.md`).
    *   Revisar e ajustar estimativas (`specs/roadmap/estimates.yml`).
    *   Re-priorizar tarefas ou quebrar features no `specs/roadmap/BACKLOG.md`.
    *   Convocar uma reunião para discutir e realinhar a arquitetura se necessário (HLD/LLD).

**Importante:** Não prosseguir com a implementação que contraria o planejamento aprovado sem uma revisão e ajuste formal na fase de Roadmap Planning.

---

## 📝 TDD Checklist (Per Feature)

Before marking feature as DONE:

- [ ] All BDD scenarios have pytest-bdd tests
- [ ] All tests follow RED → GREEN → REFACTOR cycle
- [ ] Test coverage ≥ 80% (pytest-cov)
- [ ] VCR.py cassettes recorded (if API tests)
- [ ] Forgebase patterns applied (EntityBase, UseCaseBase, etc.)
- [ ] Code refactored (no duplication, clear names)
- [ ] All tests pass (pytest -v)
- [ ] Committed (1 feature = 1 commit)

---

## 🔗 Related Documents

- **BACKLOG.md**: Session-based workflow (integrates TDD cycle)
- **estimates.yml**: Story points include TDD effort
- **ADR-005**: VCR.py testing strategy
- **FEATURE_BREAKDOWN.md**: Scenarios mapped to tests

---

**Last Updated**: 2025-11-05
**Status**: Ready for Sprint 1 Implementation
**Next Action**: Apply TDD workflow to F01 (config.feature)
