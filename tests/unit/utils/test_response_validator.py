"""Tests for ResponseValidator."""

import pytest

from forge_llm.domain.entities import ChatResponse
from forge_llm.domain.value_objects import TokenUsage
from forge_llm.utils.response_validator import (
    ResponseValidationError,
    ResponseValidator,
)


def _create_response(content: str) -> ChatResponse:
    """Helper para criar ChatResponse."""
    return ChatResponse(
        content=content,
        model="test-model",
        provider="test",
        usage=TokenUsage(prompt_tokens=10, completion_tokens=5),
        tool_calls=[],
        finish_reason="stop",
    )


class TestResponseValidatorBasics:
    """Testes basicos para ResponseValidator."""

    def test_validator_creation(self):
        """ResponseValidator deve ser criado com schema."""
        schema = {"type": "object"}
        validator = ResponseValidator(schema)
        assert validator.schema == schema


class TestResponseValidatorValidate:
    """Testes de validacao."""

    def test_validate_valid_json(self):
        """Deve validar JSON valido."""
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
            },
        }
        validator = ResponseValidator(schema)
        response = _create_response('{"name": "John"}')
        result = validator.validate(response)
        assert result == {"name": "John"}

    def test_validate_invalid_json(self):
        """Deve lancar erro para JSON invalido."""
        schema = {"type": "object"}
        validator = ResponseValidator(schema)
        response = _create_response("not json")

        with pytest.raises(ResponseValidationError) as exc_info:
            validator.validate(response)

        assert "Invalid JSON" in str(exc_info.value)
        assert exc_info.value.raw_content == "not json"

    def test_validate_schema_mismatch(self):
        """Deve lancar erro quando nao segue schema."""
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
            },
            "required": ["name"],
        }
        validator = ResponseValidator(schema)
        response = _create_response('{"age": 25}')

        with pytest.raises(ResponseValidationError) as exc_info:
            validator.validate(response)

        assert "Schema validation failed" in str(exc_info.value)

    def test_validate_wrong_type(self):
        """Deve lancar erro para tipo errado."""
        schema = {
            "type": "object",
            "properties": {
                "count": {"type": "integer"},
            },
        }
        validator = ResponseValidator(schema)
        response = _create_response('{"count": "not a number"}')

        with pytest.raises(ResponseValidationError):
            validator.validate(response)


class TestResponseValidatorValidateText:
    """Testes de validacao de texto."""

    def test_validate_text_valid(self):
        """Deve validar texto JSON valido."""
        schema = {"type": "array", "items": {"type": "number"}}
        validator = ResponseValidator(schema)
        result = validator.validate_text("[1, 2, 3]")
        assert result == [1, 2, 3]

    def test_validate_text_invalid(self):
        """Deve lancar erro para texto invalido."""
        schema = {"type": "object"}
        validator = ResponseValidator(schema)

        with pytest.raises(ResponseValidationError):
            validator.validate_text("invalid")


class TestResponseValidatorIsValid:
    """Testes do metodo is_valid."""

    def test_is_valid_true(self):
        """Deve retornar True para JSON valido."""
        schema = {"type": "object"}
        validator = ResponseValidator(schema)
        response = _create_response("{}")
        assert validator.is_valid(response) is True

    def test_is_valid_false(self):
        """Deve retornar False para JSON invalido."""
        schema = {"type": "object"}
        validator = ResponseValidator(schema)
        response = _create_response("invalid")
        assert validator.is_valid(response) is False


class TestResponseValidatorExtractJson:
    """Testes de extracao de JSON."""

    def test_extract_json_from_text(self):
        """Deve extrair JSON de texto misto."""
        schema = {"type": "object", "properties": {"name": {"type": "string"}}}
        validator = ResponseValidator(schema)

        text = 'Here is the result: {"name": "John"} and more text'
        result = validator.extract_json(text)
        assert result == {"name": "John"}

    def test_extract_json_array(self):
        """Deve extrair array JSON de texto."""
        schema = {"type": "array", "items": {"type": "number"}}
        validator = ResponseValidator(schema)

        text = "The numbers are [1, 2, 3] as requested"
        result = validator.extract_json(text)
        assert result == [1, 2, 3]

    def test_extract_json_none_when_not_found(self):
        """Deve retornar None quando nao encontrar JSON valido."""
        schema = {"type": "object", "required": ["id"]}
        validator = ResponseValidator(schema)

        text = "No valid JSON here"
        result = validator.extract_json(text)
        assert result is None

    def test_extract_json_prefers_complete_text(self):
        """Deve preferir texto completo se for JSON valido."""
        schema = {"type": "object"}
        validator = ResponseValidator(schema)

        text = '{"key": "value"}'
        result = validator.extract_json(text)
        assert result == {"key": "value"}


class TestResponseValidatorComplexSchemas:
    """Testes com schemas complexos."""

    def test_nested_object(self):
        """Deve validar objetos aninhados."""
        schema = {
            "type": "object",
            "properties": {
                "user": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "email": {"type": "string"},
                    },
                    "required": ["name"],
                },
            },
            "required": ["user"],
        }
        validator = ResponseValidator(schema)
        response = _create_response('{"user": {"name": "John", "email": "j@test.com"}}')
        result = validator.validate(response)
        assert result["user"]["name"] == "John"

    def test_array_of_objects(self):
        """Deve validar array de objetos."""
        schema = {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                },
                "required": ["id"],
            },
        }
        validator = ResponseValidator(schema)
        response = _create_response('[{"id": 1}, {"id": 2}]')
        result = validator.validate(response)
        assert len(result) == 2
