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
    ResponseFormat,
    TokenUsage,
    ToolDefinition,
)
from forge_llm.infrastructure import (
    CacheConfig,
    CacheKey,
    CachePort,
    CacheStats,
    CompositeRateLimiter,
    InMemoryCache,
    NoOpCache,
    NoOpRateLimiter,
    RateLimitConfig,
    RateLimiterPort,
    RateLimitExceededError,
    RateLimitStats,
    RetryCallback,
    RetryConfig,
    TokenBucketRateLimiter,
    create_rate_limiter,
    retry_decorator,
    with_retry,
)
from forge_llm.mcp import MCPClient, MCPServerConfig, MCPTool, MCPToolAdapter
from forge_llm.mcp.exceptions import (
    MCPConnectionError,
    MCPError,
    MCPServerNotConnectedError,
    MCPToolExecutionError,
    MCPToolNotFoundError,
)
from forge_llm.observability import (
    CallbackObserver,
    ChatCompleteEvent,
    ChatErrorEvent,
    ChatStartEvent,
    LoggingObserver,
    MetricsObserver,
    ObservabilityConfig,
    ObservabilityManager,
    ObserverPort,
    RetryEvent,
    StreamChunkEvent,
    UsageMetrics,
)
from forge_llm.persistence import (
    ConversationStore,
    InMemoryConversationStore,
    JSONConversationStore,
    StoredConversation,
)
from forge_llm.providers.auto_fallback_provider import AllProvidersFailedError
from forge_llm.providers.registry import ProviderNotFoundError, ProviderRegistry
from forge_llm.utils.summarizer import (
    ConversationSummarizer,
    NoOpSummarizer,
    SummarizerConfig,
    SummarizerPort,
    SummaryResult,
)

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
    "ResponseFormat",
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
    "RateLimitExceededError",
    # Observability
    "ObservabilityManager",
    "ObservabilityConfig",
    "ObserverPort",
    "LoggingObserver",
    "MetricsObserver",
    "UsageMetrics",
    "CallbackObserver",
    "ChatStartEvent",
    "ChatCompleteEvent",
    "ChatErrorEvent",
    "RetryEvent",
    "StreamChunkEvent",
    # Persistence
    "ConversationStore",
    "StoredConversation",
    "JSONConversationStore",
    "InMemoryConversationStore",
    # Infrastructure - Cache
    "CacheConfig",
    "CacheKey",
    "CachePort",
    "CacheStats",
    "InMemoryCache",
    "NoOpCache",
    # Infrastructure - Rate Limiter
    "RateLimitConfig",
    "RateLimitStats",
    "RateLimiterPort",
    "TokenBucketRateLimiter",
    "NoOpRateLimiter",
    "CompositeRateLimiter",
    "create_rate_limiter",
    # Infrastructure - Retry
    "RetryConfig",
    "RetryCallback",
    "with_retry",
    "retry_decorator",
    # Summarizer
    "SummarizerConfig",
    "SummaryResult",
    "SummarizerPort",
    "ConversationSummarizer",
    "NoOpSummarizer",
    # Version
    "__version__",
]
