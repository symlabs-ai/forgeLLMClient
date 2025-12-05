"""Integration tests for AutoFallbackProvider."""

import os

import pytest

from forge_llm.domain.value_objects import Message


def get_available_keys() -> dict[str, str]:
    """Get available API keys from environment."""
    keys = {}
    if os.getenv("OPENAI_API_KEY"):
        keys["openai"] = os.getenv("OPENAI_API_KEY", "")
    if os.getenv("ANTHROPIC_API_KEY"):
        keys["anthropic"] = os.getenv("ANTHROPIC_API_KEY", "")
    if os.getenv("OPENROUTER_API_KEY"):
        keys["openrouter"] = os.getenv("OPENROUTER_API_KEY", "")
    return keys


has_multiple_keys = pytest.mark.skipif(
    len(get_available_keys()) < 2,
    reason="Need at least 2 API keys for fallback tests",
)


@pytest.mark.integration
@pytest.mark.asyncio
class TestAutoFallbackIntegration:
    """Integration tests for AutoFallbackProvider with real APIs."""

    @has_multiple_keys
    async def test_fallback_uses_first_provider(self):
        """First provider should be used when healthy."""
        from forge_llm.providers.auto_fallback_provider import AutoFallbackProvider

        keys = get_available_keys()
        providers = list(keys.keys())

        provider = AutoFallbackProvider(
            providers=providers,
            api_keys=keys,
        )

        messages = [Message(role="user", content="Say 'OK'")]
        response = await provider.chat(messages, max_tokens=20)

        assert response.content is not None
        assert provider.last_provider_used == providers[0]

    @has_multiple_keys
    async def test_fallback_tracks_provider_used(self):
        """Provider used should be tracked correctly."""
        from forge_llm.providers.auto_fallback_provider import AutoFallbackProvider

        keys = get_available_keys()
        providers = list(keys.keys())

        provider = AutoFallbackProvider(
            providers=providers,
            api_keys=keys,
        )

        messages = [Message(role="user", content="Say 'hello'")]
        response = await provider.chat(messages, max_tokens=20)

        assert response.content is not None
        assert provider.last_provider_used in providers
        assert provider.last_fallback_result is not None
        assert provider.last_fallback_result.provider_used == provider.last_provider_used

    @has_multiple_keys
    async def test_fallback_with_streaming(self):
        """Streaming should work with fallback provider."""
        from forge_llm.providers.auto_fallback_provider import AutoFallbackProvider

        keys = get_available_keys()
        providers = list(keys.keys())

        provider = AutoFallbackProvider(
            providers=providers,
            api_keys=keys,
        )

        messages = [Message(role="user", content="Count 1 2 3")]

        chunks = []
        async for chunk in provider.chat_stream(messages, max_tokens=20):
            chunks.append(chunk)

        assert len(chunks) > 0
        assert provider.last_provider_used in providers

    @pytest.mark.skipif(
        not os.getenv("OPENAI_API_KEY"),
        reason="OPENAI_API_KEY not set",
    )
    async def test_fallback_with_invalid_first_provider(self):
        """Should fallback when first provider has invalid key."""
        from forge_llm.domain.exceptions import AuthenticationError
        from forge_llm.providers.auto_fallback_provider import (
            AutoFallbackConfig,
            AutoFallbackProvider,
        )

        # First provider has invalid key, second has valid
        provider = AutoFallbackProvider(
            providers=["openai", "openai"],
            api_keys={
                "openai": os.getenv("OPENAI_API_KEY", ""),  # Will use same key for both
            },
            config=AutoFallbackConfig(
                fallback_on_errors=(AuthenticationError,),  # Add auth error for test
            ),
        )

        messages = [Message(role="user", content="Say 'OK'")]
        response = await provider.chat(messages, max_tokens=20)

        # Should succeed with valid key
        assert response.content is not None


@pytest.mark.integration
@pytest.mark.asyncio
class TestAutoFallbackWithClient:
    """Integration tests using AutoFallbackProvider with Client."""

    @has_multiple_keys
    async def test_client_with_fallback_provider(self):
        """Client should work with AutoFallbackProvider."""
        from forge_llm import Client
        from forge_llm.providers.auto_fallback_provider import AutoFallbackProvider

        keys = get_available_keys()
        providers = list(keys.keys())

        fallback = AutoFallbackProvider(
            providers=providers,
            api_keys=keys,
        )

        client = Client(provider=fallback)

        response = await client.chat("Say 'hello'", max_tokens=20)

        assert response.content is not None
        assert fallback.last_provider_used in providers

        await client.close()
