"""Integration tests for OpenRouter provider."""

import os

import pytest

from forge_llm.domain.value_objects import ImageContent, Message
from forge_llm.providers.openrouter_provider import OpenRouterProvider


@pytest.mark.integration
@pytest.mark.skipif(
    not os.getenv("OPENROUTER_API_KEY"),
    reason="OPENROUTER_API_KEY not set",
)
class TestOpenRouterIntegration:
    """Integration tests for OpenRouter provider."""

    @pytest.fixture
    def provider(self):
        """Create provider with real API key."""
        return OpenRouterProvider(
            api_key=os.getenv("OPENROUTER_API_KEY"),
            site_url="https://forge-llm-test.local",
            site_name="ForgeLLM Test Suite",
        )

    @pytest.mark.asyncio
    async def test_openrouter_chat_basic(self, provider):
        """Test basic chat with OpenRouter."""
        messages = [
            Message(role="user", content="Say 'hello' in one word only"),
        ]

        response = await provider.chat(messages)

        assert response.content is not None
        assert len(response.content) > 0
        assert response.provider == "openrouter"
        assert response.usage.total_tokens > 0

    @pytest.mark.asyncio
    async def test_openrouter_chat_with_system(self, provider):
        """Test chat with system message."""
        messages = [
            Message(role="system", content="You only respond with 'OK'"),
            Message(role="user", content="Hello"),
        ]

        response = await provider.chat(messages)

        assert response.content is not None
        assert "OK" in response.content.upper()

    @pytest.mark.asyncio
    async def test_openrouter_streaming(self, provider):
        """Test streaming response."""
        messages = [
            Message(role="user", content="Count from 1 to 3"),
        ]

        chunks = []
        async for chunk in provider.chat_stream(messages):
            chunks.append(chunk)

        assert len(chunks) > 0
        # Verify we got content
        content = "".join(c["delta"]["content"] for c in chunks)
        assert len(content) > 0
        # Verify streaming produced multiple chunks
        assert len(chunks) > 1

    @pytest.mark.asyncio
    async def test_openrouter_model_selection(self, provider):
        """Test selecting specific model."""
        messages = [
            Message(role="user", content="Say 'test'"),
        ]

        response = await provider.chat(
            messages,
            model="openai/gpt-4o-mini",
        )

        assert response.content is not None
        assert "gpt-4o-mini" in response.model

    @pytest.mark.asyncio
    async def test_openrouter_temperature(self, provider):
        """Test temperature parameter."""
        messages = [
            Message(role="user", content="Say 'hello'"),
        ]

        # Low temperature should give consistent results
        response = await provider.chat(messages, temperature=0.0)

        assert response.content is not None

    @pytest.mark.asyncio
    async def test_openrouter_max_tokens(self, provider):
        """Test max_tokens parameter."""
        messages = [
            Message(role="user", content="Write a long story"),
        ]

        response = await provider.chat(messages, max_tokens=10)

        # Response should be limited
        assert response.content is not None
        # With 10 max tokens, response should be short
        assert response.usage.completion_tokens <= 15  # Some buffer

    @pytest.mark.asyncio
    async def test_openrouter_tool_calling(self, provider):
        """Test tool calling functionality."""
        messages = [
            Message(
                role="user",
                content="What's the weather like in Paris today?",
            ),
        ]

        tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_weather",
                    "description": "Get the current weather in a location",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The city name",
                            },
                        },
                        "required": ["location"],
                    },
                },
            }
        ]

        response = await provider.chat(messages, tools=tools)

        # Model should either respond or call the tool
        assert response.content is not None or len(response.tool_calls) > 0

        if response.tool_calls:
            tool_call = response.tool_calls[0]
            assert tool_call.name == "get_weather"
            assert "location" in tool_call.arguments


@pytest.mark.integration
@pytest.mark.skipif(
    not os.getenv("OPENROUTER_API_KEY"),
    reason="OPENROUTER_API_KEY not set",
)
class TestOpenRouterFreeTierModel:
    """Integration tests using OpenRouter free tier models.

    Note: Free tier models on OpenRouter change frequently.
    These tests will skip if the specified model is unavailable.
    """

    # Free tier models to try (in order of preference)
    FREE_MODELS = [
        "google/gemma-2-9b-it:free",
        "meta-llama/llama-3.2-3b-instruct:free",
        "qwen/qwen-2-7b-instruct:free",
    ]

    @pytest.fixture
    def provider(self):
        """Create provider with first available free tier model."""
        return OpenRouterProvider(
            api_key=os.getenv("OPENROUTER_API_KEY"),
            model=self.FREE_MODELS[0],  # Try first free model
            site_url="https://forge-llm-test.local",
            site_name="ForgeLLM Test Suite",
        )

    @pytest.mark.asyncio
    async def test_free_model_chat(self, provider):
        """Test chat with free tier model."""
        from openai import NotFoundError

        from forge_llm.domain.exceptions import RateLimitError

        messages = [
            Message(role="user", content="Say 'hello' in one word only"),
        ]

        # Try each free model until one works
        for model in self.FREE_MODELS:
            try:
                response = await provider.chat(messages, model=model)
                assert response.content is not None
                assert len(response.content) > 0
                assert response.provider == "openrouter"
                return  # Test passed
            except (NotFoundError, RateLimitError):
                continue  # Try next model

        pytest.skip("No free tier models available on OpenRouter")

    @pytest.mark.asyncio
    async def test_free_model_streaming(self, provider):
        """Test streaming with free tier model."""
        from openai import NotFoundError

        from forge_llm.domain.exceptions import RateLimitError

        messages = [
            Message(role="user", content="Count from 1 to 3"),
        ]

        # Try each free model until one works
        for model in self.FREE_MODELS:
            try:
                chunks = []
                async for chunk in provider.chat_stream(messages, model=model):
                    chunks.append(chunk)

                assert len(chunks) > 0
                content = "".join(c["delta"]["content"] for c in chunks)
                assert len(content) > 0
                return  # Test passed
            except (NotFoundError, RateLimitError):
                continue  # Try next model

        pytest.skip("No free tier models available on OpenRouter")
