"""
E2E Tests for Sprint 2 Features.

These tests validate the Sprint 2 deliverables work correctly
in an integrated environment.
"""
import asyncio
import os
from unittest.mock import MagicMock, patch

import pytest

from forge_llm import ChatAgent, ChatSession, ToolRegistry, TruncateCompactor
from forge_llm.application.agents import AsyncChatAgent
from forge_llm.application.session import SummarizeCompactor
from forge_llm.domain.entities import ProviderConfig
from forge_llm.infrastructure.logging import LogService, reset_logging
from forge_llm.infrastructure.resilience import with_retry


class TestOllamaProviderE2E:
    """E2E tests for Ollama provider."""

    def test_ollama_adapter_creation(self):
        """Test that Ollama adapter can be created."""
        agent = ChatAgent(
            provider="ollama",
            model="llama3",
            base_url="http://localhost:11434",
        )
        assert agent._provider_name == "ollama"

    def test_ollama_adapter_validates_connection(self):
        """Test Ollama validates connection on first use."""
        agent = ChatAgent(
            provider="ollama",
            model="llama3",
            base_url="http://localhost:11434",
        )
        # Without Ollama running, this should fail gracefully
        # The adapter should be created without error
        assert agent is not None


class TestStreamingWithToolsE2E:
    """E2E tests for streaming with tools."""

    def test_stream_chat_with_tools_mock(self):
        """Test streaming with tools using mocked provider."""
        registry = ToolRegistry()

        @registry.tool
        def get_time() -> str:
            """Get current time."""
            return "12:00 PM"

        with patch.object(ChatAgent, "_create_provider") as mock_create:
            mock_provider = MagicMock()
            mock_provider.stream.return_value = iter(
                [
                    {"content": "The time is ", "provider": "openai"},
                    {"content": "12:00 PM", "provider": "openai"},
                    {"content": "", "provider": "openai", "finish_reason": "stop"},
                ]
            )
            mock_create.return_value = mock_provider

            agent = ChatAgent(provider="openai", api_key="test", tools=registry)

            chunks = list(agent.stream_chat("What time is it?"))
            assert len(chunks) >= 1

    def test_tool_registry_with_multiple_tools(self):
        """Test registering multiple tools."""
        registry = ToolRegistry()

        @registry.tool
        def add(a: int, b: int) -> int:
            """Add two numbers."""
            return a + b

        @registry.tool
        def multiply(a: int, b: int) -> int:
            """Multiply two numbers."""
            return a * b

        assert len(registry.list_tools()) == 2
        assert "add" in registry.list_tools()
        assert "multiply" in registry.list_tools()


class TestSummarizeCompactorE2E:
    """E2E tests for SummarizeCompactor."""

    def test_summarize_compactor_initialization(self):
        """Test SummarizeCompactor can be initialized."""
        with patch.object(ChatAgent, "_create_provider"):
            agent = ChatAgent(provider="openai", api_key="test")
            compactor = SummarizeCompactor(
                agent=agent,
                summary_tokens=200,
                keep_recent=4,
            )
            assert compactor._summary_tokens == 200
            assert compactor._keep_recent == 4

    def test_truncate_compactor_in_session(self):
        """Test TruncateCompactor works in session."""
        session = ChatSession(
            system_prompt="You are helpful.",
            max_tokens=100,
            compactor=TruncateCompactor(),
        )
        assert session._compactor is not None


class TestAsyncAPIE2E:
    """E2E tests for Async API."""

    @pytest.mark.asyncio
    async def test_async_agent_creation(self):
        """Test AsyncChatAgent can be created."""
        agent = AsyncChatAgent(
            provider="openai",
            api_key="test-key",
            model="gpt-4o-mini",
        )
        assert agent.provider_name == "openai"

    @pytest.mark.asyncio
    async def test_async_agent_with_mock(self):
        """Test AsyncChatAgent with mocked provider."""
        from unittest.mock import AsyncMock

        mock_provider = AsyncMock()
        mock_response = {
            "content": "Hello!",
            "role": "assistant",
            "model": "gpt-4o-mini",
            "provider": "openai",
            "usage": {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15},
        }
        mock_provider.send.return_value = mock_response

        agent = AsyncChatAgent(
            provider="openai",
            api_key="test-key",
            model="gpt-4o-mini",
        )
        agent._provider = mock_provider

        response = await agent.chat("Hello")
        assert response.content == "Hello!"

    @pytest.mark.asyncio
    async def test_concurrent_async_requests(self):
        """Test multiple async requests can run concurrently."""
        from unittest.mock import AsyncMock

        call_count = 0

        mock_provider = AsyncMock()

        async def mock_send(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            await asyncio.sleep(0.01)  # Simulate network delay
            return {
                "content": f"Response {call_count}",
                "role": "assistant",
                "model": "gpt-4o-mini",
                "provider": "openai",
                "usage": {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15},
            }

        mock_provider.send = mock_send

        agent = AsyncChatAgent(
            provider="openai",
            api_key="test-key",
            model="gpt-4o-mini",
        )
        agent._provider = mock_provider

        # Run 3 concurrent requests
        tasks = [agent.chat(f"Question {i}") for i in range(3)]
        responses = await asyncio.gather(*tasks)

        assert len(responses) == 3
        assert call_count == 3


class TestOpenRouterProviderE2E:
    """E2E tests for OpenRouter provider."""

    def test_openrouter_adapter_creation(self):
        """Test OpenRouter adapter can be created."""
        agent = ChatAgent(
            provider="openrouter",
            api_key="test-key",
            model="openai/gpt-4o",
        )
        assert agent._provider_name == "openrouter"

    def test_openrouter_model_formats(self):
        """Test OpenRouter accepts various model formats."""
        models = [
            "openai/gpt-4o",
            "anthropic/claude-3-haiku",
            "meta-llama/llama-3-70b-instruct",
        ]
        for model in models:
            agent = ChatAgent(
                provider="openrouter",
                api_key="test-key",
                model=model,
            )
            assert agent._config.model == model


class TestStructuredLoggingE2E:
    """E2E tests for structured logging."""

    def setup_method(self):
        """Reset logging before each test."""
        reset_logging()

    def test_log_service_creation(self):
        """Test LogService can be created and used."""
        logger = LogService("test_e2e")
        logger.info("Test message", key="value")
        # No error means success

    def test_correlation_context(self):
        """Test correlation ID context manager."""
        with LogService.correlation_context("test-correlation-123") as cid:
            assert cid == "test-correlation-123"
            assert LogService.get_correlation_id() == "test-correlation-123"

        assert LogService.get_correlation_id() is None

    def test_timed_context(self):
        """Test timing context manager."""
        with LogService.timed("test_operation") as timing:
            pass  # Simulate some work

        assert "elapsed_ms" in timing
        assert timing["elapsed_ms"] >= 0


class TestResilienceE2E:
    """E2E tests for resilience features."""

    def test_retry_decorator_success(self):
        """Test retry decorator with successful function."""
        call_count = 0

        @with_retry(max_attempts=3)
        def successful_function():
            nonlocal call_count
            call_count += 1
            return "success"

        result = successful_function()
        assert result == "success"
        assert call_count == 1

    def test_retry_decorator_eventual_success(self):
        """Test retry decorator with eventual success."""
        call_count = 0

        @with_retry(max_attempts=3, min_wait=0.01, max_wait=0.1)
        def flaky_function():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise ConnectionError("Temporary failure")
            return "success"

        result = flaky_function()
        assert result == "success"
        assert call_count == 2


class TestIntegrationScenarios:
    """Integration scenarios combining multiple features."""

    def test_session_with_compactor_and_tools(self):
        """Test session with compactor and tool registry."""
        registry = ToolRegistry()

        @registry.tool
        def echo(message: str) -> str:
            """Echo a message."""
            return f"Echo: {message}"

        session = ChatSession(
            system_prompt="You are helpful.",
            max_tokens=4000,
            compactor=TruncateCompactor(),
        )

        with patch.object(ChatAgent, "_create_provider") as mock_create:
            mock_provider = MagicMock()
            mock_provider.send.return_value = {
                "content": "Hello!",
                "role": "assistant",
                "model": "gpt-4",
                "provider": "openai",
                "usage": {"input_tokens": 10, "output_tokens": 5},
            }
            mock_create.return_value = mock_provider

            agent = ChatAgent(provider="openai", api_key="test", tools=registry)

            # Should work without errors
            assert agent is not None
            assert session is not None

    def test_logging_with_retry(self):
        """Test logging integration with retry decorator."""
        logger = LogService("retry_test")

        @with_retry(max_attempts=2, min_wait=0.01, max_wait=0.1)
        def logged_operation():
            logger.info("Executing operation")
            return "done"

        with LogService.correlation_context("op-123"):
            result = logged_operation()

        assert result == "done"
