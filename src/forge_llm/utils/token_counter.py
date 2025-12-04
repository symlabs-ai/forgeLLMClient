"""Token Counter - Contagem de tokens para mensagens."""

from typing import Any

import tiktoken

from forge_llm.domain.value_objects import Message


class TokenCounter:
    """
    Contador de tokens para mensagens.

    Usa tiktoken para contagem precisa de tokens compativel com modelos OpenAI.
    Para outros providers, a contagem e aproximada.

    Exemplo:
        counter = TokenCounter(model="gpt-4o-mini")
        count = counter.count_text("Hello world")
        count = counter.count_messages([Message(role="user", content="Hi")])
    """

    # Overhead de tokens por mensagem (role, delimitadores, etc)
    MESSAGE_OVERHEAD = 4

    # Mapeamento de modelos para encodings
    MODEL_ENCODINGS = {
        "gpt-4o": "o200k_base",
        "gpt-4o-mini": "o200k_base",
        "gpt-4-turbo": "cl100k_base",
        "gpt-4": "cl100k_base",
        "gpt-3.5-turbo": "cl100k_base",
        "claude": "cl100k_base",  # Aproximacao
    }

    def __init__(self, model: str = "gpt-4o-mini") -> None:
        """
        Inicializar TokenCounter.

        Args:
            model: Nome do modelo para encoding de tokens
        """
        self._model = model
        self._encoding = self._get_encoding(model)

    def _get_encoding(self, model: str) -> tiktoken.Encoding:
        """
        Obter encoding apropriado para o modelo.

        Args:
            model: Nome do modelo

        Returns:
            Encoding do tiktoken
        """
        # Tentar encontrar encoding especifico
        for prefix, encoding_name in self.MODEL_ENCODINGS.items():
            if model.startswith(prefix):
                return tiktoken.get_encoding(encoding_name)

        # Fallback para cl100k_base (GPT-4 style)
        try:
            return tiktoken.encoding_for_model(model)
        except KeyError:
            return tiktoken.get_encoding("cl100k_base")

    def count_text(self, text: str) -> int:
        """
        Contar tokens em um texto.

        Args:
            text: Texto para contar

        Returns:
            Numero de tokens
        """
        if not text:
            return 0
        return len(self._encoding.encode(text))

    def count_messages(self, messages: list[Message]) -> int:
        """
        Contar tokens em lista de mensagens.

        Args:
            messages: Lista de mensagens

        Returns:
            Total de tokens (incluindo overhead)
        """
        total = 0
        for msg in messages:
            content = self._extract_content(msg.content)
            total += self.count_text(content)
            total += self.MESSAGE_OVERHEAD
        return total

    def _extract_content(self, content: str | list[Any]) -> str:
        """
        Extrair texto de conteudo que pode ser string ou lista.

        Args:
            content: Conteudo da mensagem

        Returns:
            Texto extraido
        """
        if isinstance(content, str):
            return content

        # Lista com texto e imagens
        texts = []
        for item in content:
            if isinstance(item, str):
                texts.append(item)
            elif hasattr(item, "text"):
                texts.append(item.text)
        return " ".join(texts)

    def estimate_remaining(
        self,
        messages: list[Message],
        max_tokens: int,
    ) -> int:
        """
        Estimar tokens restantes para resposta.

        Args:
            messages: Lista de mensagens
            max_tokens: Limite total de tokens do contexto

        Returns:
            Tokens disponiveis para resposta
        """
        used = self.count_messages(messages)
        return max(0, max_tokens - used)

    @property
    def model(self) -> str:
        """Modelo configurado."""
        return self._model
