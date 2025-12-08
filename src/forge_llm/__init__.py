"""
ForgeLLMClient - SDK Python para interface unificada com LLMs.

Exemplo de uso:
    from forge_llm import Client

    client = Client(provider="openai", api_key="sk-...")
    response = await client.chat("Ola!")
    print(response.content)
"""

from forge_llm.application.ports.conversation_client_port import ConversationClientPort
from forge_llm.client import Client
from forge_llm.domain.entities import ChatResponse, Conversation, ToolCall
from forge_llm.domain.exceptions import (
    APIError,
    APITimeoutError,
    AuthenticationError,
    ConfigurationError,
    ForgeError,
    ProviderError,
    RateLimitError,
    RetryExhaustedError,
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
    HookAbortError,
    HookContext,
    HookFunction,
    HookManager,
    HookType,
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
    create_content_filter_hook,
    create_cost_tracker_hook,
    create_rate_limit_hook,
    create_rate_limiter,
    logging_hook,
    retry_decorator,
    retry_logging_hook,
    timing_hook,
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
from forge_llm.utils import (
    BatchProcessor,
    ConversationMemory,
    ResponseValidationError,
    ResponseValidator,
    TokenCounter,
)
from forge_llm.utils.summarizer import (
    ConversationSummarizer,
    NoOpSummarizer,
    SummarizerConfig,
    SummarizerPort,
    SummaryResult,
)

__version__ = "0.1.1"

__all__ = [
    # Client
    "Client",
    # Ports (Dependency Inversion)
    "ConversationClientPort",
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
    # Exceptions - Base
    "ForgeError",
    "ValidationError",
    "ConfigurationError",
    # Exceptions - Provider-related (inherit from ProviderError)
    "ProviderError",
    "AuthenticationError",
    "RateLimitError",
    "APIError",
    "APITimeoutError",
    "RetryExhaustedError",
    "ProviderNotFoundError",
    "AllProvidersFailedError",
    # Exceptions - Tool-related
    "ToolNotFoundError",
    "ToolCallNotFoundError",
    # Exceptions - MCP-related
    "MCPError",
    "MCPConnectionError",
    "MCPToolNotFoundError",
    "MCPToolExecutionError",
    "MCPServerNotConnectedError",
    # Exceptions - Rate Limiting
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
    # Infrastructure - Hooks
    "HookType",
    "HookContext",
    "HookFunction",
    "HookManager",
    "HookAbortError",
    "logging_hook",
    "timing_hook",
    "retry_logging_hook",
    "create_rate_limit_hook",
    "create_content_filter_hook",
    "create_cost_tracker_hook",
    # Summarizer
    "SummarizerConfig",
    "SummaryResult",
    "SummarizerPort",
    "ConversationSummarizer",
    "NoOpSummarizer",
    # Utils
    "TokenCounter",
    "ConversationMemory",
    "ResponseValidator",
    "ResponseValidationError",
    "BatchProcessor",
    # Version
    "__version__",
]
