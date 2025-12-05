"""
ForgeLLMClient - SDK Python para interface unificada com LLMs.

Exemplo de uso:
    from forge_llm import Client

    client = Client(provider="openai", api_key="sk-...")
    response = await client.chat("Ola!")
    print(response.content)
"""

from forge_llm.client import Client
from forge_llm.domain.entities import ChatResponse, Conversation, ToolCall
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
from forge_llm.domain.value_objects import (
    EnhancedMessage,
    Message,
    MessageMetadata,
    TokenUsage,
    ToolDefinition,
)
from forge_llm.mcp import MCPClient, MCPServerConfig, MCPTool, MCPToolAdapter
from forge_llm.mcp.exceptions import (
    MCPConnectionError,
    MCPError,
    MCPServerNotConnectedError,
    MCPToolExecutionError,
    MCPToolNotFoundError,
)
from forge_llm.providers.auto_fallback_provider import AllProvidersFailedError
from forge_llm.providers.registry import ProviderNotFoundError, ProviderRegistry

__version__ = "0.1.0"

__all__ = [
    # Client
    "Client",
    # Registry
    "ProviderRegistry",
    # Entities
    "ChatResponse",
    "Conversation",
    "ToolCall",
    # Value Objects
    "Message",
    "MessageMetadata",
    "EnhancedMessage",
    "TokenUsage",
    "ToolDefinition",
    # MCP
    "MCPClient",
    "MCPServerConfig",
    "MCPTool",
    "MCPToolAdapter",
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
    "AllProvidersFailedError",
    "MCPError",
    "MCPConnectionError",
    "MCPToolNotFoundError",
    "MCPToolExecutionError",
    "MCPServerNotConnectedError",
    # Version
    "__version__",
]
