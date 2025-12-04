"""
ForgeLLMClient - SDK Python para interface unificada com LLMs.

Exemplo de uso:
    from forge_llm import Client

    client = Client(provider="openai", api_key="sk-...")
    response = await client.chat("Ola!")
    print(response.content)
"""

from forge_llm.client import Client
from forge_llm.domain.entities import ChatResponse, ToolCall
from forge_llm.domain.exceptions import (
    AuthenticationError,
    ConfigurationError,
    ForgeError,
    ProviderError,
    RateLimitError,
    ToolCallNotFoundError,
    ToolNotFoundError,
    ValidationError,
)
from forge_llm.domain.value_objects import Message, TokenUsage, ToolDefinition
from forge_llm.providers.registry import ProviderNotFoundError, ProviderRegistry

__version__ = "0.1.0"

__all__ = [
    # Client
    "Client",
    # Registry
    "ProviderRegistry",
    # Entities
    "ChatResponse",
    "ToolCall",
    # Value Objects
    "Message",
    "TokenUsage",
    "ToolDefinition",
    # Exceptions
    "ForgeError",
    "ValidationError",
    "ProviderError",
    "AuthenticationError",
    "RateLimitError",
    "ConfigurationError",
    "ProviderNotFoundError",
    "ToolNotFoundError",
    "ToolCallNotFoundError",
    # Version
    "__version__",
]
