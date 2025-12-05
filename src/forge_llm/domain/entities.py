"""Entidades de dominio do ForgeLLMClient."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import TYPE_CHECKING, Any
from uuid import uuid4

from forge_llm.domain.exceptions import ValidationError
from forge_llm.domain.value_objects import (
    EnhancedMessage,
    Message,
    MessageMetadata,
    TokenUsage,
)

if TYPE_CHECKING:
    from forge_llm.application.ports.provider_port import ProviderPort


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

    Suporta:
    - Limite por contagem de mensagens (max_messages)
    - Limite por tokens (max_tokens) - requer model
    - Hot-swap de provider mid-conversation
    - Metadados por mensagem (timestamp, provider, model)
    - Serializacao para persistencia

    Exemplo:
        conv = Conversation(client, system="Voce e um assistente")
        response = await conv.chat("Ola!")
        response = await conv.chat("Qual foi minha primeira mensagem?")

    Com Hot-swap:
        conv = Conversation(client, system="Assistente")
        await conv.chat("Ola!")
        conv.change_provider("anthropic", api_key="sk-ant-...")
        await conv.chat("Continue")  # Usa novo provider
    """

    def __init__(
        self,
        client: Any,
        system: str | None = None,
        max_messages: int | None = None,
        max_tokens: int | None = None,
        model: str | None = None,
    ) -> None:
        """
        Inicializar conversa.

        Args:
            client: Cliente configurado para fazer chamadas
            system: System prompt opcional
            max_messages: Limite maximo de mensagens no historico (None = sem limite)
            max_tokens: Limite maximo de tokens no historico (None = sem limite)
            model: Modelo para contagem de tokens (requerido se max_tokens)
        """
        self._client = client
        self._system_prompt = system
        self._max_messages = max_messages
        self._max_tokens = max_tokens
        self._model = model
        self._messages: list[EnhancedMessage] = []
        self._provider_history: list[str] = []
        self._last_provider: str | None = None
        self._last_model: str | None = None
        self._token_counter: Any = None

        # Inicializar token counter se max_tokens definido
        if max_tokens is not None:
            self._init_token_counter()

    def _init_token_counter(self) -> None:
        """Inicializar contador de tokens."""
        try:
            from forge_llm.utils.token_counter import TokenCounter

            model = self._model or "gpt-4o-mini"
            self._token_counter = TokenCounter(model=model)
        except ImportError:
            self._token_counter = None

    @property
    def system_prompt(self) -> str | None:
        """Retorna o system prompt da conversa."""
        return self._system_prompt

    @property
    def messages(self) -> list[Message]:
        """Retorna copia das mensagens do historico (sem metadados)."""
        return [em.message for em in self._messages]

    @property
    def enhanced_messages(self) -> list[EnhancedMessage]:
        """Retorna copia das mensagens com metadados."""
        return self._messages.copy()

    @property
    def message_count(self) -> int:
        """Retorna quantidade de mensagens no historico."""
        return len(self._messages)

    @property
    def max_messages(self) -> int | None:
        """Retorna limite maximo de mensagens."""
        return self._max_messages

    @property
    def max_tokens(self) -> int | None:
        """Retorna limite maximo de tokens."""
        return self._max_tokens

    @property
    def token_count(self) -> int:
        """Retorna contagem atual de tokens no historico."""
        if self._token_counter is None:
            return 0

        messages = [em.message for em in self._messages]
        count: int = self._token_counter.count_messages(messages)

        if self._system_prompt:
            count += self._token_counter.count_text(self._system_prompt)
            count += self._token_counter.MESSAGE_OVERHEAD

        return count

    @property
    def last_provider(self) -> str | None:
        """Retorna ultimo provider usado."""
        return self._last_provider

    @property
    def last_model(self) -> str | None:
        """Retorna ultimo modelo usado."""
        return self._last_model

    @property
    def provider_history(self) -> list[str]:
        """Retorna historico de providers usados."""
        return self._provider_history.copy()

    def is_empty(self) -> bool:
        """Indica se a conversa esta vazia."""
        return len(self._messages) == 0

    def _trim_messages(self) -> None:
        """Remove mensagens antigas se exceder limites."""
        # Trim por contagem
        if self._max_messages is not None and len(self._messages) > self._max_messages:
            self._messages = self._messages[-self._max_messages :]

        # Trim por tokens (com protecao contra loop infinito)
        if self._max_tokens is not None and self._token_counter is not None:
            max_iterations = len(self._messages)
            iterations = 0
            while self.token_count > self._max_tokens and len(self._messages) > 1:
                if iterations >= max_iterations:
                    break  # Protecao contra loop infinito
                self._messages.pop(0)
                iterations += 1

    def add_user_message(
        self,
        content: str,
        provider: str | None = None,
        model: str | None = None,
    ) -> None:
        """
        Adiciona mensagem do usuario ao historico.

        Args:
            content: Conteudo da mensagem
            provider: Provider atual (opcional)
            model: Modelo atual (opcional)
        """
        message = Message(role="user", content=content)
        metadata = MessageMetadata(
            timestamp=datetime.now(),
            provider=provider,
            model=model,
        )
        self._messages.append(EnhancedMessage(message=message, metadata=metadata))
        self._trim_messages()

    def add_assistant_message(
        self,
        content: str,
        provider: str | None = None,
        model: str | None = None,
    ) -> None:
        """
        Adiciona mensagem do assistant ao historico.

        Args:
            content: Conteudo da mensagem
            provider: Provider que gerou a resposta
            model: Modelo que gerou a resposta
        """
        message = Message(role="assistant", content=content)
        metadata = MessageMetadata(
            timestamp=datetime.now(),
            provider=provider,
            model=model,
        )
        self._messages.append(EnhancedMessage(message=message, metadata=metadata))
        self._trim_messages()

        # Atualizar tracking
        if provider:
            self._last_provider = provider
            if provider not in self._provider_history:
                self._provider_history.append(provider)
        if model:
            self._last_model = model

    def get_messages_for_api(self) -> list[Message]:
        """
        Retorna mensagens formatadas para envio a API.

        Inclui system prompt como primeira mensagem se definido.
        """
        messages: list[Message] = []
        if self._system_prompt:
            messages.append(Message(role="system", content=self._system_prompt))
        messages.extend(em.message for em in self._messages)
        return messages

    def clear(self) -> None:
        """Limpa o historico de mensagens, mantendo system prompt."""
        self._messages.clear()

    def change_provider(
        self,
        provider: str | ProviderPort,
        api_key: str | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Trocar provider mid-conversation (hot-swap).

        O historico de mensagens e preservado.

        Args:
            provider: Nome do provider ou instancia de ProviderPort
            api_key: API key para o novo provider
            **kwargs: Argumentos adicionais para o provider
        """
        self._client.configure(provider, api_key=api_key, **kwargs)

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

        Raises:
            ConfigurationError: Se o client nao esta configurado
        """
        # Validar que client esta configurado
        if not self._client.is_configured:
            from forge_llm.domain.exceptions import ConfigurationError

            raise ConfigurationError("Client não está configurado para chat")

        # Obter info do provider atual
        current_provider = self._client.provider_name
        current_model = self._client.model

        # Adicionar mensagem do usuario
        self.add_user_message(
            content=message,
            provider=current_provider,
            model=current_model,
        )

        # Obter mensagens para API
        messages = self.get_messages_for_api()

        # Fazer chamada via client
        response: ChatResponse = await self._client.chat(messages, **kwargs)

        # Adicionar resposta ao historico com metadados
        self.add_assistant_message(
            content=response.content,
            provider=response.provider,
            model=response.model,
        )

        return response

    def to_dict(self) -> dict[str, Any]:
        """
        Serializar conversa para dicionario.

        Returns:
            Dicionario com estado completo da conversa
        """
        return {
            "system_prompt": self._system_prompt,
            "max_messages": self._max_messages,
            "max_tokens": self._max_tokens,
            "model": self._model,
            "messages": [em.to_dict() for em in self._messages],
            "provider_history": self._provider_history,
            "last_provider": self._last_provider,
            "last_model": self._last_model,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any], client: Any) -> Conversation:
        """
        Restaurar conversa a partir de dicionario.

        Args:
            data: Dicionario serializado
            client: Cliente configurado

        Returns:
            Conversa restaurada

        Raises:
            ValidationError: Se client não implementa interface necessária
        """
        # Validar que client implementa interface necessária
        if not hasattr(client, "chat") or not hasattr(client, "configure"):
            raise ValidationError("Client deve implementar interface Client (chat, configure)")

        conv = cls(
            client=client,
            system=data.get("system_prompt"),
            max_messages=data.get("max_messages"),
            max_tokens=data.get("max_tokens"),
            model=data.get("model"),
        )

        # Restaurar mensagens
        for msg_data in data.get("messages", []):
            enhanced = EnhancedMessage.from_dict(msg_data)
            conv._messages.append(enhanced)

        # Restaurar tracking
        conv._provider_history = data.get("provider_history", [])
        conv._last_provider = data.get("last_provider")
        conv._last_model = data.get("last_model")

        return conv
