"""Integration tests for Observability with real API calls."""

import os

import pytest

from forge_llm.domain.value_objects import Message

has_any_key = pytest.mark.skipif(
    not (os.getenv("OPENAI_API_KEY") or os.getenv("ANTHROPIC_API_KEY") or os.getenv("OPENROUTER_API_KEY")),
    reason="No API keys available",
)


def get_provider_and_key() -> tuple[str, str]:
    """Get first available provider and key."""
    if os.getenv("OPENAI_API_KEY"):
        return "openai", os.getenv("OPENAI_API_KEY", "")
    if os.getenv("ANTHROPIC_API_KEY"):
        return "anthropic", os.getenv("ANTHROPIC_API_KEY", "")
    if os.getenv("OPENROUTER_API_KEY"):
        return "openrouter", os.getenv("OPENROUTER_API_KEY", "")
    return "", ""


@pytest.mark.integration
@pytest.mark.asyncio
class TestObservabilityIntegration:
    """Integration tests for observability with real API calls."""

    @has_any_key
    async def test_logging_observer_captures_real_call(self):
        """LoggingObserver should capture real API call events."""
        from forge_llm import Client, LoggingObserver, ObservabilityManager

        provider, api_key = get_provider_and_key()
        if not provider:
            pytest.skip("No API keys available")

        obs = ObservabilityManager()
        obs.add_observer(LoggingObserver())

        client = Client(
            provider=provider,
            api_key=api_key,
            observability=obs,
        )

        response = await client.chat("Say 'test'", max_tokens=20)

        assert response.content is not None
        await client.close()

    @has_any_key
    async def test_metrics_observer_tracks_real_call(self):
        """MetricsObserver should track real API call metrics."""
        from forge_llm import Client, MetricsObserver, ObservabilityManager

        provider, api_key = get_provider_and_key()
        if not provider:
            pytest.skip("No API keys available")

        metrics_obs = MetricsObserver()
        obs = ObservabilityManager()
        obs.add_observer(metrics_obs)

        client = Client(
            provider=provider,
            api_key=api_key,
            observability=obs,
        )

        response = await client.chat("Say 'hello'", max_tokens=20)

        assert response.content is not None

        # Verify metrics were captured
        metrics = metrics_obs.metrics
        assert metrics.total_requests == 1
        assert metrics.total_tokens > 0
        assert metrics.avg_latency_ms > 0
        assert provider in metrics.requests_by_provider

        await client.close()

    @has_any_key
    async def test_callback_observer_receives_events(self):
        """CallbackObserver should receive events from real API calls."""
        from forge_llm import (
            CallbackObserver,
            ChatCompleteEvent,
            ChatStartEvent,
            Client,
            ObservabilityManager,
        )

        provider, api_key = get_provider_and_key()
        if not provider:
            pytest.skip("No API keys available")

        events_received: list = []

        async def on_start(event: ChatStartEvent) -> None:
            events_received.append(("start", event))

        async def on_complete(event: ChatCompleteEvent) -> None:
            events_received.append(("complete", event))

        callback_obs = CallbackObserver(on_start=on_start, on_complete=on_complete)
        obs = ObservabilityManager()
        obs.add_observer(callback_obs)

        client = Client(
            provider=provider,
            api_key=api_key,
            observability=obs,
        )

        response = await client.chat("Say 'OK'", max_tokens=20)

        assert response.content is not None

        # Verify callbacks were called
        assert len(events_received) == 2
        assert events_received[0][0] == "start"
        assert events_received[1][0] == "complete"

        # Verify event data
        start_event = events_received[0][1]
        assert start_event.provider == provider
        assert start_event.message_count == 1

        complete_event = events_received[1][1]
        assert complete_event.provider == provider
        assert complete_event.latency_ms > 0
        assert complete_event.token_usage.total_tokens > 0

        await client.close()

    @has_any_key
    async def test_multiple_calls_accumulate_metrics(self):
        """Multiple calls should accumulate in MetricsObserver."""
        from forge_llm import Client, MetricsObserver, ObservabilityManager

        provider, api_key = get_provider_and_key()
        if not provider:
            pytest.skip("No API keys available")

        metrics_obs = MetricsObserver()
        obs = ObservabilityManager()
        obs.add_observer(metrics_obs)

        client = Client(
            provider=provider,
            api_key=api_key,
            observability=obs,
        )

        # Make 3 calls
        for i in range(3):
            await client.chat(f"Say '{i}'", max_tokens=20)

        # Verify accumulated metrics
        metrics = metrics_obs.metrics
        assert metrics.total_requests == 3
        assert metrics.total_tokens > 0
        assert metrics.requests_by_provider[provider] == 3

        await client.close()

    @has_any_key
    async def test_observability_with_conversation(self):
        """Observability should work with Conversation helper."""
        from forge_llm import Client, MetricsObserver, ObservabilityManager

        provider, api_key = get_provider_and_key()
        if not provider:
            pytest.skip("No API keys available")

        metrics_obs = MetricsObserver()
        obs = ObservabilityManager()
        obs.add_observer(metrics_obs)

        client = Client(
            provider=provider,
            api_key=api_key,
            observability=obs,
        )

        conv = client.create_conversation(
            system="You are a helpful assistant",
            max_messages=10,
        )

        # Multi-turn conversation
        await conv.chat("Hello", max_tokens=20)
        await conv.chat("How are you?", max_tokens=20)

        # Verify metrics
        metrics = metrics_obs.metrics
        assert metrics.total_requests == 2

        await client.close()
