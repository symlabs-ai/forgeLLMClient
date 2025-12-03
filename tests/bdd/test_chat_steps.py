"""
Step definitions para chat.feature.

BDD: Forge chat basico pendente de implementacao.
"""

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

# Marcar todos os testes como skip ate implementacao
pytestmark = pytest.mark.skip("BDD: Forge chat pendente de implementacao")

# Vincular feature
scenarios("../../specs/bdd/10_forge_core/chat.feature")


# ============================================================
# GIVEN STEPS
# ============================================================


@given("que o ForgeLLMClient esta instalado")
def forge_installed():
    """Verifica que o ForgeLLMClient esta instalado."""
    # TODO: Implementar verificacao
    pass


@given("o ambiente de teste esta configurado")
def test_env_configured():
    """Configura ambiente de teste."""
    # TODO: Implementar configuracao
    pass


@given(parsers.parse('que o cliente esta configurado com o provedor "{provider}"'))
def client_with_provider(context, provider):
    """Configura cliente com provedor especificado."""
    # TODO: Implementar
    # from forgellmclient import Client
    # context["client"] = Client(provider=provider)
    context["provider"] = provider


@given("que o cliente NAO esta configurado com nenhum provedor")
def client_unconfigured(context):
    """Cliente sem provedor configurado."""
    # TODO: Implementar
    # from forgellmclient import Client
    # context["client"] = Client()
    context["client"] = None


@given(parsers.parse("o timeout esta configurado para {seconds:d} segundo"))
def timeout_configured(context, seconds):
    """Configura timeout."""
    context["timeout"] = seconds


# ============================================================
# WHEN STEPS
# ============================================================


@when(parsers.parse('envio a mensagem "{message}"'))
def send_message(context, message):
    """Envia mensagem ao LLM."""
    # TODO: Implementar
    # response = context["client"].chat(message)
    # context["response"] = response
    context["message"] = message


@when(parsers.parse('envio a mensagem "{message}" com temperatura {temp:f}'))
def send_message_with_temp(context, message, temp):
    """Envia mensagem com temperatura especificada."""
    # TODO: Implementar
    # response = context["client"].chat(message, temperature=temp)
    # context["response"] = response
    context["message"] = message
    context["temperature"] = temp


@when(parsers.parse('envio a mensagem "{message}" com streaming habilitado'))
def send_message_streaming(context, message):
    """Envia mensagem com streaming."""
    # TODO: Implementar
    # chunks = list(context["client"].chat(message, stream=True))
    # context["chunks"] = chunks
    context["message"] = message
    context["streaming"] = True


@when("tento enviar uma mensagem")
def try_send_message(context):
    """Tenta enviar mensagem (esperando erro)."""
    # TODO: Implementar
    # try:
    #     context["client"].chat("test")
    # except Exception as e:
    #     context["error"] = e
    pass


@when("envio uma mensagem vazia")
def send_empty_message(context):
    """Envia mensagem vazia."""
    # TODO: Implementar
    # try:
    #     context["client"].chat("")
    # except Exception as e:
    #     context["error"] = e
    context["message"] = ""


# ============================================================
# THEN STEPS
# ============================================================


@then(parsers.parse('recebo uma resposta com status "{status}"'))
def check_response_status(context, status):
    """Verifica status da resposta."""
    # TODO: Implementar
    # assert context["response"].status == status
    pass


@then("a resposta contem texto nao vazio")
def check_response_has_text(context):
    """Verifica que resposta tem texto."""
    # TODO: Implementar
    # assert context["response"].content
    # assert len(context["response"].content) > 0
    pass


@then("a resposta tem formato ChatResponse valido")
def check_response_format(context):
    """Verifica formato da resposta."""
    # TODO: Implementar
    # from forgellmclient.types import ChatResponse
    # assert isinstance(context["response"], ChatResponse)
    pass


@then("recebo chunks de resposta progressivamente")
def check_streaming_chunks(context):
    """Verifica chunks de streaming."""
    # TODO: Implementar
    # assert len(context["chunks"]) > 1
    pass


@then("o ultimo chunk indica fim do stream")
def check_last_chunk(context):
    """Verifica ultimo chunk."""
    # TODO: Implementar
    # assert context["chunks"][-1].finish_reason is not None
    pass


@then("a resposta final esta completa")
def check_final_response(context):
    """Verifica resposta final."""
    # TODO: Implementar
    pass


@then(parsers.parse('recebo um erro do tipo "{error_type}"'))
def check_error_type(context, error_type):
    """Verifica tipo do erro."""
    # TODO: Implementar
    # assert context["error"].__class__.__name__ == error_type
    pass


@then(parsers.parse('a mensagem de erro contem "{text}"'))
def check_error_message(context, text):
    """Verifica mensagem de erro."""
    # TODO: Implementar
    # assert text.lower() in str(context["error"]).lower()
    pass
