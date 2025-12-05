"""Testes unitarios para observers."""

import logging
from datetime import datetime

import pytest

from forge_llm.domain.value_objects import TokenUsage
from forge_llm.observability.events import (
    ChatCompleteEvent,
    ChatErrorEvent,
    ChatStartEvent,
    RetryEvent,
    StreamChunkEvent,
)
from forge_llm.observability.observers import (
    CallbackObserver,
    LoggingObserver,
    MetricsObserver,
)


class TestLoggingObserver:
    """Testes para LoggingObserver."""

    @pytest.mark.asyncio
    async def test_log_chat_start(self, caplog: pytest.LogCaptureFixture) -> None:
        """Deve logar inicio de chat."""
        observer = LoggingObserver(level=logging.INFO)

        event = ChatStartEvent(
            timestamp=datetime.now(),
            request_id="req_abc123",
            provider="openai",
            model="gpt-4",
            message_count=3,
            has_tools=True,
        )

        with caplog.at_level(logging.INFO, logger="forge_llm"):
            await observer.on_event(event)

        assert "req_abc123" in caplog.text
        assert "openai" in caplog.text
        assert "gpt-4" in caplog.text
        assert "Chat started" in caplog.text

    @pytest.mark.asyncio
    async def test_log_chat_complete(self, caplog: pytest.LogCaptureFixture) -> None:
        """Deve logar conclusao de chat."""
        observer = LoggingObserver(level=logging.INFO)

        event = ChatCompleteEvent(
            timestamp=datetime.now(),
            request_id="req_abc123",
            provider="openai",
            model="gpt-4",
            latency_ms=245.5,
            token_usage=TokenUsage(prompt_tokens=10, completion_tokens=20, total_tokens=30),
            finish_reason="stop",
            tool_calls_count=0,
        )

        with caplog.at_level(logging.INFO, logger="forge_llm"):
            await observer.on_event(event)

        assert "req_abc123" in caplog.text
        assert "Chat completed" in caplog.text
        assert "245" in caplog.text  # latency

    @pytest.mark.asyncio
    async def test_log_chat_error(self, caplog: pytest.LogCaptureFixture) -> None:
        """Deve logar erro de chat como ERROR."""
        observer = LoggingObserver()

        event = ChatErrorEvent(
            timestamp=datetime.now(),
            request_id="req_abc123",
            provider="openai",
            error_type="RateLimitError",
            error_message="Rate limit exceeded",
            latency_ms=50.0,
            retryable=True,
        )

        with caplog.at_level(logging.ERROR, logger="forge_llm"):
            await observer.on_event(event)

        assert "req_abc123" in caplog.text
        assert "RateLimitError" in caplog.text
        assert "Chat error" in caplog.text

    @pytest.mark.asyncio
    async def test_log_retry(self, caplog: pytest.LogCaptureFixture) -> None:
        """Deve logar retry como WARNING."""
        observer = LoggingObserver()

        event = RetryEvent(
            timestamp=datetime.now(),
            request_id="req_abc123",
            provider="openai",
            attempt=2,
            max_attempts=3,
            delay_ms=2000.0,
            error_type="RateLimitError",
        )

        with caplog.at_level(logging.WARNING, logger="forge_llm"):
            await observer.on_event(event)

        assert "req_abc123" in caplog.text
        assert "Retry" in caplog.text
        assert "2" in caplog.text  # attempt
        assert "3" in caplog.text  # max_attempts

    @pytest.mark.asyncio
    async def test_log_stream_chunk(self, caplog: pytest.LogCaptureFixture) -> None:
        """Deve logar chunk como DEBUG."""
        observer = LoggingObserver()

        event = StreamChunkEvent(
            timestamp=datetime.now(),
            request_id="req_abc123",
            provider="openai",
            chunk_index=5,
            has_content=True,
            has_tool_call=False,
        )

        with caplog.at_level(logging.DEBUG, logger="forge_llm"):
            await observer.on_event(event)

        assert "req_abc123" in caplog.text
        assert "Stream chunk" in caplog.text

    def test_custom_logger(self) -> None:
        """Deve aceitar logger customizado."""
        custom_logger = logging.getLogger("custom_app")
        observer = LoggingObserver(logger=custom_logger)

        assert observer._logger == custom_logger


class TestMetricsObserver:
    """Testes para MetricsObserver."""

    @pytest.mark.asyncio
    async def test_contagem_requests(self) -> None:
        """Deve contar requests."""
        observer = MetricsObserver()

        for _ in range(3):
            event = ChatStartEvent(
                timestamp=datetime.now(),
                request_id="req_abc123",
                provider="openai",
                model="gpt-4",
                message_count=1,
                has_tools=False,
            )
            await observer.on_event(event)

        assert observer.metrics.total_requests == 3

    @pytest.mark.asyncio
    async def test_contagem_tokens(self) -> None:
        """Deve contar tokens."""
        observer = MetricsObserver()

        event = ChatCompleteEvent(
            timestamp=datetime.now(),
            request_id="req_abc123",
            provider="openai",
            model="gpt-4",
            latency_ms=245.5,
            token_usage=TokenUsage(prompt_tokens=100, completion_tokens=50, total_tokens=150),
            finish_reason="stop",
            tool_calls_count=0,
        )
        await observer.on_event(event)

        assert observer.metrics.total_tokens == 150
        assert observer.metrics.total_prompt_tokens == 100
        assert observer.metrics.total_completion_tokens == 50

    @pytest.mark.asyncio
    async def test_requests_por_provider(self) -> None:
        """Deve agrupar requests por provider."""
        observer = MetricsObserver()

        # 2 requests openai
        for _ in range(2):
            event = ChatStartEvent(
                timestamp=datetime.now(),
                request_id="req_abc123",
                provider="openai",
                model="gpt-4",
                message_count=1,
                has_tools=False,
            )
            await observer.on_event(event)

        # 1 request anthropic
        event = ChatStartEvent(
            timestamp=datetime.now(),
            request_id="req_abc123",
            provider="anthropic",
            model="claude-3",
            message_count=1,
            has_tools=False,
        )
        await observer.on_event(event)

        assert observer.metrics.requests_by_provider["openai"] == 2
        assert observer.metrics.requests_by_provider["anthropic"] == 1

    @pytest.mark.asyncio
    async def test_tokens_por_provider(self) -> None:
        """Deve agrupar tokens por provider."""
        observer = MetricsObserver()

        event1 = ChatCompleteEvent(
            timestamp=datetime.now(),
            request_id="req_1",
            provider="openai",
            model="gpt-4",
            latency_ms=100.0,
            token_usage=TokenUsage(prompt_tokens=50, completion_tokens=25, total_tokens=75),
            finish_reason="stop",
            tool_calls_count=0,
        )
        await observer.on_event(event1)

        event2 = ChatCompleteEvent(
            timestamp=datetime.now(),
            request_id="req_2",
            provider="anthropic",
            model="claude-3",
            latency_ms=150.0,
            token_usage=TokenUsage(prompt_tokens=100, completion_tokens=50, total_tokens=150),
            finish_reason="stop",
            tool_calls_count=0,
        )
        await observer.on_event(event2)

        assert observer.metrics.tokens_by_provider["openai"] == 75
        assert observer.metrics.tokens_by_provider["anthropic"] == 150

    @pytest.mark.asyncio
    async def test_contagem_erros(self) -> None:
        """Deve contar erros por tipo."""
        observer = MetricsObserver()

        # 2 RateLimitError
        for _ in range(2):
            event = ChatErrorEvent(
                timestamp=datetime.now(),
                request_id="req_abc123",
                provider="openai",
                error_type="RateLimitError",
                error_message="Rate limit",
                latency_ms=50.0,
                retryable=True,
            )
            await observer.on_event(event)

        # 1 AuthenticationError
        event = ChatErrorEvent(
            timestamp=datetime.now(),
            request_id="req_abc123",
            provider="openai",
            error_type="AuthenticationError",
            error_message="Invalid key",
            latency_ms=10.0,
            retryable=False,
        )
        await observer.on_event(event)

        assert observer.metrics.total_errors == 3
        assert observer.metrics.errors_by_type["RateLimitError"] == 2
        assert observer.metrics.errors_by_type["AuthenticationError"] == 1

    @pytest.mark.asyncio
    async def test_contagem_retries(self) -> None:
        """Deve contar retries."""
        observer = MetricsObserver()

        for _ in range(3):
            event = RetryEvent(
                timestamp=datetime.now(),
                request_id="req_abc123",
                provider="openai",
                attempt=1,
                max_attempts=3,
                delay_ms=1000.0,
                error_type="RateLimitError",
            )
            await observer.on_event(event)

        assert observer.metrics.total_retries == 3

    @pytest.mark.asyncio
    async def test_latencia_media(self) -> None:
        """Deve calcular latencia media."""
        observer = MetricsObserver()

        latencies = [100.0, 200.0, 300.0]
        for lat in latencies:
            event = ChatCompleteEvent(
                timestamp=datetime.now(),
                request_id="req_abc123",
                provider="openai",
                model="gpt-4",
                latency_ms=lat,
                token_usage=TokenUsage(prompt_tokens=10, completion_tokens=10, total_tokens=20),
                finish_reason="stop",
                tool_calls_count=0,
            )
            await observer.on_event(event)

        assert observer.metrics.avg_latency_ms == 200.0  # (100+200+300)/3

    def test_latencia_media_sem_dados(self) -> None:
        """Latencia media deve ser 0 sem dados."""
        observer = MetricsObserver()

        assert observer.metrics.avg_latency_ms == 0.0

    def test_reset_metrics(self) -> None:
        """Deve resetar metricas."""
        observer = MetricsObserver()
        observer._metrics.total_requests = 10
        observer._metrics.total_tokens = 1000

        observer.reset()

        assert observer.metrics.total_requests == 0
        assert observer.metrics.total_tokens == 0

    def test_metrics_to_dict(self) -> None:
        """Deve converter metricas para dict."""
        observer = MetricsObserver()
        observer._metrics.total_requests = 5
        observer._metrics.total_tokens = 100

        result = observer.metrics.to_dict()

        assert result["total_requests"] == 5
        assert result["total_tokens"] == 100
        assert "avg_latency_ms" in result


class TestCallbackObserver:
    """Testes para CallbackObserver."""

    @pytest.mark.asyncio
    async def test_callback_on_start(self) -> None:
        """Deve chamar callback on_start."""
        received: list[ChatStartEvent] = []

        async def on_start(event: ChatStartEvent) -> None:
            received.append(event)

        observer = CallbackObserver(on_start=on_start)

        event = ChatStartEvent(
            timestamp=datetime.now(),
            request_id="req_abc123",
            provider="openai",
            model="gpt-4",
            message_count=1,
            has_tools=False,
        )
        await observer.on_event(event)

        assert len(received) == 1
        assert received[0] == event

    @pytest.mark.asyncio
    async def test_callback_on_complete(self) -> None:
        """Deve chamar callback on_complete."""
        received: list[ChatCompleteEvent] = []

        async def on_complete(event: ChatCompleteEvent) -> None:
            received.append(event)

        observer = CallbackObserver(on_complete=on_complete)

        event = ChatCompleteEvent(
            timestamp=datetime.now(),
            request_id="req_abc123",
            provider="openai",
            model="gpt-4",
            latency_ms=100.0,
            token_usage=TokenUsage(prompt_tokens=10, completion_tokens=10, total_tokens=20),
            finish_reason="stop",
            tool_calls_count=0,
        )
        await observer.on_event(event)

        assert len(received) == 1

    @pytest.mark.asyncio
    async def test_callback_on_error(self) -> None:
        """Deve chamar callback on_error."""
        received: list[ChatErrorEvent] = []

        async def on_error(event: ChatErrorEvent) -> None:
            received.append(event)

        observer = CallbackObserver(on_error=on_error)

        event = ChatErrorEvent(
            timestamp=datetime.now(),
            request_id="req_abc123",
            provider="openai",
            error_type="RateLimitError",
            error_message="Rate limit",
            latency_ms=50.0,
            retryable=True,
        )
        await observer.on_event(event)

        assert len(received) == 1

    @pytest.mark.asyncio
    async def test_callback_on_retry(self) -> None:
        """Deve chamar callback on_retry."""
        received: list[RetryEvent] = []

        async def on_retry(event: RetryEvent) -> None:
            received.append(event)

        observer = CallbackObserver(on_retry=on_retry)

        event = RetryEvent(
            timestamp=datetime.now(),
            request_id="req_abc123",
            provider="openai",
            attempt=1,
            max_attempts=3,
            delay_ms=1000.0,
            error_type="RateLimitError",
        )
        await observer.on_event(event)

        assert len(received) == 1

    @pytest.mark.asyncio
    async def test_callback_on_stream_chunk(self) -> None:
        """Deve chamar callback on_stream_chunk."""
        received: list[StreamChunkEvent] = []

        async def on_chunk(event: StreamChunkEvent) -> None:
            received.append(event)

        observer = CallbackObserver(on_stream_chunk=on_chunk)

        event = StreamChunkEvent(
            timestamp=datetime.now(),
            request_id="req_abc123",
            provider="openai",
            chunk_index=0,
            has_content=True,
            has_tool_call=False,
        )
        await observer.on_event(event)

        assert len(received) == 1

    @pytest.mark.asyncio
    async def test_sem_callback(self) -> None:
        """Deve funcionar sem callbacks definidos."""
        observer = CallbackObserver()

        event = ChatStartEvent(
            timestamp=datetime.now(),
            request_id="req_abc123",
            provider="openai",
            model="gpt-4",
            message_count=1,
            has_tools=False,
        )

        # Nao deve lancar excecao
        await observer.on_event(event)

    @pytest.mark.asyncio
    async def test_multiplos_callbacks(self) -> None:
        """Deve suportar multiplos callbacks."""
        starts: list[ChatStartEvent] = []
        completes: list[ChatCompleteEvent] = []

        async def on_start(event: ChatStartEvent) -> None:
            starts.append(event)

        async def on_complete(event: ChatCompleteEvent) -> None:
            completes.append(event)

        observer = CallbackObserver(on_start=on_start, on_complete=on_complete)

        start_event = ChatStartEvent(
            timestamp=datetime.now(),
            request_id="req_abc123",
            provider="openai",
            model="gpt-4",
            message_count=1,
            has_tools=False,
        )
        await observer.on_event(start_event)

        complete_event = ChatCompleteEvent(
            timestamp=datetime.now(),
            request_id="req_abc123",
            provider="openai",
            model="gpt-4",
            latency_ms=100.0,
            token_usage=TokenUsage(prompt_tokens=10, completion_tokens=10, total_tokens=20),
            finish_reason="stop",
            tool_calls_count=0,
        )
        await observer.on_event(complete_event)

        assert len(starts) == 1
        assert len(completes) == 1
