"""Unit tests for Client retry integration."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from forge_llm.client import Client
from forge_llm.domain.entities import ChatResponse
from forge_llm.domain.exceptions import (
    AuthenticationError,
    RateLimitError,
    RetryExhaustedError,
    ValidationError,
)
from forge_llm.domain.value_objects import TokenUsage
from forge_llm.infrastructure.retry import RetryConfig


class TestClientRetryConfiguration:
    """Tests for Client retry configuration."""

    def test_client_without_retry(self):
        """Client without retry config has no retry."""
        client = Client(provider="mock", api_key="test-key")

        assert client._retry_config is None

    def test_client_with_max_retries(self):
        """Client with max_retries creates RetryConfig."""
        client = Client(provider="mock", api_key="test-key", max_retries=3)

        assert client._retry_config is not None
        assert client._retry_config.max_retries == 3
        assert client._retry_config.base_delay == 1.0  # default

    def test_client_with_retry_delay(self):
        """Client with retry_delay configures base_delay."""
        client = Client(
            provider="mock", api_key="test-key", max_retries=3, retry_delay=0.5
        )

        assert client._retry_config is not None
        assert client._retry_config.base_delay == 0.5

    def test_client_with_custom_retry_config(self):
        """Client accepts custom RetryConfig."""
        config = RetryConfig(
            max_retries=5,
            base_delay=2.0,
            max_delay=30.0,
            jitter=False,
        )
        client = Client(provider="mock", api_key="test-key", retry_config=config)

        assert client._retry_config is config
        assert client._retry_config.max_retries == 5
        assert client._retry_config.base_delay == 2.0
        assert client._retry_config.max_delay == 30.0
        assert client._retry_config.jitter is False

    def test_retry_config_overrides_max_retries(self):
        """retry_config takes precedence over max_retries."""
        config = RetryConfig(max_retries=10)
        client = Client(
            provider="mock", api_key="test-key", max_retries=3, retry_config=config
        )

        # retry_config should take precedence
        assert client._retry_config.max_retries == 10

    def test_zero_max_retries_means_no_retry(self):
        """max_retries=0 means no retry config."""
        client = Client(provider="mock", api_key="test-key", max_retries=0)

        assert client._retry_config is None


class TestClientRetryBehavior:
    """Tests for Client retry behavior during chat."""

    @pytest.fixture
    def mock_provider(self):
        """Create a mock provider."""
        provider = MagicMock()
        provider.provider_name = "mock"
        provider.default_model = "mock-model"
        provider.chat = AsyncMock()
        return provider

    @pytest.mark.asyncio
    async def test_chat_without_retry_calls_once(self, mock_provider):
        """Chat without retry config calls provider once."""
        usage = TokenUsage(prompt_tokens=10, completion_tokens=5)
        response = ChatResponse(
            content="Hello!", model="mock-model", provider="mock", usage=usage
        )
        mock_provider.chat.return_value = response

        client = Client()
        client.configure(mock_provider)

        result = await client.chat("Hello")

        assert result == response
        assert mock_provider.chat.call_count == 1

    @pytest.mark.asyncio
    async def test_chat_with_retry_success_first_attempt(self, mock_provider):
        """Chat with retry that succeeds on first attempt."""
        usage = TokenUsage(prompt_tokens=10, completion_tokens=5)
        response = ChatResponse(
            content="Hello!", model="mock-model", provider="mock", usage=usage
        )
        mock_provider.chat.return_value = response

        client = Client(max_retries=3)
        client.configure(mock_provider)

        result = await client.chat("Hello")

        assert result == response
        assert mock_provider.chat.call_count == 1

    @pytest.mark.asyncio
    async def test_chat_with_retry_success_after_failures(self, mock_provider):
        """Chat with retry succeeds after retryable failures."""
        usage = TokenUsage(prompt_tokens=10, completion_tokens=5)
        response = ChatResponse(
            content="Hello!", model="mock-model", provider="mock", usage=usage
        )
        call_count = 0

        async def chat_with_failures(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise RateLimitError("Rate limited", "mock")
            return response

        mock_provider.chat.side_effect = chat_with_failures

        client = Client(max_retries=3, retry_delay=0.01)
        client.configure(mock_provider)

        result = await client.chat("Hello")

        assert result == response
        assert call_count == 3

    @pytest.mark.asyncio
    async def test_chat_exhausts_retries(self, mock_provider):
        """Chat raises RetryExhaustedError when retries exhausted."""
        mock_provider.chat.side_effect = RateLimitError("Rate limited", "mock")

        client = Client(max_retries=2, retry_delay=0.01)
        client.configure(mock_provider)

        with pytest.raises(RetryExhaustedError) as exc_info:
            await client.chat("Hello")

        assert exc_info.value.attempts == 3  # max_retries + 1
        assert exc_info.value.provider == "mock"

    @pytest.mark.asyncio
    async def test_chat_non_retryable_error_not_retried(self, mock_provider):
        """Non-retryable errors are raised immediately without retry."""
        mock_provider.chat.side_effect = AuthenticationError("Invalid key", "mock")

        client = Client(max_retries=3, retry_delay=0.01)
        client.configure(mock_provider)

        with pytest.raises(AuthenticationError):
            await client.chat("Hello")

        # Should only be called once - no retries
        assert mock_provider.chat.call_count == 1

    @pytest.mark.asyncio
    async def test_chat_validation_error_not_retried(self):
        """Validation errors are raised without retry."""
        client = Client(provider="mock", api_key="test-key", max_retries=3)

        with pytest.raises(ValidationError):
            await client.chat("")  # empty message


class TestClientProperties:
    """Tests for Client properties."""

    def test_is_configured_false_initially(self):
        """Client is not configured when created without provider."""
        client = Client()

        assert client.is_configured is False

    def test_is_configured_true_with_provider(self):
        """Client is configured when provider is set."""
        client = Client(provider="mock", api_key="test-key")

        assert client.is_configured is True

    def test_provider_name_raises_when_not_configured(self):
        """provider_name raises when client not configured."""
        client = Client()

        with pytest.raises(RuntimeError, match="Cliente nao configurado"):
            _ = client.provider_name

    def test_model_raises_when_not_configured(self):
        """model raises when client not configured."""
        client = Client()

        with pytest.raises(RuntimeError, match="Cliente nao configurado"):
            _ = client.model

    def test_chat_raises_when_not_configured(self):
        """chat raises when client not configured."""
        client = Client()

        with pytest.raises(RuntimeError, match="Cliente nao configurado"):
            import asyncio

            asyncio.get_event_loop().run_until_complete(client.chat("Hello"))


class TestClientConversation:
    """Tests for Client.create_conversation."""

    def test_create_conversation_basic(self):
        """create_conversation returns Conversation instance."""
        from forge_llm.domain.entities import Conversation

        client = Client(provider="mock", api_key="test-key")
        conv = client.create_conversation()

        assert isinstance(conv, Conversation)
        assert conv.system_prompt is None
        assert conv.max_messages is None
        assert conv.is_empty()

    def test_create_conversation_with_system_prompt(self):
        """create_conversation accepts system prompt."""
        client = Client(provider="mock", api_key="test-key")
        conv = client.create_conversation(system="You are helpful")

        assert conv.system_prompt == "You are helpful"

    def test_create_conversation_with_max_messages(self):
        """create_conversation accepts max_messages limit."""
        client = Client(provider="mock", api_key="test-key")
        conv = client.create_conversation(max_messages=10)

        assert conv.max_messages == 10

    def test_create_conversation_with_all_options(self):
        """create_conversation accepts all options."""
        client = Client(provider="mock", api_key="test-key")
        conv = client.create_conversation(system="Be brief", max_messages=20)

        assert conv.system_prompt == "Be brief"
        assert conv.max_messages == 20

    def test_create_conversation_raises_when_not_configured(self):
        """create_conversation raises when client not configured."""
        client = Client()

        with pytest.raises(RuntimeError, match="Cliente nao configurado"):
            client.create_conversation()

    def test_conversation_max_messages_trims_history(self):
        """Conversation trims messages when max_messages is exceeded."""
        client = Client(provider="mock", api_key="test-key")
        conv = client.create_conversation(max_messages=4)

        # Add 6 messages (3 pairs)
        conv.add_user_message("msg1")
        conv.add_assistant_message("resp1")
        conv.add_user_message("msg2")
        conv.add_assistant_message("resp2")
        conv.add_user_message("msg3")
        conv.add_assistant_message("resp3")

        # Should only have last 4 messages
        assert conv.message_count == 4
        messages = conv.messages
        # After 6 messages with max=4, keeps: msg2, resp2, msg3, resp3
        assert messages[0].content == "msg2"
        assert messages[1].content == "resp2"
        assert messages[2].content == "msg3"
        assert messages[3].content == "resp3"
