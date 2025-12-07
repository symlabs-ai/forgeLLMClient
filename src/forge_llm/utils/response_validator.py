"""Response Validator - Validacao de respostas contra schema JSON."""

import json
from typing import Any

from jsonschema import ValidationError as JsonSchemaError
from jsonschema import validate

from forge_llm.domain.entities import ChatResponse
from forge_llm.domain.exceptions import ForgeError


class ResponseValidationError(ForgeError):
    """Erro de validacao de resposta."""

    def __init__(self, message: str, raw_content: str | None = None) -> None:
        """
        Inicializar erro de validacao.

        Args:
            message: Mensagem de erro
            raw_content: Conteudo original que falhou validacao
        """
        super().__init__(message)
        self.raw_content = raw_content


class ResponseValidator:
    """
    Validador de respostas contra schema JSON.

    Util para garantir que respostas do LLM sigam um formato esperado.

    Exemplo:
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"}
            },
            "required": ["name"]
        }
        validator = ResponseValidator(schema)
        data = validator.validate(response)
    """

    def __init__(self, schema: dict[str, Any]) -> None:
        """
        Inicializar validador.

        Args:
            schema: JSON Schema para validacao
        """
        self._schema = schema

    def validate(self, response: ChatResponse) -> dict[str, Any]:
        """
        Validar resposta contra schema.

        Args:
            response: Resposta do chat

        Returns:
            Dados validados como dicionario

        Raises:
            ResponseValidationError: Se resposta nao for JSON valido ou
                                    nao seguir schema
        """
        return self.validate_text(response.content)

    def validate_text(self, text: str) -> dict[str, Any]:
        """
        Validar texto JSON contra schema.

        Args:
            text: Texto JSON para validar

        Returns:
            Dados validados como dicionario

        Raises:
            ResponseValidationError: Se texto nao for JSON valido ou
                                    nao seguir schema
        """
        # Parse JSON
        try:
            data = json.loads(text)
        except json.JSONDecodeError as e:
            raise ResponseValidationError(
                f"Invalid JSON: {e}",
                raw_content=text,
            ) from e

        # Validate against schema
        try:
            validate(instance=data, schema=self._schema)
        except JsonSchemaError as e:
            raise ResponseValidationError(
                f"Schema validation failed: {e.message}",
                raw_content=text,
            ) from e

        return data  # type: ignore[no-any-return]

    def is_valid(self, response: ChatResponse) -> bool:
        """
        Verificar se resposta e valida sem lancar excecao.

        Args:
            response: Resposta do chat

        Returns:
            True se valido, False caso contrario
        """
        try:
            self.validate(response)
            return True
        except ResponseValidationError:
            return False

    def extract_json(self, text: str) -> dict[str, Any] | None:
        """
        Tentar extrair e validar JSON de texto que pode conter outros dados.

        Busca por blocos JSON no texto (entre {} ou []).

        Args:
            text: Texto que pode conter JSON

        Returns:
            Dados validados ou None se nao encontrar JSON valido
        """
        # Tentar texto completo primeiro
        try:
            return self.validate_text(text)
        except ResponseValidationError:
            pass

        # Procurar por blocos JSON
        start_chars = ["{", "["]
        end_chars = ["}", "]"]

        for start_char, end_char in zip(start_chars, end_chars, strict=False):
            start = text.find(start_char)
            if start == -1:
                continue

            # Encontrar o fechamento correspondente
            depth = 0
            for i, char in enumerate(text[start:], start):
                if char == start_char:
                    depth += 1
                elif char == end_char:
                    depth -= 1
                    if depth == 0:
                        try:
                            return self.validate_text(text[start : i + 1])
                        except ResponseValidationError:
                            break

        return None

    @property
    def schema(self) -> dict[str, Any]:
        """Schema JSON usado para validacao."""
        return self._schema
