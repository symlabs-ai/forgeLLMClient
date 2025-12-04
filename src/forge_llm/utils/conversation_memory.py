"""Conversation Memory - Gerenciamento de historico de mensagens."""

from forge_llm.domain.value_objects import Message
from forge_llm.utils.token_counter import TokenCounter


class ConversationMemory:
    """
    Gerenciador de historico de conversa com truncamento automatico.

    Mantém mensagens dentro de um limite de tokens, removendo as mais antigas
    quando necessário.

    Exemplo:
        memory = ConversationMemory(max_tokens=4000)
        memory.add(Message(role="user", content="Hello"))
        memory.add(Message(role="assistant", content="Hi!"))
        messages = memory.get_messages()
    """

    def __init__(
        self,
        max_tokens: int = 4000,
        model: str = "gpt-4o-mini",
        system_message: str | None = None,
    ) -> None:
        """
        Inicializar ConversationMemory.

        Args:
            max_tokens: Limite maximo de tokens para mensagens
            model: Modelo para contagem de tokens
            system_message: Mensagem de sistema opcional
        """
        self._max_tokens = max_tokens
        self._counter = TokenCounter(model)
        self._system = system_message
        self._messages: list[Message] = []

    def add(self, message: Message) -> None:
        """
        Adicionar mensagem ao historico.

        Trunca automaticamente mensagens antigas se exceder o limite.

        Args:
            message: Mensagem a adicionar
        """
        self._messages.append(message)
        self._truncate_if_needed()

    def add_user(self, content: str) -> None:
        """
        Adicionar mensagem de usuario.

        Args:
            content: Conteudo da mensagem
        """
        self.add(Message(role="user", content=content))

    def add_assistant(self, content: str) -> None:
        """
        Adicionar mensagem de assistente.

        Args:
            content: Conteudo da mensagem
        """
        self.add(Message(role="assistant", content=content))

    def get_messages(self) -> list[Message]:
        """
        Obter todas as mensagens incluindo system message.

        Returns:
            Lista de mensagens prontas para enviar
        """
        result: list[Message] = []
        if self._system:
            result.append(Message(role="system", content=self._system))
        result.extend(self._messages)
        return result

    def _truncate_if_needed(self) -> None:
        """Truncar mensagens antigas se exceder limite de tokens."""
        # Calcular tokens do system message
        system_tokens = 0
        if self._system:
            system_tokens = self._counter.count_text(self._system)
            system_tokens += TokenCounter.MESSAGE_OVERHEAD

        available_tokens = self._max_tokens - system_tokens

        while (
            self._counter.count_messages(self._messages) > available_tokens
            and len(self._messages) > 1
        ):
            self._messages.pop(0)

    def clear(self) -> None:
        """Limpar todas as mensagens (exceto system)."""
        self._messages.clear()

    def set_system_message(self, message: str | None) -> None:
        """
        Definir mensagem de sistema.

        Args:
            message: Nova mensagem de sistema ou None para remover
        """
        self._system = message
        self._truncate_if_needed()

    @property
    def system_message(self) -> str | None:
        """Mensagem de sistema atual."""
        return self._system

    @property
    def token_count(self) -> int:
        """Total de tokens no historico (incluindo system)."""
        count = self._counter.count_messages(self._messages)
        if self._system:
            count += self._counter.count_text(self._system)
            count += TokenCounter.MESSAGE_OVERHEAD
        return count

    @property
    def max_tokens(self) -> int:
        """Limite maximo de tokens."""
        return self._max_tokens

    @property
    def message_count(self) -> int:
        """Numero de mensagens no historico (excluindo system)."""
        return len(self._messages)

    def __len__(self) -> int:
        """Numero de mensagens."""
        return len(self._messages)
