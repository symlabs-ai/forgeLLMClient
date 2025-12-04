"""Configuração para testes de integração."""

import os
from pathlib import Path

import pytest

# Carregar .env se existir
_env_file = Path(__file__).parent.parent.parent / ".env"
if _env_file.exists():
    with open(_env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                # Remove \r se existir (Windows line endings)
                value = value.strip().rstrip("\r")
                os.environ[key] = value


def get_openai_api_key() -> str | None:
    """Obter API key do OpenAI do ambiente."""
    key = os.environ.get("OPENAI_API_KEY")
    if key:
        return key.strip().rstrip("\r")
    return None


def get_anthropic_api_key() -> str | None:
    """Obter API key do Anthropic do ambiente."""
    key = os.environ.get("ANTHROPIC_API_KEY")
    if key:
        return key.strip().rstrip("\r")
    return None


# Fixtures para API keys
@pytest.fixture
def openai_api_key() -> str:
    """Fixture que retorna a API key do OpenAI."""
    key = get_openai_api_key()
    if not key:
        pytest.skip("OPENAI_API_KEY não disponível")
    return key


@pytest.fixture
def anthropic_api_key() -> str:
    """Fixture que retorna a API key do Anthropic."""
    key = get_anthropic_api_key()
    if not key:
        pytest.skip("ANTHROPIC_API_KEY não disponível")
    return key


# Fixtures para modelos configuraveis via ambiente
@pytest.fixture
def openai_model() -> str:
    """Fixture que retorna o modelo OpenAI a usar nos testes."""
    return os.environ.get("OPENAI_TEST_MODEL", "gpt-4o-mini")


@pytest.fixture
def anthropic_model() -> str:
    """Fixture que retorna o modelo Anthropic a usar nos testes."""
    return os.environ.get("ANTHROPIC_TEST_MODEL", "claude-sonnet-4-20250514")


# Skip conditions
has_openai_key = pytest.mark.skipif(
    get_openai_api_key() is None,
    reason="OPENAI_API_KEY não disponível",
)

has_anthropic_key = pytest.mark.skipif(
    get_anthropic_api_key() is None,
    reason="ANTHROPIC_API_KEY não disponível",
)

# Timeout para testes de integracao (60 segundos por teste)
integration_timeout = pytest.mark.timeout(60)
