"""
ForgeLLM - Unified LLM client with provider portability.

Main exports:
    - ChatAgent: Main agent for chat interactions
    - AsyncChatAgent: Async agent for chat interactions
    - ChatMessage: Message entity for conversations
    - ChatResponse: Response wrapper with metadata and tokens
    - ChatSession: Session management with history
    - TruncateCompactor: Simple truncation for context compaction
    - SummarizeCompactor: LLM-based summarization for context compaction
    - AsyncSummarizeCompactor: Async LLM-based summarization
    - ToolRegistry: Tool registration and execution
"""
__version__ = "0.4.0"

# Domain exports
# Application exports
from forge_llm.application.agents import AsyncChatAgent, ChatAgent
from forge_llm.application.session import (
    AsyncSummarizeCompactor,
    ChatSession,
    SummarizeCompactor,
    TruncateCompactor,
)
from forge_llm.application.tools import ToolRegistry
from forge_llm.domain.entities import (
    ChatChunk,
    ChatConfig,
    ChatMessage,
    ToolCall,
    ToolDefinition,
    ToolResult,
)
from forge_llm.domain.value_objects import (
    ChatResponse,
    ResponseMetadata,
    TokenUsage,
)

__all__ = [
    "__version__",
    # Domain
    "ChatMessage",
    "ChatConfig",
    "ChatChunk",
    "ToolDefinition",
    "ToolCall",
    "ToolResult",
    # Value Objects
    "ChatResponse",
    "TokenUsage",
    "ResponseMetadata",
    # Application
    "AsyncChatAgent",
    "AsyncSummarizeCompactor",
    "ChatAgent",
    "ChatSession",
    "TruncateCompactor",
    "SummarizeCompactor",
    "ToolRegistry",
]
