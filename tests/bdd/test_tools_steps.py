"""
Step definitions para tools.feature.

BDD: Forge tool calling pendente de implementacao.
"""

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

# Marcar todos os testes como skip ate implementacao
pytestmark = pytest.mark.skip("BDD: Forge tool calling pendente de implementacao")

# Vincular feature
scenarios("../../specs/bdd/10_forge_core/tools.feature")


# ============================================================
# GIVEN STEPS
# ============================================================


@given(parsers.parse('que a ferramenta "{tool_name}" esta registrada'))
def tool_registered(context, tool_name):
    """Registra ferramenta no cliente."""
    # TODO: Implementar
    # context["client"].register_tool(name=tool_name, ...)
    if "tools" not in context:
        context["tools"] = []
    context["tools"].append(tool_name)


@given(parsers.parse('recebi um tool_call com id "{tc_id}" para "{tool_name}"'))
def received_tool_call(context, tc_id, tool_name):
    """Simula recebimento de tool_call."""
    context["pending_tool_call"] = {
        "id": tc_id,
        "name": tool_name,
    }


@given(parsers.parse('as ferramentas "{tool1}" e "{tool2}" estao registradas'))
def multiple_tools_registered(context, tool1, tool2):
    """Registra multiplas ferramentas."""
    context["tools"] = [tool1, tool2]


# ============================================================
# WHEN STEPS
# ============================================================


@when(parsers.parse('registro a ferramenta "{tool_name}" com descricao "{description}"'))
def register_tool(context, tool_name, description):
    """Registra ferramenta com descricao."""
    # TODO: Implementar
    # context["client"].register_tool(name=tool_name, description=description)
    if "tools" not in context:
        context["tools"] = []
    context["tools"].append({"name": tool_name, "description": description})


@when(parsers.parse('envio o resultado "{result}" para o tool_call "{tc_id}"'))
def send_tool_result(context, result, tc_id):
    """Envia resultado de tool call."""
    # TODO: Implementar
    # response = context["client"].submit_tool_result(tc_id, result)
    # context["response"] = response
    context["tool_result"] = {"id": tc_id, "result": result}


@when("tento registrar uma ferramenta sem nome")
def try_register_tool_without_name(context):
    """Tenta registrar ferramenta sem nome."""
    # TODO: Implementar
    # try:
    #     context["client"].register_tool(name="", description="test")
    # except Exception as e:
    #     context["error"] = e
    pass


@when(parsers.parse('tento enviar resultado para tool_call "{tc_id}"'))
def try_send_result_invalid_tc(context, tc_id):
    """Tenta enviar resultado para tool_call inexistente."""
    # TODO: Implementar
    # try:
    #     context["client"].submit_tool_result(tc_id, "result")
    # except Exception as e:
    #     context["error"] = e
    pass


# ============================================================
# THEN STEPS
# ============================================================


@then(parsers.parse("o cliente tem {count:d} ferramentas registradas"))
def check_tool_count(context, count):
    """Verifica quantidade de ferramentas."""
    # TODO: Implementar
    # assert len(context["client"].tools) == count
    pass


@then(parsers.parse('a ferramenta "{tool_name}" esta disponivel'))
def check_tool_available(context, tool_name):
    """Verifica ferramenta disponivel."""
    # TODO: Implementar
    # assert tool_name in [t.name for t in context["client"].tools]
    pass


@then("recebo uma resposta com tool_call")
def check_response_has_tool_call(context):
    """Verifica que resposta tem tool_call."""
    # TODO: Implementar
    # assert context["response"].tool_calls is not None
    # assert len(context["response"].tool_calls) > 0
    pass


@then(parsers.parse('o tool_call tem nome "{name}"'))
def check_tool_call_name(context, name):
    """Verifica nome do tool_call."""
    # TODO: Implementar
    # assert context["response"].tool_calls[0].name == name
    pass


@then("o tool_call tem argumentos em formato JSON")
def check_tool_call_args(context):
    """Verifica argumentos do tool_call."""
    # TODO: Implementar
    # args = context["response"].tool_calls[0].arguments
    # assert isinstance(args, dict)
    pass


@then("o tool_call tem um id unico")
def check_tool_call_id(context):
    """Verifica id do tool_call."""
    # TODO: Implementar
    # assert context["response"].tool_calls[0].id is not None
    pass


@then("recebo uma resposta final do LLM")
def check_final_llm_response(context):
    """Verifica resposta final."""
    # TODO: Implementar
    # assert context["response"].content is not None
    pass


@then("a resposta incorpora o resultado da ferramenta")
def check_tool_result_incorporated(context):
    """Verifica que resultado foi incorporado."""
    # TODO: Implementar
    pass


@then("recebo uma resposta com multiplos tool_calls")
def check_multiple_tool_calls(context):
    """Verifica multiplos tool_calls."""
    # TODO: Implementar
    # assert len(context["response"].tool_calls) > 1
    pass


@then(parsers.parse('existe tool_call para "{tool_name}"'))
def check_tool_call_exists(context, tool_name):
    """Verifica que tool_call existe para ferramenta."""
    # TODO: Implementar
    # names = [tc.name for tc in context["response"].tool_calls]
    # assert tool_name in names
    pass
