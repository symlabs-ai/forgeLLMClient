# Changelog

All notable changes to ForgeLLM will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Structured JSON logging with structlog
  - Correlation ID support for request tracing
  - Timing context manager for measuring operations
  - Contextual logging with `LogService.bind()`
- Mypy strict type checking support across all 42 source files
- OpenRouter provider for unified access to multiple LLM providers
  - Support for OpenAI, Anthropic, Google, Meta, and Mistral models via OpenRouter API
- Async API for non-blocking chat operations
  - `AsyncChatAgent` for async chat and streaming
  - `AsyncOpenAIAdapter` and `AsyncAnthropicAdapter`
  - `IAsyncLLMProviderPort` protocol
- SummarizeCompactor for LLM-based context compaction
  - Automatic summarization of old conversation history
  - Configurable keep_recent and summary_tokens parameters
- Streaming with tool execution support
  - Auto-execute tools during streaming
  - Tool call parsing from streaming chunks
- Coverage configuration for test reporting
- Resilience module with retry and exponential backoff
  - `@with_retry` decorator using tenacity
  - Configurable max attempts and delay
- Ollama provider for local LLM deployment

### Changed
- Updated logging infrastructure to use structlog for JSON output
- Improved type annotations throughout codebase

## [0.1.1] - 2024-12-16

### Added
- Complete MVP implementation
- OpenAI provider adapter
- Anthropic provider adapter
- ChatAgent for unified LLM interactions
- ChatSession for conversation management with context window tracking
- Tool system with ToolRegistry, ToolDefinition, ToolCall, and ToolResult
- Provider configuration with ProviderConfig entity
- Domain errors: ProviderNotConfiguredError, ContextWindowExceededError, ToolExecutionError
- Comprehensive test suite with 221 tests

### Features
- Unified interface for multiple LLM providers
- Automatic context window management
- Tool/function calling support
- Streaming responses
- Session-based conversation history
- Token usage tracking

## [0.1.0] - 2024-12-15

### Added
- Initial project structure
- Clean architecture with hexagonal ports and adapters
- Domain entities and value objects
- Basic infrastructure scaffolding
