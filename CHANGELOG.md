# Changelog

All notable changes to ForgeLLM will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.5.0] - 2024-12-28

### Added
- **Multimodal Support (Images)** - Full image input support for vision models
  - `ImageContent` value object with `from_url()` and `from_base64()` factory methods
  - `TextContent` value object for explicit text blocks
  - `ContentBlock` type alias for multimodal content
  - `ChatMessage.user_with_image()` and `user_with_images()` factory methods
  - `ChatMessage.has_images` property
  - OpenAI conversion to `image_url` format
  - Anthropic conversion to native image format
  - Support for URL and Base64 image sources
  - Detail level support (auto, low, high) for OpenAI

- **Multimodal Support (Audio)** - Audio input support for speech models
  - `AudioContent` value object with `from_base64()` and `from_file()` factory methods
  - `ChatMessage.user_with_audio()` and `user_with_audios()` factory methods
  - `ChatMessage.has_audio` property
  - OpenAI conversion to `input_audio` format
  - Supported formats: WAV, MP3 (Base64 encoded)
  - Supported provider: OpenAI (gpt-4o-audio-preview)

- **UnsupportedFeatureError** exception for provider-specific feature limitations
  - Raised when attempting to use audio with Anthropic (not supported)

- **Comprehensive tests** for multimodal content
  - 33 tests for content value objects (TextContent, ImageContent, AudioContent)
  - 30 tests for ChatMessage multimodal support
  - Tests for serialization, deserialization, and provider format conversion

### Changed
- Test suite expanded to 576+ unit tests
- `ContentBlock` type alias now includes `AudioContent`

## [0.4.0] - 2024-12-17

### Added
- **SummarizeCompactor production-ready features**
  - Error handling with retry logic and exponential backoff
  - `max_retries` parameter (default 3) for configurable retry attempts
  - `retry_delay` parameter (default 1.0s) with exponential backoff
  - Fallback to truncation when all retries fail
  - Logging for warnings and errors during summarization
- **AsyncSummarizeCompactor** for async applications
  - Full async implementation with `await compactor.compact()`
  - Same API as sync version
  - Uses `asyncio.sleep()` for non-blocking retry delays
- **Comprehensive tests** for SummarizeCompactor
  - Tests for `prompt_file` parameter loading
  - Tests for retry logic and fallback behavior
  - Tests for AsyncSummarizeCompactor (24 tests)
- **Updated examples** in `docs/product/examples/`
  - `session_compaction.py`: retry config, custom prompts, async examples
  - `async_chat.py`: session management, AsyncSummarizeCompactor examples

### Changed
- Examples moved from `/examples/` to `/docs/product/examples/`
- `AsyncChatAgent` and `AsyncSummarizeCompactor` now exported from main package
- Test suite expanded to 542+ unit tests

## [0.3.0] - 2024-12-17

### Added
- Comprehensive documentation in `/docs/product/`
  - User documentation: quickstart, api-reference, providers, tools, sessions, streaming, error-handling, recipes
  - Agent documentation: discovery, api-summary, patterns, troubleshooting
- AI agent discovery module (`forge_llm.dev`)
  - `get_agent_quickstart()` - Complete API guide for AI coding agents
  - `get_documentation_path()` - Path to documentation directory
  - `get_api_summary()` - Condensed API reference
- Live integration tests (`tests/live/`)
  - OpenAI live tests (10 tests)
  - Anthropic live tests (10 tests)
  - Cross-provider tests (6 tests)
  - README with usage instructions
- New unit test scenarios (6 files, ~200 tests)
  - Conversation scenarios
  - Tool chaining scenarios
  - Streaming edge cases
  - Error fallback scenarios
  - Provider switching scenarios
  - Session persistence scenarios
- "Para Agentes de Código de IA" section in README.md for discovery

### Fixed
- Anthropic adapter system prompt handling
  - System messages now correctly extracted and passed as `system` parameter
  - Fixes 400 Bad Request errors with system role

### Changed
- Test suite expanded from ~380 to 508+ unit tests
- README updated with AI agent discovery section

## [0.2.0] - 2024-12-16

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
