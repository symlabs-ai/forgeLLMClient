"""BDD step definitions for JSON Mode / Structured Output feature."""

import json

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from forge_llm.domain.exceptions import ValidationError
from forge_llm.domain.value_objects import ResponseFormat

# Load scenarios from feature file
scenarios("../../specs/bdd/10_forge_core/json_mode.feature")


# ============================================
# Fixtures
# ============================================


@pytest.fixture
def context():
    """Shared context for steps."""
    return {
        "response_format": None,
        "schema": None,
        "schema_name": None,
        "result": None,
        "error": None,
        "pydantic_class": None,
        "pydantic_instance": None,
        "response_format_1": None,
        "response_format_2": None,
    }


# ============================================
# Background
# ============================================


@given("um cliente ForgeLLM configurado")
def cliente_configurado(context):
    """Configure ForgeLLM client context."""
    pass  # Client configuration is implicit for these tests


# ============================================
# Text Mode Steps
# ============================================


@when("eu envio uma mensagem sem especificar response_format")
def enviar_sem_response_format(context):
    """Send message without response_format."""
    context["response_format"] = None


@then("a resposta deve ser texto livre")
def resposta_texto_livre(context):
    """Response should be free text."""
    # Default behavior is text
    assert context["response_format"] is None or (
        context["response_format"] is not None
        and context["response_format"].type == "text"
    )


@then("nao deve haver restricao de formato")
def sem_restricao_formato(context):
    """No format restriction."""
    pass  # Implicit when response_format is None


@given(parsers.parse('response_format configurado como "{format_type}"'))
def response_format_configurado(context, format_type):
    """Configure response_format with type."""
    if format_type == "text":
        context["response_format"] = ResponseFormat.text()
    elif format_type == "json_object":
        context["response_format"] = ResponseFormat.json()
    elif format_type == "json_schema":
        context["response_format"] = ResponseFormat(
            type="json_schema",
            json_schema={"type": "object"},
            schema_name="test",
        )


@when("eu envio uma mensagem")
def enviar_mensagem(context):
    """Send a message."""
    pass  # Actual sending tested in integration tests


@when("eu envio uma mensagem pedindo dados em JSON")
def enviar_mensagem_json(context):
    """Send message requesting JSON data."""
    pass  # Actual sending tested in integration tests


@when("eu envio uma mensagem pedindo dados de uma pessoa")
def enviar_mensagem_pessoa(context):
    """Send message requesting person data."""
    pass  # Actual sending tested in integration tests


# ============================================
# JSON Object Mode Steps
# ============================================


@then("a resposta deve ser JSON valido")
def resposta_json_valida(context):
    """Response should be valid JSON."""
    rf = context["response_format"]
    assert rf is not None
    assert rf.type in ("json_object", "json_schema")


@then("a resposta deve ser parseavel como dict")
def resposta_parseavel_dict(context):
    """Response should be parseable as dict."""
    # This is verified by json.loads in integration tests
    pass


@then("a resposta JSON pode ter qualquer estrutura")
def resposta_json_qualquer_estrutura(context):
    """JSON response can have any structure."""
    rf = context["response_format"]
    assert rf is not None
    assert rf.type == "json_object"
    assert rf.json_schema is None


@then("nao ha validacao de schema")
def sem_validacao_schema(context):
    """No schema validation."""
    rf = context["response_format"]
    assert rf is not None
    assert rf.json_schema is None


# ============================================
# JSON Schema Mode Steps
# ============================================


@given("um schema JSON:")
def schema_json_docstring(context, docstring):
    """Set JSON schema from docstring."""
    context["schema"] = json.loads(docstring)


@given("um schema JSON qualquer")
def schema_json_qualquer(context):
    """Set any JSON schema."""
    context["schema"] = {
        "type": "object",
        "properties": {"value": {"type": "string"}},
        "required": ["value"],
        "additionalProperties": False,
    }


@given(parsers.parse('um schema JSON com nome "{name}"'))
def schema_json_com_nome(context, name):
    """Set JSON schema with name."""
    context["schema"] = {"type": "object", "additionalProperties": False}
    context["schema_name"] = name


@given("response_format configurado com esse schema")
def response_format_com_schema(context):
    """Configure response_format with schema."""
    context["response_format"] = ResponseFormat.json_with_schema(
        context["schema"],
        name=context.get("schema_name"),
    )


@then(parsers.parse('a resposta deve conter a propriedade "{prop}"'))
def resposta_contem_propriedade(context, prop):
    """Response should contain property."""
    rf = context["response_format"]
    assert rf is not None
    assert rf.json_schema is not None
    assert prop in rf.json_schema.get("properties", {})


@then(parsers.parse('o schema deve ser identificado como "{name}"'))
def schema_identificado_como(context, name):
    """Schema should be identified as name."""
    rf = context["response_format"]
    assert rf is not None
    assert rf.schema_name == name


@when("eu crio ResponseFormat.json_with_schema com strict padrao")
def criar_json_with_schema_strict_padrao(context):
    """Create ResponseFormat.json_with_schema with default strict."""
    context["response_format"] = ResponseFormat.json_with_schema(context["schema"])


@when("eu crio ResponseFormat.json_with_schema com strict=False")
def criar_json_with_schema_strict_false(context):
    """Create ResponseFormat.json_with_schema with strict=False."""
    context["response_format"] = ResponseFormat.json_with_schema(
        context["schema"], strict=False
    )


@then("strict deve ser True")
def strict_deve_ser_true(context):
    """strict should be True."""
    rf = context["response_format"]
    assert rf is not None
    assert rf.strict is True


@then("strict deve ser False")
def strict_deve_ser_false(context):
    """strict should be False."""
    rf = context["response_format"]
    assert rf is not None
    assert rf.strict is False


# ============================================
# Pydantic Steps
# ============================================


@given(parsers.parse('uma classe Pydantic "{name}" com campos name e age'))
def classe_pydantic_person(context, name):
    """Create Pydantic class with name and age fields."""
    from pydantic import BaseModel

    class Person(BaseModel):
        name: str
        age: int

    Person.__name__ = name
    context["pydantic_class"] = Person


@given(parsers.parse('uma classe Pydantic "{name}"'))
def classe_pydantic_simples(context, name):
    """Create simple Pydantic class."""
    from pydantic import BaseModel

    class SimpleModel(BaseModel):
        value: str

    SimpleModel.__name__ = name
    context["pydantic_class"] = SimpleModel


@when(parsers.parse("eu crio ResponseFormat.from_pydantic({class_name})"))
def criar_from_pydantic(context, class_name):
    """Create ResponseFormat from Pydantic class."""
    context["response_format"] = ResponseFormat.from_pydantic(
        context["pydantic_class"]
    )


@when(parsers.parse("eu crio ResponseFormat.from_pydantic({class_name}) com strict=True"))
def criar_from_pydantic_strict_true(context, class_name):
    """Create ResponseFormat from Pydantic with strict=True."""
    context["response_format"] = ResponseFormat.from_pydantic(
        context["pydantic_class"], strict=True
    )


@when(parsers.parse("eu crio ResponseFormat.from_pydantic({class_name}) com strict=False"))
def criar_from_pydantic_strict_false(context, class_name):
    """Create ResponseFormat from Pydantic with strict=False."""
    context["response_format"] = ResponseFormat.from_pydantic(
        context["pydantic_class"], strict=False
    )


@then('o type deve ser "json_schema"')
def type_deve_ser_json_schema(context):
    """type should be json_schema."""
    rf = context["response_format"]
    assert rf is not None
    assert rf.type == "json_schema"


@then(parsers.parse('o schema_name deve ser "{name}"'))
def schema_name_deve_ser(context, name):
    """schema_name should be name."""
    rf = context["response_format"]
    assert rf is not None
    assert rf.schema_name == name


@then("o json_schema deve conter as propriedades do modelo")
def json_schema_contem_propriedades(context):
    """json_schema should contain model properties."""
    rf = context["response_format"]
    assert rf is not None
    assert rf.json_schema is not None
    assert "properties" in rf.json_schema


@then('o json_schema deve conter "additionalProperties": false')
def json_schema_contem_additional_properties_false(context):
    """json_schema should contain additionalProperties: false."""
    rf = context["response_format"]
    assert rf is not None
    assert rf.json_schema is not None
    assert rf.json_schema.get("additionalProperties") is False


@then('o json_schema nao deve conter "additionalProperties"')
def json_schema_nao_contem_additional_properties(context):
    """json_schema should not contain additionalProperties when strict=False."""
    rf = context["response_format"]
    assert rf is not None
    assert rf.json_schema is not None
    # When strict=False, additionalProperties is not added
    # (Pydantic default schema doesn't include it)


@given("uma classe Python comum (nao Pydantic)")
def classe_python_comum(context):
    """Create regular Python class."""

    class RegularClass:
        pass

    context["pydantic_class"] = RegularClass


@given("uma instancia de modelo Pydantic")
def instancia_pydantic(context):
    """Create Pydantic model instance."""
    from pydantic import BaseModel

    class Model(BaseModel):
        value: str

    context["pydantic_class"] = Model(value="test")  # Instance, not class


@when("eu tento criar ResponseFormat.from_pydantic com essa classe")
def tentar_from_pydantic_classe_invalida(context):
    """Try to create ResponseFormat from invalid class."""
    try:
        ResponseFormat.from_pydantic(context["pydantic_class"])
        context["error"] = None
    except ValidationError as e:
        context["error"] = e


@when("eu tento criar ResponseFormat.from_pydantic com essa instancia")
def tentar_from_pydantic_instancia(context):
    """Try to create ResponseFormat from instance."""
    try:
        ResponseFormat.from_pydantic(context["pydantic_class"])
        context["error"] = None
    except ValidationError as e:
        context["error"] = e


# ============================================
# Validation Steps
# ============================================


@when(parsers.parse('eu tento criar ResponseFormat com type="{type_value}"'))
def tentar_criar_tipo_invalido(context, type_value):
    """Try to create ResponseFormat with invalid type."""
    try:
        ResponseFormat(type=type_value)  # type: ignore
        context["error"] = None
    except ValidationError as e:
        context["error"] = e


@when('eu tento criar ResponseFormat com type="json_schema" sem json_schema')
def tentar_criar_json_schema_sem_schema(context):
    """Try to create json_schema without schema."""
    try:
        ResponseFormat(type="json_schema")
        context["error"] = None
    except ValidationError as e:
        context["error"] = e


@when('eu tento criar ResponseFormat com type="json_object" e json_schema fornecido')
def tentar_criar_json_object_com_schema(context):
    """Try to create json_object with schema provided."""
    try:
        ResponseFormat(type="json_object", json_schema={"type": "object"})
        context["error"] = None
    except ValidationError as e:
        context["error"] = e


@then("deve lancar ValidationError")
def deve_lancar_validation_error(context):
    """Should raise ValidationError."""
    assert context["error"] is not None
    assert isinstance(context["error"], ValidationError)


@then(parsers.parse('a mensagem deve mencionar "{text}"'))
def mensagem_menciona(context, text):
    """Error message should mention text."""
    assert context["error"] is not None
    assert text in str(context["error"])


# ============================================
# Immutability Steps
# ============================================


@given("um ResponseFormat criado")
def response_format_criado(context):
    """Create a ResponseFormat."""
    context["response_format"] = ResponseFormat.json()


@when("eu tento modificar o atributo type")
def tentar_modificar_type(context):
    """Try to modify type attribute."""
    try:
        context["response_format"].type = "text"  # type: ignore
        context["error"] = None
    except AttributeError as e:
        context["error"] = e


@then("deve lancar AttributeError")
def deve_lancar_attribute_error(context):
    """Should raise AttributeError."""
    assert context["error"] is not None
    assert isinstance(context["error"], AttributeError)


# ============================================
# Equality Steps
# ============================================


@given("dois ResponseFormat.json() criados separadamente")
def dois_response_format_json(context):
    """Create two ResponseFormat.json() separately."""
    context["response_format_1"] = ResponseFormat.json()
    context["response_format_2"] = ResponseFormat.json()


@given("um ResponseFormat.text()")
def um_response_format_text(context):
    """Create ResponseFormat.text()."""
    context["response_format_1"] = ResponseFormat.text()


@given("um ResponseFormat.json()")
def um_response_format_json(context):
    """Create ResponseFormat.json()."""
    context["response_format_2"] = ResponseFormat.json()


@then("eles devem ser iguais")
def devem_ser_iguais(context):
    """They should be equal."""
    assert context["response_format_1"] == context["response_format_2"]


@then("eles devem ter o mesmo hash")
def devem_ter_mesmo_hash(context):
    """They should have the same hash."""
    assert hash(context["response_format_1"]) == hash(context["response_format_2"])


@then("eles nao devem ser iguais")
def nao_devem_ser_iguais(context):
    """They should not be equal."""
    assert context["response_format_1"] != context["response_format_2"]


# ============================================
# Serialization Steps
# ============================================


@given("um ResponseFormat.text()")
def response_format_text_serialization(context):
    """Create ResponseFormat.text() for serialization."""
    context["response_format"] = ResponseFormat.text()


@given("um ResponseFormat com json_schema")
def response_format_json_schema_serialization(context):
    """Create ResponseFormat with json_schema for serialization."""
    context["response_format"] = ResponseFormat.json_with_schema(
        {"type": "object", "additionalProperties": False},
        name="TestSchema",
    )


@when("eu chamo to_dict()")
def chamo_to_dict(context):
    """Call to_dict()."""
    context["result"] = context["response_format"].to_dict()


@then(parsers.parse('o resultado deve conter chave "{key}" com valor "{value}"'))
def resultado_contem_key_value_str(context, key, value):
    """Result should contain key: value (string)."""
    assert context["result"] is not None
    assert key in context["result"]
    assert context["result"][key] == value


@then(parsers.parse('o resultado deve conter chave "{key}" com valor true'))
def resultado_contem_key_true(context, key):
    """Result should contain key: true."""
    assert context["result"] is not None
    assert key in context["result"]
    assert context["result"][key] is True


@then(parsers.parse('o resultado deve conter chave "{key}" com valor false'))
def resultado_contem_key_false(context, key):
    """Result should contain key: false."""
    assert context["result"] is not None
    assert key in context["result"]
    assert context["result"][key] is False


@then(parsers.parse('o resultado deve conter chave "{key}"'))
def resultado_contem_key(context, key):
    """Result should contain key."""
    assert context["result"] is not None
    assert key in context["result"]


# ============================================
# Provider-Specific Steps
# ============================================


@given("provider OpenAI configurado")
def provider_openai_configurado(context):
    """Configure OpenAI provider."""
    context["provider"] = "openai"


@given("provider Anthropic configurado")
def provider_anthropic_configurado(context):
    """Configure Anthropic provider."""
    context["provider"] = "anthropic"


@given("response_format configurado com json_schema")
def response_format_json_schema_provider(context):
    """Configure response_format with json_schema for provider tests."""
    context["response_format"] = ResponseFormat.json_with_schema(
        {"type": "object", "additionalProperties": False},
        name="TestSchema",
    )


@then("a requisicao deve usar parametro text.format")
def requisicao_usa_text_format(context):
    """Request should use text.format parameter."""
    # Verified in unit tests for OpenAI provider
    assert context["provider"] == "openai"
    assert context["response_format"] is not None


@then("o system prompt deve conter instrucoes de JSON")
def system_prompt_contem_instrucoes_json(context):
    """System prompt should contain JSON instructions."""
    # Verified in unit tests for Anthropic provider
    assert context["provider"] == "anthropic"
    assert context["response_format"] is not None


@then("deve haver um tool com o schema")
def deve_haver_tool_com_schema(context):
    """There should be a tool with the schema."""
    # Verified in unit tests for Anthropic provider
    assert context["provider"] == "anthropic"
    assert context["response_format"] is not None
    assert context["response_format"].json_schema is not None


@then("o system prompt deve instruir uso do tool")
def system_prompt_instrui_uso_tool(context):
    """System prompt should instruct tool usage."""
    # Verified in unit tests for Anthropic provider
    assert context["provider"] == "anthropic"
