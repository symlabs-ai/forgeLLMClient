"""Value Objects do ForgeLLMClient."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Literal, Union

from forge_llm.domain.exceptions import ValidationError

# Type alias for message content - using Union for forward reference compatibility
# X | Y syntax causes TypeError at runtime with forward references
MessageContent = Union[str, list[Union[str, "ImageContent"]]]  # noqa: UP007


@dataclass(frozen=True, eq=True)
class Message:
    """
    Mensagem em uma conversa com LLM.

    Value object imutavel representando uma mensagem.
    Suporta conteudo simples (str) ou misto (lista de texto e imagens).
    """

    role: Literal["system", "user", "assistant", "tool"]
    content: MessageContent
    name: str | None = None
    tool_call_id: str | None = None

    def __post_init__(self) -> None:
        """Validar apos inicializacao."""
        self._validate()

    def _validate(self) -> None:
        """Validar invariantes da mensagem."""
        valid_roles = {"system", "user", "assistant", "tool"}
        if self.role not in valid_roles:
            raise ValidationError(f"Role invalido: {self.role}")

        if self.role == "tool" and not self.tool_call_id:
            raise ValidationError("tool_call_id obrigatorio para role 'tool'")

    @property
    def has_images(self) -> bool:
        """Indica se a mensagem contem imagens."""
        if isinstance(self.content, str):
            return False
        return any(isinstance(item, ImageContent) for item in self.content)

    @property
    def images(self) -> list[ImageContent]:
        """Retorna lista de imagens na mensagem."""
        if isinstance(self.content, str):
            return []
        return [item for item in self.content if isinstance(item, ImageContent)]

    @property
    def text_content(self) -> str:
        """Retorna apenas o texto da mensagem."""
        if isinstance(self.content, str):
            return self.content
        texts = [item for item in self.content if isinstance(item, str)]
        return " ".join(texts)

    def to_dict(self) -> dict[str, Any]:
        """Converter para dicionario."""
        d: dict[str, Any] = {"role": self.role, "content": self.content}
        if self.name:
            d["name"] = self.name
        if self.tool_call_id:
            d["tool_call_id"] = self.tool_call_id
        return d


@dataclass(frozen=True, eq=True)
class TokenUsage:
    """Informacoes de consumo de tokens."""

    prompt_tokens: int
    completion_tokens: int
    total_tokens: int = field(default=-1)

    def __post_init__(self) -> None:
        """Calcular total e validar."""
        # Calcular total se nao fornecido
        if self.total_tokens == -1:
            object.__setattr__(
                self, "total_tokens", self.prompt_tokens + self.completion_tokens
            )
        self._validate()

    def _validate(self) -> None:
        """Validar invariantes."""
        if self.prompt_tokens < 0:
            raise ValidationError("prompt_tokens nao pode ser negativo")
        if self.completion_tokens < 0:
            raise ValidationError("completion_tokens nao pode ser negativo")

    def to_dict(self) -> dict[str, int]:
        """Converter para dicionario."""
        return {
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "total_tokens": self.total_tokens,
        }


@dataclass(frozen=True, eq=True)
class ToolDefinition:
    """Definicao de uma ferramenta para tool calling."""

    name: str
    description: str
    parameters: dict[str, Any]

    def __post_init__(self) -> None:
        """Validar apos inicializacao."""
        self._validate()

    def _validate(self) -> None:
        """Validar invariantes."""
        if not self.name:
            raise ValidationError("Nome da tool e obrigatorio")
        if not self.description:
            raise ValidationError("Descricao da tool e obrigatoria")

    def to_dict(self) -> dict[str, Any]:
        """Converter para dicionario."""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters,
        }


# Tamanho maximo de base64 em bytes (20MB - limite comum das APIs)
MAX_BASE64_SIZE = 20 * 1024 * 1024


@dataclass(frozen=True, eq=True)
class ImageContent:
    """
    Conteudo de imagem para mensagens multimodais.

    Suporta imagens por URL ou base64.
    Limite de 20MB para base64 (limite comum das APIs).
    """

    url: str | None = None
    base64_data: str | None = None
    media_type: str = "image/jpeg"

    def __post_init__(self) -> None:
        """Validar apos inicializacao."""
        self._validate()

    def _validate(self) -> None:
        """Validar invariantes."""
        if not self.url and not self.base64_data:
            raise ValidationError("URL ou base64_data obrigatorio")
        if self.url and self.base64_data:
            raise ValidationError("Usar URL ou base64_data, nao ambos")

        valid_media_types = {"image/jpeg", "image/png", "image/gif", "image/webp"}
        if self.media_type not in valid_media_types:
            raise ValidationError(f"Media type invalido: {self.media_type}")

        # Validar tamanho do base64
        if self.base64_data and len(self.base64_data) > MAX_BASE64_SIZE:
            raise ValidationError(
                f"Base64 excede limite de {MAX_BASE64_SIZE // (1024*1024)}MB"
            )

    @property
    def is_url(self) -> bool:
        """Indica se a imagem e por URL."""
        return self.url is not None

    @property
    def is_base64(self) -> bool:
        """Indica se a imagem e em base64."""
        return self.base64_data is not None

    def to_dict(self) -> dict[str, Any]:
        """Converter para dicionario."""
        if self.url:
            return {"type": "url", "url": self.url, "media_type": self.media_type}
        return {
            "type": "base64",
            "data": self.base64_data,
            "media_type": self.media_type,
        }


@dataclass(frozen=True, eq=True)
class ResponseFormat:
    """
    Formato de resposta estruturada para LLMs.

    Suporta modos:
    - "text": Resposta padrão em texto livre
    - "json_object": Resposta JSON (modelo escolhe estrutura)
    - "json_schema": Resposta JSON validada contra schema

    Para json_schema, forneça um JSON Schema ou classe Pydantic.

    Exemplo:
        # JSON livre
        format = ResponseFormat(type="json_object")

        # Com schema
        format = ResponseFormat(
            type="json_schema",
            json_schema={
                "type": "object",
                "properties": {"name": {"type": "string"}},
                "required": ["name"]
            }
        )

        # Com Pydantic (requer pydantic instalado)
        from pydantic import BaseModel
        class Person(BaseModel):
            name: str
            age: int
        format = ResponseFormat.from_pydantic(Person)
    """

    type: Literal["text", "json_object", "json_schema"] = "text"
    json_schema: dict[str, Any] | None = None
    schema_name: str | None = None
    strict: bool = True

    def __post_init__(self) -> None:
        """Validar apos inicializacao."""
        self._validate()

    def _validate(self) -> None:
        """Validar invariantes."""
        valid_types = {"text", "json_object", "json_schema"}
        if self.type not in valid_types:
            raise ValidationError(f"Tipo de formato invalido: {self.type}")

        if self.type == "json_schema" and not self.json_schema:
            raise ValidationError("json_schema obrigatorio para type='json_schema'")

        if self.type != "json_schema" and self.json_schema:
            raise ValidationError("json_schema so pode ser usado com type='json_schema'")

    @classmethod
    def text(cls) -> ResponseFormat:
        """Criar formato texto padrão."""
        return cls(type="text")

    @classmethod
    def json(cls) -> ResponseFormat:
        """Criar formato JSON livre."""
        return cls(type="json_object")

    @classmethod
    def json_with_schema(
        cls,
        schema: dict[str, Any],
        name: str | None = None,
        strict: bool = True,
    ) -> ResponseFormat:
        """
        Criar formato JSON com schema.

        Args:
            schema: JSON Schema dict
            name: Nome do schema (opcional, gerado automaticamente)
            strict: Se True, força resposta exata ao schema
        """
        return cls(
            type="json_schema",
            json_schema=schema,
            schema_name=name,
            strict=strict,
        )

    @classmethod
    def from_pydantic(  # type: ignore[valid-type]
        cls, model: type[Any], strict: bool = True
    ) -> ResponseFormat:
        """
        Criar formato a partir de modelo Pydantic.

        Args:
            model: Classe Pydantic (BaseModel)
            strict: Se True, força resposta exata ao schema

        Returns:
            ResponseFormat configurado com schema do modelo

        Raises:
            ValidationError: Se pydantic não disponível ou modelo inválido

        Note:
            When strict=True, adds 'additionalProperties: false' to the root
            schema for OpenAI API compatibility (required for structured outputs).
        """
        try:
            from pydantic import BaseModel
        except ImportError as e:
            raise ValidationError("pydantic necessario para from_pydantic()") from e

        if not isinstance(model, type) or not issubclass(model, BaseModel):
            raise ValidationError("model deve ser subclasse de pydantic.BaseModel")

        schema: dict[str, Any] = model.model_json_schema()  # type: ignore[attr-defined]
        name: str = model.__name__  # type: ignore[attr-defined]

        # Add additionalProperties: false for OpenAI strict mode compatibility
        if strict and schema.get("type") == "object":
            schema = dict(schema)  # Make a copy to avoid mutating cached schema
            schema["additionalProperties"] = False

        return cls(
            type="json_schema",
            json_schema=schema,
            schema_name=name,
            strict=strict,
        )

    def to_dict(self) -> dict[str, Any]:
        """Converter para dicionario."""
        result: dict[str, Any] = {"type": self.type}
        if self.json_schema:
            result["json_schema"] = self.json_schema
        if self.schema_name:
            result["schema_name"] = self.schema_name
        result["strict"] = self.strict
        return result


@dataclass(frozen=True, eq=True)
class MessageMetadata:
    """
    Metadados de uma mensagem na conversa.

    Rastreia informacoes de contexto como timestamp, provider e modelo
    usados para gerar/receber a mensagem.
    """

    timestamp: datetime = field(default_factory=datetime.now)
    provider: str | None = None
    model: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Converter para dicionario."""
        return {
            "timestamp": self.timestamp.isoformat(),
            "provider": self.provider,
            "model": self.model,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> MessageMetadata:
        """Criar a partir de dicionario."""
        timestamp = data.get("timestamp")
        if isinstance(timestamp, str):
            try:
                timestamp = datetime.fromisoformat(timestamp)
            except ValueError as e:
                raise ValidationError(f"Timestamp inválido: {timestamp}") from e
        elif timestamp is None:
            timestamp = datetime.now()

        return cls(
            timestamp=timestamp,
            provider=data.get("provider"),
            model=data.get("model"),
        )


@dataclass(frozen=True, eq=True)
class EnhancedMessage:
    """
    Mensagem com metadados de contexto.

    Combina Message com MessageMetadata para rastreamento
    completo do historico da conversa.
    """

    message: Message
    metadata: MessageMetadata = field(default_factory=MessageMetadata)

    @property
    def role(self) -> str:
        """Role da mensagem."""
        return self.message.role

    @property
    def content(self) -> MessageContent:
        """Conteudo da mensagem."""
        return self.message.content

    @property
    def timestamp(self) -> datetime:
        """Timestamp da mensagem."""
        return self.metadata.timestamp

    @property
    def provider(self) -> str | None:
        """Provider que gerou/recebeu a mensagem."""
        return self.metadata.provider

    @property
    def model(self) -> str | None:
        """Modelo usado."""
        return self.metadata.model

    def to_dict(self) -> dict[str, Any]:
        """Converter para dicionario."""
        return {
            "message": self.message.to_dict(),
            "metadata": self.metadata.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> EnhancedMessage:
        """Criar a partir de dicionario."""
        if "message" not in data:
            raise ValidationError("Campo 'message' obrigatório em EnhancedMessage")

        msg_data = data["message"]
        if "role" not in msg_data or "content" not in msg_data:
            raise ValidationError("Campos 'role' e 'content' obrigatórios em message")

        meta_data = data.get("metadata", {})

        message = Message(
            role=msg_data["role"],
            content=msg_data["content"],
            name=msg_data.get("name"),
            tool_call_id=msg_data.get("tool_call_id"),
        )
        metadata = MessageMetadata.from_dict(meta_data)

        return cls(message=message, metadata=metadata)
