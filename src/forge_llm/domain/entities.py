"""Entidades de dominio do ForgeLLMClient."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import uuid4

from forge_llm.domain.exceptions import ValidationError
from forge_llm.domain.value_objects import Message, TokenUsage


@dataclass
class ToolCall:
    """Chamada de ferramenta solicitada pelo LLM."""

    name: str
    arguments: dict[str, Any]
    id: str | None = None

    def __post_init__(self) -> None:
        """Validar e gerar id se necessario."""
        if self.id is None:
            self.id = f"call_{uuid4().hex[:12]}"
        self._validate()

    def _validate(self) -> None:
        """Validar invariantes."""
        if not self.name:
            raise ValidationError("Nome da tool e obrigatorio")
        if not isinstance(self.arguments, dict):
            raise ValidationError("Argumentos devem ser um dicionario")

    def to_dict(self) -> dict[str, Any]:
        """Converter para dicionario."""
        return {
            "id": self.id,
            "name": self.name,
            "arguments": self.arguments,
        }


@dataclass
class ChatResponse:
    """
    Resposta de chat de um provedor LLM.

    Representa uma resposta completa (nao streaming).
    """

    content: str
    model: str
    provider: str
    usage: TokenUsage
    tool_calls: list[ToolCall] = field(default_factory=list)
    finish_reason: str = "stop"
    id: str | None = None
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        """Validar apos inicializacao."""
        if self.id is None:
            self.id = f"resp_{uuid4().hex[:12]}"
        self._validate()

    def _validate(self) -> None:
        """Validar invariantes da resposta."""
        if not self.model:
            raise ValidationError("Modelo e obrigatorio")
        if not self.provider:
            raise ValidationError("Provider e obrigatorio")

    @property
    def has_tool_calls(self) -> bool:
        """Indica se resposta contem tool calls."""
        return len(self.tool_calls) > 0


class Conversation:
    """
    Gerencia historico de conversas multi-turn.

    Mantem o contexto entre mensagens e envia historico completo
    para o provider em cada chamada.

    Exemplo:
        conv = Conversation(client, system="Voce e um assistente")
        response = await conv.chat("Ola!")
        response = await conv.chat("Qual foi minha primeira mensagem?")
    """

    def __init__(
        self,
        client: Any,
        system: str | None = None,
        max_messages: int | None = None,
    ) -> None:
        """
        Inicializar conversa.

        Args:
            client: Cliente configurado para fazer chamadas
            system: System prompt opcional
            max_messages: Limite maximo de mensagens no historico (None = sem limite)
        """
        self._client = client
        self._system_prompt = system
        self._max_messages = max_messages
        self._messages: list[Message] = []

    @property
    def system_prompt(self) -> str | None:
        """Retorna o system prompt da conversa."""
        return self._system_prompt

    @property
    def messages(self) -> list[Message]:
        """Retorna copia das mensagens do historico."""
        return self._messages.copy()

    @property
    def message_count(self) -> int:
        """Retorna quantidade de mensagens no historico."""
        return len(self._messages)

    @property
    def max_messages(self) -> int | None:
        """Retorna limite maximo de mensagens."""
        return self._max_messages

    def is_empty(self) -> bool:
        """Indica se a conversa esta vazia."""
        return len(self._messages) == 0

    def _trim_messages(self) -> None:
        """Remove mensagens antigas se exceder max_messages."""
        if self._max_messages is not None and len(self._messages) > self._max_messages:
            # Remove mensagens mais antigas, mantendo as mais recentes
            self._messages = self._messages[-self._max_messages:]

    def add_user_message(self, content: str) -> None:
        """
        Adiciona mensagem do usuario ao historico.

        Args:
            content: Conteudo da mensagem
        """
        self._messages.append(Message(role="user", content=content))
        self._trim_messages()

    def add_assistant_message(self, content: str) -> None:
        """
        Adiciona mensagem do assistant ao historico.

        Args:
            content: Conteudo da mensagem
        """
        self._messages.append(Message(role="assistant", content=content))
        self._trim_messages()

    def get_messages_for_api(self) -> list[Message]:
        """
        Retorna mensagens formatadas para envio a API.

        Inclui system prompt como primeira mensagem se definido.
        """
        messages: list[Message] = []
        if self._system_prompt:
            messages.append(Message(role="system", content=self._system_prompt))
        messages.extend(self._messages)
        return messages

    def clear(self) -> None:
        """Limpa o historico de mensagens, mantendo system prompt."""
        self._messages.clear()

    async def chat(
        self,
        message: str,
        **kwargs: Any,
    ) -> ChatResponse:
        """
        Envia mensagem e recebe resposta, mantendo contexto.

        Args:
            message: Mensagem do usuario
            **kwargs: Argumentos adicionais para o provider

        Returns:
            ChatResponse com a resposta
        """
        # Adicionar mensagem do usuario
        self.add_user_message(message)

        # Obter mensagens para API
        messages = self.get_messages_for_api()

        # Fazer chamada via client
        response = await self._client.chat(messages, **kwargs)

        # Adicionar resposta ao historico
        self.add_assistant_message(response.content)

        return response
