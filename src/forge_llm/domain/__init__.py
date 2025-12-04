"""Domain layer - Entidades, Value Objects e Exceptions."""

from forge_llm.domain.entities import ChatResponse, ToolCall
from forge_llm.domain.exceptions import (
    AuthenticationError,
    ConfigurationError,
    ForgeError,
    ProviderError,
    RateLimitError,
    ToolNotFoundError,
    ValidationError,
)
from forge_llm.domain.value_objects import Message, TokenUsage, ToolDefinition

__all__ = [
    "ChatResponse",
    "ToolCall",
    "Message",
    "TokenUsage",
    "ToolDefinition",
    "ForgeError",
    "ProviderError",
    "AuthenticationError",
    "RateLimitError",
    "ConfigurationError",
    "ToolNotFoundError",
    "ValidationError",
]
