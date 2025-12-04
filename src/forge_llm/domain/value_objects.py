"""Value Objects do ForgeLLMClient."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

from forge_llm.domain.exceptions import ValidationError

# Type alias for message content - using Union for forward reference compatibility
MessageContent = str | list[str | "ImageContent"]


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
