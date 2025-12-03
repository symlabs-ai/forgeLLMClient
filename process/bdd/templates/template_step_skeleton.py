# Template: Step Definition Skeleton
# Para criar step definitions vazias (pytest-bdd)

"""
Template de step definition para pytest-bdd.

Uso:
1. Copiar este template para tests/bdd/
2. Renomear para test_[nome_feature]_steps.py
3. Atualizar path da feature em scenarios()
4. Criar step definitions para cada DADO/QUANDO/ENTÃO
5. Inicialmente, deixar tudo com pytest.skip()
"""

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

# ===========================
# IMPORTANTE: Marcar como skip até implementação
# ===========================
pytestmark = pytest.mark.skip("BDD ([nome da feature]) pendente de implementação")

# ===========================
# Vincular feature Gherkin
# ===========================
# Ajustar o caminho relativo para a feature correspondente
scenarios("../../specs/bdd/[prefixo]_[dominio]/[nome].feature")

# ===========================
# FIXTURES ESPECÍFICAS (se necessário)
# ===========================

@pytest.fixture
def custom_fixture():
    """
    Fixture específica para esta feature.
    TODO: Implementar quando necessário.
    """
    return {}

# ===========================
# STEP DEFINITIONS
# ===========================
# Padrões:
# - @given: Pré-condição (contexto inicial)
# - @when: Ação executada
# - @then: Resultado esperado
# - target_fixture="nome": Retorna valor para uso em steps seguintes

# ----------------------------
# GIVEN Steps
# ----------------------------

@given('[step text exato da feature]', target_fixture="nome_fixture")
def step_given_contexto():
    """
    TODO (TDD): Implementar configuração de contexto.

    Quando implementar:
    1. Remover pytest.mark.skip do topo do arquivo
    2. Importar módulos necessários
    3. Retornar objeto/valor para uso nos próximos steps

    Exemplo:
        from forge import ForgeClient
        return ForgeClient(provider="echo")
    """
    pytest.skip("Aguardando implementação (TDD)")

@given(parsers.parse('[step com "{parametro}"]'), target_fixture="resultado")
def step_given_parametrizado(parametro):
    """
    TODO (TDD): Implementar step com parâmetro.

    Args:
        parametro: Valor capturado do step Gherkin

    Quando implementar:
        # Usar o parâmetro
        config = {"provider": parametro}
        return config
    """
    pytest.skip("Aguardando implementação (TDD)")

# ----------------------------
# WHEN Steps
# ----------------------------

@when('[step text exato da feature]', target_fixture="response")
def step_when_acao(nome_fixture):
    """
    TODO (TDD): Implementar ação.

    Args:
        nome_fixture: Resultado do step GIVEN anterior

    Quando implementar:
        return nome_fixture.execute_action()
    """
    pytest.skip("Aguardando implementação (TDD)")

@when(parsers.parse('[step com "{parametro}"]'))
def step_when_parametrizado(nome_fixture, parametro, context):
    """
    TODO (TDD): Implementar ação parametrizada.

    Args:
        nome_fixture: Fixture de contexto
        parametro: Valor capturado
        context: Dicionário compartilhado (fixture do conftest.py)

    Quando implementar:
        result = nome_fixture.action(parametro)
        context['last_result'] = result
    """
    pytest.skip("Aguardando implementação (TDD)")

# ----------------------------
# THEN Steps
# ----------------------------

@then('[step text exato da feature]')
def step_then_validacao(response):
    """
    TODO (TDD): Implementar validação de resultado.

    Args:
        response: Resultado do step WHEN

    Quando implementar:
        assert response is not None
        assert response.status == "success"
    """
    pytest.skip("Aguardando implementação (TDD)")

@then(parsers.parse('[step com "{texto_esperado}"]'))
def step_then_parametrizada(response, texto_esperado):
    """
    TODO (TDD): Implementar validação parametrizada.

    Args:
        response: Resultado anterior
        texto_esperado: Valor esperado capturado do step

    Quando implementar:
        assert texto_esperado in response.content
    """
    pytest.skip("Aguardando implementação (TDD)")

# ----------------------------
# E (AND) Steps
# ----------------------------
# Steps com "E" reutilizam definições de DADO/QUANDO/ENTÃO
# Não é necessário criar @given/@when/@then duplicados

# ===========================
# EXEMPLO COMPLETO
# ===========================

"""
Feature Gherkin:

@sdk @ci-fast
FUNCIONALIDADE: Chat básico
  CENÁRIO: Enviar mensagem simples
    DADO que o Forge está configurado com o provedor "echo"
    QUANDO envio a mensagem "Olá"
    ENTÃO recebo uma resposta contendo "Olá"

Step definitions correspondentes:

@given('que o Forge está configurado com o provedor "echo"', target_fixture="forge_client")
def forge_with_echo():
    from forge import ForgeClient
    return ForgeClient(provider="echo")

@when(parsers.parse('envio a mensagem "{message}"'), target_fixture="response")
def send_message(forge_client, message):
    return forge_client.chat(message)

@then(parsers.parse('recebo uma resposta contendo "{text}"'))
def check_response_contains(response, text):
    assert text in response.content
"""

# ===========================
# EXECUTAR TESTE
# ===========================

"""
# Coletar testes (sem executar):
$ pytest --collect-only tests/bdd/test_[nome]_steps.py

# Executar (todos skipped inicialmente):
$ pytest tests/bdd/test_[nome]_steps.py -v

# Quando implementar (remover pytestmark.skip):
$ pytest tests/bdd/test_[nome]_steps.py -v
# Resultado: FAIL (Red) → implementar código → PASS (Green)
"""
