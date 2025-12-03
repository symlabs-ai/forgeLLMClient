# Tech Stack — ForgeLLMClient

> **Versao:** 1.0
> **Data:** 2025-12-03

---

## Python Core

| Componente | Versao | Justificativa |
|------------|--------|---------------|
| **Python** | 3.12+ | Type hints avancados, performance, LTS |

---

## Dependencias de Producao

### SDK Core

| Biblioteca | Versao | Proposito |
|------------|--------|-----------|
| **httpx** | >=0.27.0 | HTTP client async |
| **forgebase** | latest | Framework base (Clean Architecture) |

### Validacao e Tipos

| Biblioteca | Versao | Proposito |
|------------|--------|-----------|
| **typing-extensions** | >=4.0.0 | Backport de tipos |

---

## Dependencias de Desenvolvimento

### Testing

| Biblioteca | Versao | Proposito |
|------------|--------|-----------|
| **pytest** | >=8.0.0 | Framework de testes |
| **pytest-bdd** | >=7.0.0 | Suporte a Gherkin |
| **pytest-asyncio** | >=0.23.0 | Testes async |
| **pytest-cov** | >=4.0.0 | Cobertura de codigo |
| **hypothesis** | >=6.0.0 | Property-based testing |

### Qualidade de Codigo

| Biblioteca | Versao | Proposito |
|------------|--------|-----------|
| **ruff** | >=0.4.0 | Linting + formatacao |
| **mypy** | >=1.7.0 | Type checking |
| **import-linter** | >=2.0.0 | Validacao de boundaries |
| **deptry** | >=0.20.0 | Higiene de dependencias |

### Pre-commit

| Biblioteca | Versao | Proposito |
|------------|--------|-----------|
| **pre-commit** | >=3.0.0 | Git hooks |

---

## Estrutura pyproject.toml

```toml
[project]
name = "forge-llm"
version = "0.1.0"
description = "SDK Python para interface unificada com LLMs"
readme = "README.md"
requires-python = ">=3.12"
license = {text = "MIT"}
authors = [
    {name = "SymLabs", email = "contact@symlabs.ai"}
]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.12",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Scientific/Engineering :: Artificial Intelligence",
]
keywords = ["llm", "ai", "openai", "anthropic", "sdk"]

dependencies = [
    "httpx>=0.27.0",
    "forgebase @ git+https://github.com/symlabs-ai/forgebase.git",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-bdd>=7.0.0",
    "pytest-asyncio>=0.23.0",
    "pytest-cov>=4.0.0",
    "hypothesis>=6.0.0",
    "ruff>=0.4.0",
    "mypy>=1.7.0",
    "import-linter>=2.0.0",
    "deptry>=0.20.0",
    "pre-commit>=3.0.0",
]

[project.urls]
Homepage = "https://github.com/symlabs-ai/forgellmclient"
Documentation = "https://github.com/symlabs-ai/forgellmclient#readme"
Repository = "https://github.com/symlabs-ai/forgellmclient"

[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[tool.setuptools.packages.find]
where = ["src"]

[tool.setuptools.package-data]
"*" = ["py.typed"]

# ============================================================
# RUFF
# ============================================================

[tool.ruff]
line-length = 88
target-version = "py312"

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "F",   # pyflakes
    "I",   # isort
    "B",   # flake8-bugbear
    "UP",  # pyupgrade
    "C4",  # flake8-comprehensions
    "SIM", # flake8-simplify
    "RET", # flake8-return
    "N",   # pep8-naming
]
ignore = [
    "E203", # whitespace before ':'
    "E501", # line too long (handled by formatter)
]

[tool.ruff.lint.per-file-ignores]
"tests/**" = ["E402", "F401"]
"src/forge_llm/**/__init__.py" = ["F401", "F403"]

# ============================================================
# MYPY
# ============================================================

[tool.mypy]
python_version = "3.12"
strict = true
warn_return_any = true
warn_unused_ignores = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
no_implicit_optional = true

[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false

# ============================================================
# PYTEST
# ============================================================

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
python_classes = "Test*"
python_functions = "test_*"
asyncio_mode = "auto"
markers = [
    "ci_fast: Testes rapidos (mocks)",
    "ci_int: Testes de integracao",
    "slow: Testes lentos",
    "sdk: Forge SDK",
    "provider: Provedores especificos",
    "openai: Provedor OpenAI",
    "anthropic: Provedor Anthropic",
    "streaming: Testes de streaming",
    "tools: Testes de tool calling",
]
addopts = "-v --tb=short"
filterwarnings = [
    "ignore::DeprecationWarning",
    "ignore::PendingDeprecationWarning",
]

# ============================================================
# COVERAGE
# ============================================================

[tool.coverage.run]
source = ["src/forge_llm"]
branch = true
omit = ["*/tests/*", "*/__init__.py"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise NotImplementedError",
    "if TYPE_CHECKING:",
    "if __name__ == .__main__.:",
]
fail_under = 80

# ============================================================
# IMPORT LINTER
# ============================================================

[tool.importlinter]
root_package = "forge_llm"

[[tool.importlinter.contracts]]
name = "Domain cannot import application or infrastructure"
type = "forbidden"
source_modules = ["forge_llm.domain"]
forbidden_modules = [
    "forge_llm.application",
    "forge_llm.infrastructure",
    "forge_llm.adapters",
    "forge_llm.providers",
]

[[tool.importlinter.contracts]]
name = "Application cannot import infrastructure or adapters"
type = "forbidden"
source_modules = ["forge_llm.application"]
forbidden_modules = [
    "forge_llm.infrastructure",
    "forge_llm.adapters",
]
```

---

## Ferramentas de Desenvolvimento

### Scripts Uteis

```bash
# Instalar projeto em modo editavel
pip install -e ".[dev]"

# Rodar testes
pytest

# Rodar testes rapidos (mocks)
pytest -m "ci_fast"

# Rodar testes de integracao
pytest -m "ci_int"

# Verificar lint
ruff check src/

# Formatar codigo
ruff format src/

# Verificar tipos
mypy src/

# Verificar boundaries
lint-imports

# Verificar dependencias
deptry src/

# Suite completa de qualidade
ruff check src/ && ruff format --check src/ && mypy src/ && lint-imports && pytest
```

---

## Estrutura de Testes

```
tests/
├── __init__.py
├── conftest.py              # Fixtures globais
├── unit/                    # Testes unitarios
│   ├── domain/
│   │   ├── test_entities.py
│   │   └── test_value_objects.py
│   ├── application/
│   │   └── test_usecases.py
│   └── providers/
│       ├── test_openai.py
│       ├── test_anthropic.py
│       └── test_mock.py
├── integration/             # Testes de integracao
│   └── providers/
│       ├── test_openai_real.py
│       └── test_anthropic_real.py
└── bdd/                     # Testes BDD
    ├── conftest.py
    ├── test_chat_steps.py
    └── test_tools_steps.py
```

---

## Referencias

- `specs/roadmap/ARCHITECTURAL_DECISIONS_APPROVED.md`
- `specs/roadmap/ADR.md`
- `temp/requirements-dev.txt`

---

*Documento gerado pelo Roadmap Planning Process*
