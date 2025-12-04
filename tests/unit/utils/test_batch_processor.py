"""Tests for BatchProcessor."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from forge_llm.domain.entities import ChatResponse
from forge_llm.domain.value_objects import Message, TokenUsage
from forge_llm.utils.batch_processor import BatchProcessor


def _create_mock_response(content: str) -> ChatResponse:
    """Helper para criar ChatResponse."""
    return ChatResponse(
        content=content,
        model="test-model",
        provider="test",
        usage=TokenUsage(prompt_tokens=10, completion_tokens=5),
        tool_calls=[],
        finish_reason="stop",
    )


@pytest.fixture
def mock_provider():
    """Fixture para criar mock provider."""
    provider = MagicMock()
    provider.chat = AsyncMock()
    return provider


class TestBatchProcessorBasics:
    """Testes basicos para BatchProcessor."""

    def test_processor_creation(self, mock_provider):
        """BatchProcessor deve ser criado com provider."""
        processor = BatchProcessor(mock_provider)
        assert processor.provider == mock_provider
        assert processor.max_concurrent == 5

    def test_processor_custom_concurrency(self, mock_provider):
        """BatchProcessor deve aceitar concorrencia customizada."""
        processor = BatchProcessor(mock_provider, max_concurrent=10)
        assert processor.max_concurrent == 10


class TestBatchProcessorProcess:
    """Testes do metodo process."""

    @pytest.mark.asyncio
    async def test_process_single_batch(self, mock_provider):
        """Deve processar um unico batch."""
        mock_provider.chat.return_value = _create_mock_response("Response 1")
        processor = BatchProcessor(mock_provider)

        batches = [[Message(role="user", content="Hello")]]
        results = await processor.process(batches)

        assert len(results) == 1
        assert results[0].content == "Response 1"
        mock_provider.chat.assert_called_once()

    @pytest.mark.asyncio
    async def test_process_multiple_batches(self, mock_provider):
        """Deve processar multiplos batches."""
        mock_provider.chat.side_effect = [
            _create_mock_response("Response 1"),
            _create_mock_response("Response 2"),
            _create_mock_response("Response 3"),
        ]
        processor = BatchProcessor(mock_provider)

        batches = [
            [Message(role="user", content="Q1")],
            [Message(role="user", content="Q2")],
            [Message(role="user", content="Q3")],
        ]
        results = await processor.process(batches)

        assert len(results) == 3
        assert mock_provider.chat.call_count == 3

    @pytest.mark.asyncio
    async def test_process_empty_batches(self, mock_provider):
        """Lista vazia deve retornar lista vazia."""
        processor = BatchProcessor(mock_provider)
        results = await processor.process([])
        assert results == []

    @pytest.mark.asyncio
    async def test_process_passes_kwargs(self, mock_provider):
        """Deve passar kwargs para provider."""
        mock_provider.chat.return_value = _create_mock_response("Response")
        processor = BatchProcessor(mock_provider)

        batches = [[Message(role="user", content="Hello")]]
        await processor.process(batches, model="gpt-4", temperature=0.5)

        mock_provider.chat.assert_called_with(
            batches[0],
            model="gpt-4",
            temperature=0.5,
        )


class TestBatchProcessorErrorHandling:
    """Testes de tratamento de erros."""

    @pytest.mark.asyncio
    async def test_process_returns_exceptions(self, mock_provider):
        """Deve retornar excecoes em vez de lancar."""
        error = Exception("API Error")
        mock_provider.chat.side_effect = [
            _create_mock_response("Success"),
            error,
            _create_mock_response("Success 2"),
        ]
        processor = BatchProcessor(mock_provider)

        batches = [
            [Message(role="user", content="Q1")],
            [Message(role="user", content="Q2")],
            [Message(role="user", content="Q3")],
        ]
        results = await processor.process(batches)

        assert len(results) == 3
        assert results[0].content == "Success"
        assert isinstance(results[1], Exception)
        assert results[2].content == "Success 2"


class TestBatchProcessorConcurrency:
    """Testes de concorrencia."""

    @pytest.mark.asyncio
    async def test_respects_max_concurrent(self, mock_provider):
        """Deve respeitar limite de concorrencia."""
        call_count = 0
        max_concurrent_seen = 0
        current_concurrent = 0

        async def track_concurrent(*args, **kwargs):
            nonlocal call_count, max_concurrent_seen, current_concurrent
            call_count += 1
            current_concurrent += 1
            max_concurrent_seen = max(max_concurrent_seen, current_concurrent)
            # Simular delay
            import asyncio
            await asyncio.sleep(0.01)
            current_concurrent -= 1
            return _create_mock_response(f"Response {call_count}")

        mock_provider.chat.side_effect = track_concurrent
        processor = BatchProcessor(mock_provider, max_concurrent=2)

        batches = [[Message(role="user", content=f"Q{i}")] for i in range(5)]
        await processor.process(batches)

        assert call_count == 5
        assert max_concurrent_seen <= 2


class TestBatchProcessorWithCallback:
    """Testes com callback."""

    @pytest.mark.asyncio
    async def test_process_with_callback_called(self, mock_provider):
        """Callback deve ser chamado para cada resultado."""
        mock_provider.chat.side_effect = [
            _create_mock_response("R1"),
            _create_mock_response("R2"),
        ]
        processor = BatchProcessor(mock_provider)

        callback_results = []

        async def callback(index, result):
            callback_results.append((index, result))

        batches = [
            [Message(role="user", content="Q1")],
            [Message(role="user", content="Q2")],
        ]
        await processor.process_with_callback(batches, callback)

        assert len(callback_results) == 2
        # Indices podem vir em qualquer ordem devido async
        indices = {r[0] for r in callback_results}
        assert indices == {0, 1}

    @pytest.mark.asyncio
    async def test_process_with_callback_on_error(self, mock_provider):
        """Callback deve receber excecoes tambem."""
        error = Exception("Error")
        mock_provider.chat.side_effect = [
            _create_mock_response("Success"),
            error,
        ]
        processor = BatchProcessor(mock_provider)

        callback_results = []

        async def callback(index, result):
            callback_results.append((index, result))

        batches = [
            [Message(role="user", content="Q1")],
            [Message(role="user", content="Q2")],
        ]
        await processor.process_with_callback(batches, callback)

        # Deve ter chamado callback para ambos
        assert len(callback_results) == 2
        # Um deve ser excecao
        exceptions = [r for r in callback_results if isinstance(r[1], Exception)]
        assert len(exceptions) == 1
