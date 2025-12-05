"""Testes unitarios para ResponseFormat."""

import pytest

from forge_llm.domain.exceptions import ValidationError
from forge_llm.domain.value_objects import ResponseFormat


class TestResponseFormat:
    """Testes para ResponseFormat value object."""

    def test_criar_formato_texto(self) -> None:
        """Deve criar formato texto padrao."""
        fmt = ResponseFormat.text()

        assert fmt.type == "text"
        assert fmt.json_schema is None
        assert fmt.schema_name is None
        assert fmt.strict is True

    def test_criar_formato_json_object(self) -> None:
        """Deve criar formato JSON livre."""
        fmt = ResponseFormat.json()

        assert fmt.type == "json_object"
        assert fmt.json_schema is None

    def test_criar_formato_json_schema(self) -> None:
        """Deve criar formato JSON com schema."""
        schema = {
            "type": "object",
            "properties": {"name": {"type": "string"}},
            "required": ["name"],
        }
        fmt = ResponseFormat.json_with_schema(schema, name="Person")

        assert fmt.type == "json_schema"
        assert fmt.json_schema == schema
        assert fmt.schema_name == "Person"
        assert fmt.strict is True

    def test_criar_json_schema_strict_false(self) -> None:
        """Deve criar JSON schema com strict=False."""
        schema = {"type": "object"}
        fmt = ResponseFormat.json_with_schema(schema, strict=False)

        assert fmt.strict is False

    def test_formato_imutavel(self) -> None:
        """ResponseFormat deve ser imutavel (frozen)."""
        fmt = ResponseFormat.json()

        with pytest.raises(AttributeError):
            fmt.type = "text"  # type: ignore

    def test_validar_tipo_invalido(self) -> None:
        """Deve rejeitar tipo invalido."""
        with pytest.raises(ValidationError, match="Tipo de formato invalido"):
            ResponseFormat(type="invalid")  # type: ignore

    def test_validar_json_schema_sem_schema(self) -> None:
        """Deve rejeitar json_schema sem schema fornecido."""
        with pytest.raises(ValidationError, match="json_schema obrigatorio"):
            ResponseFormat(type="json_schema")

    def test_validar_schema_com_tipo_errado(self) -> None:
        """Deve rejeitar schema quando tipo nao e json_schema."""
        with pytest.raises(ValidationError, match="json_schema so pode ser usado"):
            ResponseFormat(type="json_object", json_schema={"type": "object"})

    def test_to_dict_texto(self) -> None:
        """Deve serializar formato texto corretamente."""
        fmt = ResponseFormat.text()
        d = fmt.to_dict()

        assert d["type"] == "text"
        assert d["strict"] is True
        assert "json_schema" not in d

    def test_to_dict_json_schema(self) -> None:
        """Deve serializar formato json_schema corretamente."""
        schema = {"type": "object"}
        fmt = ResponseFormat.json_with_schema(schema, name="Test", strict=False)
        d = fmt.to_dict()

        assert d["type"] == "json_schema"
        assert d["json_schema"] == schema
        assert d["schema_name"] == "Test"
        assert d["strict"] is False


class TestResponseFormatPydantic:
    """Testes para ResponseFormat.from_pydantic()."""

    def test_criar_de_pydantic(self) -> None:
        """Deve criar formato a partir de modelo Pydantic."""
        from pydantic import BaseModel

        class Person(BaseModel):
            name: str
            age: int

        fmt = ResponseFormat.from_pydantic(Person)

        assert fmt.type == "json_schema"
        assert fmt.schema_name == "Person"
        assert fmt.json_schema is not None
        assert "properties" in fmt.json_schema

    def test_criar_de_pydantic_strict_false(self) -> None:
        """Deve criar de Pydantic com strict=False."""
        from pydantic import BaseModel

        class Simple(BaseModel):
            value: str

        fmt = ResponseFormat.from_pydantic(Simple, strict=False)

        assert fmt.strict is False

    def test_rejeitar_classe_nao_pydantic(self) -> None:
        """Deve rejeitar classe que nao e BaseModel."""

        class NotPydantic:
            pass

        with pytest.raises(ValidationError, match="subclasse de pydantic.BaseModel"):
            ResponseFormat.from_pydantic(NotPydantic)  # type: ignore

    def test_rejeitar_instancia_ao_inves_de_classe(self) -> None:
        """Deve rejeitar instancia ao inves de classe."""
        from pydantic import BaseModel

        class Model(BaseModel):
            value: str

        instance = Model(value="test")

        with pytest.raises(ValidationError, match="subclasse de pydantic.BaseModel"):
            ResponseFormat.from_pydantic(instance)  # type: ignore


class TestResponseFormatEquality:
    """Testes para igualdade de ResponseFormat."""

    def test_formatos_iguais(self) -> None:
        """Formatos identicos devem ser iguais."""
        fmt1 = ResponseFormat.json()
        fmt2 = ResponseFormat.json()

        assert fmt1 == fmt2

    def test_formatos_diferentes(self) -> None:
        """Formatos diferentes nao devem ser iguais."""
        fmt1 = ResponseFormat.text()
        fmt2 = ResponseFormat.json()

        assert fmt1 != fmt2

    def test_hash_igual_para_iguais(self) -> None:
        """Formatos iguais devem ter mesmo hash."""
        fmt1 = ResponseFormat(type="json_object")
        fmt2 = ResponseFormat(type="json_object")

        assert hash(fmt1) == hash(fmt2)
