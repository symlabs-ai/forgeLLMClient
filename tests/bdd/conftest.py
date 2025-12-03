"""
Configuracao pytest-bdd para ForgeLLMClient.

Este arquivo contem fixtures compartilhadas entre todos os testes BDD.
"""

from typing import Any

import pytest

# ============================================================
# FIXTURES DE CONTEXTO
# ============================================================


@pytest.fixture
def context() -> dict[str, Any]:
    """Contexto compartilhado entre steps de um cenario."""
    return {}


@pytest.fixture
def responses() -> dict[str, Any]:
    """Armazena respostas para comparacao entre cenarios."""
    return {}


# ============================================================
# FIXTURES DE CONFIGURACAO
# ============================================================


@pytest.fixture
def forge_config() -> dict[str, Any]:
    """Configuracao padrao do Forge para testes."""
    return {
        "provider": "mock",
        "timeout": 30,
        "temperature": 0.7,
    }


@pytest.fixture
def mock_provider_config() -> dict[str, Any]:
    """Configuracao do provider mock para testes rapidos."""
    return {
        "provider": "mock",
        "responses": {
            "default": "Mock response",
            "echo": lambda msg: f"Echo: {msg}",
        },
    }


# ============================================================
# FIXTURES DE CLIENTE (SKELETON)
# ============================================================


@pytest.fixture
def forge_client(forge_config):
    """
    Cliente ForgeLLMClient configurado para testes.

    TODO: Implementar quando o cliente existir.
    """
    pytest.skip("Aguardando implementacao do ForgeLLMClient")
    # from forgellmclient import Client
    # return Client(**forge_config)


@pytest.fixture
def forge_client_unconfigured():
    """
    Cliente ForgeLLMClient sem provedor configurado.

    TODO: Implementar quando o cliente existir.
    """
    pytest.skip("Aguardando implementacao do ForgeLLMClient")
    # from forgellmclient import Client
    # return Client()


# ============================================================
# FIXTURES DE FERRAMENTAS (TOOLS)
# ============================================================


@pytest.fixture
def sample_tools() -> list[dict[str, Any]]:
    """Ferramentas de exemplo para testes de tool calling."""
    return [
        {
            "name": "calculadora",
            "description": "Faz calculos matematicos",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "Expressao matematica"},
                },
                "required": ["expression"],
            },
        },
        {
            "name": "clima",
            "description": "Consulta previsao do tempo",
            "parameters": {
                "type": "object",
                "properties": {
                    "cidade": {"type": "string", "description": "Nome da cidade"},
                },
                "required": ["cidade"],
            },
        },
    ]


@pytest.fixture
def weather_tool() -> dict[str, Any]:
    """Ferramenta get_weather para testes."""
    return {
        "name": "get_weather",
        "description": "Consulta clima de uma cidade",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "Nome da cidade"},
            },
            "required": ["city"],
        },
    }


# ============================================================
# MARKERS CUSTOMIZADOS
# ============================================================


def pytest_configure(config):
    """Registra markers customizados."""
    config.addinivalue_line("markers", "ci_fast: Testes rapidos (mocks)")
    config.addinivalue_line("markers", "ci_int: Testes de integracao")
    config.addinivalue_line("markers", "slow: Testes lentos")
    config.addinivalue_line("markers", "sdk: Forge SDK")
    config.addinivalue_line("markers", "provider: Provedores especificos")
    config.addinivalue_line("markers", "openai: Provedor OpenAI")
    config.addinivalue_line("markers", "anthropic: Provedor Anthropic")
    config.addinivalue_line("markers", "streaming: Testes de streaming")
    config.addinivalue_line("markers", "tools: Testes de tool calling")
