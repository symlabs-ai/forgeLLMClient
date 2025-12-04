"""Batch Processor - Processamento paralelo de multiplas requests."""

import asyncio
from typing import Any

from forge_llm.application.ports.provider_port import ProviderPort
from forge_llm.domain.entities import ChatResponse
from forge_llm.domain.value_objects import Message


class BatchProcessor:
    """
    Processador de requests em lote com controle de concorrencia.

    Permite enviar multiplas requests em paralelo respeitando
    um limite de concorrencia.

    Exemplo:
        processor = BatchProcessor(provider, max_concurrent=5)
        results = await processor.process([
            [Message(role="user", content="Question 1")],
            [Message(role="user", content="Question 2")],
            [Message(role="user", content="Question 3")],
        ])
    """

    def __init__(
        self,
        provider: ProviderPort,
        max_concurrent: int = 5,
    ) -> None:
        """
        Inicializar BatchProcessor.

        Args:
            provider: Provider para fazer as requests
            max_concurrent: Numero maximo de requests simultaneas
        """
        self._provider = provider
        self._max_concurrent = max_concurrent

    async def process(
        self,
        message_batches: list[list[Message]],
        **kwargs: Any,
    ) -> list[ChatResponse | Exception]:
        """
        Processar multiplos batches de mensagens em paralelo.

        Args:
            message_batches: Lista de listas de mensagens
            **kwargs: Argumentos extras para chat()

        Returns:
            Lista de respostas ou excecoes na mesma ordem dos inputs
        """
        semaphore = asyncio.Semaphore(self._max_concurrent)
        tasks = [
            self._process_one(messages, semaphore, **kwargs)
            for messages in message_batches
        ]
        return await asyncio.gather(*tasks, return_exceptions=True)

    async def _process_one(
        self,
        messages: list[Message],
        semaphore: asyncio.Semaphore,
        **kwargs: Any,
    ) -> ChatResponse:
        """
        Processar um batch com controle de semaforo.

        Args:
            messages: Lista de mensagens
            semaphore: Semaforo para controle de concorrencia
            **kwargs: Argumentos extras para chat()

        Returns:
            Resposta do chat
        """
        async with semaphore:
            return await self._provider.chat(messages, **kwargs)

    async def process_with_callback(
        self,
        message_batches: list[list[Message]],
        callback: Any,
        **kwargs: Any,
    ) -> list[ChatResponse | Exception]:
        """
        Processar batches com callback para cada resultado.

        Args:
            message_batches: Lista de listas de mensagens
            callback: Funcao async chamada com (index, result) apos cada request
            **kwargs: Argumentos extras para chat()

        Returns:
            Lista de respostas ou excecoes
        """
        semaphore = asyncio.Semaphore(self._max_concurrent)
        results: list[ChatResponse | Exception] = [
            Exception("Not processed")
        ] * len(message_batches)

        async def process_with_index(index: int, messages: list[Message]) -> None:
            async with semaphore:
                try:
                    result = await self._provider.chat(messages, **kwargs)
                    results[index] = result
                    if callback:
                        await callback(index, result)
                except Exception as e:
                    results[index] = e
                    if callback:
                        await callback(index, e)

        tasks = [
            process_with_index(i, messages)
            for i, messages in enumerate(message_batches)
        ]
        await asyncio.gather(*tasks)
        return results

    @property
    def max_concurrent(self) -> int:
        """Limite de concorrencia."""
        return self._max_concurrent

    @property
    def provider(self) -> ProviderPort:
        """Provider configurado."""
        return self._provider
