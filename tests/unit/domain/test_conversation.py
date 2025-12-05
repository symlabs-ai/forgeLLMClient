"""Testes para Conversation - Sprint 14 (Hot-Swap & Context Management)."""

from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

import pytest

from forge_llm.domain.entities import ChatResponse, Conversation
from forge_llm.domain.value_objects import (
    EnhancedMessage,
    Message,
    MessageMetadata,
    TokenUsage,
)


class TestMessageMetadata:
    """Testes para MessageMetadata value object."""

    def test_metadata_creation_with_defaults(self):
        """MessageMetadata deve ter timestamp automatico."""
        meta = MessageMetadata()
        assert isinstance(meta.timestamp, datetime)
        assert meta.provider is None
        assert meta.model is None

    def test_metadata_creation_with_values(self):
        """MessageMetadata deve aceitar valores explicitos."""
        ts = datetime(2025, 1, 1, 12, 0, 0)
        meta = MessageMetadata(
            timestamp=ts,
            provider="openai",
            model="gpt-4",
        )
        assert meta.timestamp == ts
        assert meta.provider == "openai"
        assert meta.model == "gpt-4"

    def test_metadata_to_dict(self):
        """MessageMetadata.to_dict deve serializar corretamente."""
        ts = datetime(2025, 1, 1, 12, 0, 0)
        meta = MessageMetadata(
            timestamp=ts,
            provider="openai",
            model="gpt-4",
        )
        d = meta.to_dict()
        assert d["timestamp"] == "2025-01-01T12:00:00"
        assert d["provider"] == "openai"
        assert d["model"] == "gpt-4"

    def test_metadata_from_dict(self):
        """MessageMetadata.from_dict deve deserializar corretamente."""
        data = {
            "timestamp": "2025-01-01T12:00:00",
            "provider": "anthropic",
            "model": "claude-3",
        }
        meta = MessageMetadata.from_dict(data)
        assert meta.timestamp == datetime(2025, 1, 1, 12, 0, 0)
        assert meta.provider == "anthropic"
        assert meta.model == "claude-3"

    def test_metadata_from_dict_with_missing_fields(self):
        """MessageMetadata.from_dict deve lidar com campos ausentes."""
        meta = MessageMetadata.from_dict({})
        assert isinstance(meta.timestamp, datetime)
        assert meta.provider is None
        assert meta.model is None

    def test_metadata_is_frozen(self):
        """MessageMetadata deve ser imutavel."""
        meta = MessageMetadata()
        with pytest.raises(AttributeError):
            meta.provider = "test"  # type: ignore


class TestEnhancedMessage:
    """Testes para EnhancedMessage value object."""

    def test_enhanced_message_creation(self):
        """EnhancedMessage deve combinar Message e Metadata."""
        msg = Message(role="user", content="Hello")
        meta = MessageMetadata(provider="openai")
        enhanced = EnhancedMessage(message=msg, metadata=meta)

        assert enhanced.message == msg
        assert enhanced.metadata == meta

    def test_enhanced_message_properties(self):
        """EnhancedMessage deve expor propriedades de conveniencia."""
        msg = Message(role="assistant", content="Hi there")
        meta = MessageMetadata(provider="anthropic", model="claude-3")
        enhanced = EnhancedMessage(message=msg, metadata=meta)

        assert enhanced.role == "assistant"
        assert enhanced.content == "Hi there"
        assert enhanced.provider == "anthropic"
        assert enhanced.model == "claude-3"

    def test_enhanced_message_to_dict(self):
        """EnhancedMessage.to_dict deve serializar corretamente."""
        msg = Message(role="user", content="Test")
        ts = datetime(2025, 1, 1)
        meta = MessageMetadata(timestamp=ts, provider="openai")
        enhanced = EnhancedMessage(message=msg, metadata=meta)

        d = enhanced.to_dict()
        assert d["message"]["role"] == "user"
        assert d["message"]["content"] == "Test"
        assert d["metadata"]["provider"] == "openai"

    def test_enhanced_message_from_dict(self):
        """EnhancedMessage.from_dict deve deserializar corretamente."""
        data = {
            "message": {"role": "user", "content": "Hello"},
            "metadata": {"provider": "openai", "model": "gpt-4"},
        }
        enhanced = EnhancedMessage.from_dict(data)

        assert enhanced.role == "user"
        assert enhanced.content == "Hello"
        assert enhanced.provider == "openai"
        assert enhanced.model == "gpt-4"

    def test_enhanced_message_is_frozen(self):
        """EnhancedMessage deve ser imutavel."""
        msg = Message(role="user", content="Test")
        enhanced = EnhancedMessage(message=msg)

        with pytest.raises(AttributeError):
            enhanced.message = Message(role="user", content="Changed")  # type: ignore


class TestConversationBasic:
    """Testes basicos de Conversation."""

    def test_conversation_creation(self):
        """Conversation deve aceitar client e system prompt."""
        client = MagicMock()
        conv = Conversation(client=client, system="You are helpful")

        assert conv.system_prompt == "You are helpful"
        assert conv.is_empty()

    def test_conversation_add_messages(self):
        """Conversation deve adicionar mensagens."""
        client = MagicMock()
        conv = Conversation(client=client)

        conv.add_user_message("Hello")
        conv.add_assistant_message("Hi there")

        assert conv.message_count == 2
        assert not conv.is_empty()

    def test_conversation_messages_property(self):
        """Conversation.messages deve retornar lista de Message."""
        client = MagicMock()
        conv = Conversation(client=client)

        conv.add_user_message("Hello")
        messages = conv.messages

        assert len(messages) == 1
        assert messages[0].role == "user"
        assert messages[0].content == "Hello"

    def test_conversation_enhanced_messages_property(self):
        """Conversation.enhanced_messages deve retornar EnhancedMessage."""
        client = MagicMock()
        conv = Conversation(client=client)

        conv.add_user_message("Hello", provider="openai", model="gpt-4")
        enhanced = conv.enhanced_messages

        assert len(enhanced) == 1
        assert isinstance(enhanced[0], EnhancedMessage)
        assert enhanced[0].provider == "openai"

    def test_conversation_clear(self):
        """Conversation.clear deve limpar mensagens."""
        client = MagicMock()
        conv = Conversation(client=client, system="System")

        conv.add_user_message("Hello")
        conv.clear()

        assert conv.is_empty()
        assert conv.system_prompt == "System"


class TestConversationMaxMessages:
    """Testes para limite de mensagens."""

    def test_max_messages_trim(self):
        """Conversation deve respeitar max_messages."""
        client = MagicMock()
        conv = Conversation(client=client, max_messages=2)

        conv.add_user_message("Msg 1")
        conv.add_assistant_message("Reply 1")
        conv.add_user_message("Msg 2")

        assert conv.message_count == 2
        assert conv.messages[0].content == "Reply 1"
        assert conv.messages[1].content == "Msg 2"

    def test_max_messages_none(self):
        """Conversation sem max_messages nao deve limitar."""
        client = MagicMock()
        conv = Conversation(client=client)

        for i in range(100):
            conv.add_user_message(f"Msg {i}")

        assert conv.message_count == 100


class TestConversationMaxTokens:
    """Testes para limite de tokens."""

    def test_max_tokens_property(self):
        """Conversation deve ter max_tokens property."""
        client = MagicMock()
        conv = Conversation(client=client, max_tokens=4000, model="gpt-4")

        assert conv.max_tokens == 4000

    def test_token_count_zero_when_no_counter(self):
        """token_count deve ser 0 quando sem max_tokens."""
        client = MagicMock()
        conv = Conversation(client=client)

        conv.add_user_message("Hello world")
        assert conv.token_count == 0

    def test_token_count_with_counter(self):
        """token_count deve funcionar com max_tokens definido."""
        client = MagicMock()
        conv = Conversation(client=client, max_tokens=4000, model="gpt-4o-mini")

        conv.add_user_message("Hello world")
        assert conv.token_count > 0

    def test_max_tokens_trim(self):
        """Conversation deve truncar por tokens."""
        client = MagicMock()
        # Limite muito baixo para forcar truncamento
        conv = Conversation(client=client, max_tokens=50, model="gpt-4o-mini")

        # Adicionar mensagens ate exceder
        for i in range(10):
            conv.add_user_message(f"This is message number {i} with some content")

        # Deve ter truncado
        assert conv.message_count < 10


class TestConversationProviderTracking:
    """Testes para tracking de provider."""

    def test_last_provider_none_initially(self):
        """last_provider deve ser None inicialmente."""
        client = MagicMock()
        conv = Conversation(client=client)

        assert conv.last_provider is None

    def test_last_provider_updated(self):
        """last_provider deve ser atualizado apos mensagem."""
        client = MagicMock()
        conv = Conversation(client=client)

        conv.add_assistant_message("Hello", provider="openai", model="gpt-4")
        assert conv.last_provider == "openai"

    def test_provider_history(self):
        """provider_history deve rastrear providers usados."""
        client = MagicMock()
        conv = Conversation(client=client)

        conv.add_assistant_message("Hi", provider="openai")
        conv.add_assistant_message("Hello", provider="anthropic")
        conv.add_assistant_message("Hey", provider="openai")  # Repetido

        history = conv.provider_history
        assert "openai" in history
        assert "anthropic" in history
        assert len(history) == 2  # Sem duplicatas


class TestConversationHotSwap:
    """Testes para hot-swap de provider."""

    def test_change_provider_calls_client_configure(self):
        """change_provider deve chamar client.configure."""
        client = MagicMock()
        conv = Conversation(client=client)

        conv.change_provider("anthropic", api_key="sk-ant-123")

        client.configure.assert_called_once_with(
            "anthropic", api_key="sk-ant-123"
        )

    def test_change_provider_preserves_history(self):
        """change_provider deve preservar historico."""
        client = MagicMock()
        conv = Conversation(client=client)

        conv.add_user_message("Hello")
        conv.add_assistant_message("Hi", provider="openai")
        conv.change_provider("anthropic")

        assert conv.message_count == 2
        assert conv.messages[0].content == "Hello"


class TestConversationSerialization:
    """Testes para serializacao."""

    def test_to_dict(self):
        """to_dict deve serializar estado completo."""
        client = MagicMock()
        conv = Conversation(
            client=client,
            system="You are helpful",
            max_messages=10,
            max_tokens=4000,
            model="gpt-4",
        )

        conv.add_user_message("Hello", provider="openai")
        conv.add_assistant_message("Hi", provider="openai", model="gpt-4")

        d = conv.to_dict()

        assert d["system_prompt"] == "You are helpful"
        assert d["max_messages"] == 10
        assert d["max_tokens"] == 4000
        assert d["model"] == "gpt-4"
        assert len(d["messages"]) == 2
        assert d["last_provider"] == "openai"

    def test_from_dict(self):
        """from_dict deve restaurar estado completo."""
        client = MagicMock()
        data = {
            "system_prompt": "You are helpful",
            "max_messages": 10,
            "max_tokens": 4000,
            "model": "gpt-4",
            "messages": [
                {
                    "message": {"role": "user", "content": "Hello"},
                    "metadata": {"provider": "openai"},
                },
                {
                    "message": {"role": "assistant", "content": "Hi"},
                    "metadata": {"provider": "openai", "model": "gpt-4"},
                },
            ],
            "provider_history": ["openai"],
            "last_provider": "openai",
            "last_model": "gpt-4",
        }

        conv = Conversation.from_dict(data, client)

        assert conv.system_prompt == "You are helpful"
        assert conv.max_messages == 10
        assert conv.max_tokens == 4000
        assert conv.message_count == 2
        assert conv.last_provider == "openai"
        assert conv.last_model == "gpt-4"

    def test_roundtrip_serialization(self):
        """Serializar e deserializar deve preservar estado."""
        client = MagicMock()
        original = Conversation(client=client, system="Test", max_messages=5)

        original.add_user_message("Hello", provider="openai")
        original.add_assistant_message("Hi", provider="openai", model="gpt-4")

        # Roundtrip
        data = original.to_dict()
        restored = Conversation.from_dict(data, client)

        assert restored.system_prompt == original.system_prompt
        assert restored.message_count == original.message_count
        assert restored.last_provider == original.last_provider


class TestConversationChat:
    """Testes para metodo chat."""

    @pytest.mark.asyncio
    async def test_chat_adds_messages(self):
        """chat deve adicionar mensagens ao historico."""
        client = MagicMock()
        client.provider_name = "openai"
        client.model = "gpt-4"
        client.chat = AsyncMock(
            return_value=ChatResponse(
                content="Hello!",
                model="gpt-4",
                provider="openai",
                usage=TokenUsage(prompt_tokens=10, completion_tokens=5),
            )
        )

        conv = Conversation(client=client)
        response = await conv.chat("Hi")

        assert conv.message_count == 2
        assert conv.messages[0].role == "user"
        assert conv.messages[1].role == "assistant"
        assert response.content == "Hello!"

    @pytest.mark.asyncio
    async def test_chat_includes_history(self):
        """chat deve incluir historico nas mensagens."""
        client = MagicMock()
        client.provider_name = "openai"
        client.model = "gpt-4"
        client.chat = AsyncMock(
            return_value=ChatResponse(
                content="Response",
                model="gpt-4",
                provider="openai",
                usage=TokenUsage(prompt_tokens=10, completion_tokens=5),
            )
        )

        conv = Conversation(client=client, system="You are helpful")
        conv.add_user_message("First")
        conv.add_assistant_message("Reply")

        await conv.chat("Second")

        # Verificar que chamou chat com todas as mensagens
        call_args = client.chat.call_args
        messages = call_args[0][0]  # Primeiro argumento posicional

        # System + First + Reply + Second = 4 mensagens
        assert len(messages) == 4
        assert messages[0].role == "system"

    @pytest.mark.asyncio
    async def test_chat_tracks_provider_metadata(self):
        """chat deve rastrear metadados do provider."""
        client = MagicMock()
        client.provider_name = "anthropic"
        client.model = "claude-3"
        client.chat = AsyncMock(
            return_value=ChatResponse(
                content="Hi",
                model="claude-3",
                provider="anthropic",
                usage=TokenUsage(prompt_tokens=5, completion_tokens=2),
            )
        )

        conv = Conversation(client=client)
        await conv.chat("Hello")

        assert conv.last_provider == "anthropic"
        assert conv.last_model == "claude-3"
        assert "anthropic" in conv.provider_history


class TestConversationGetMessagesForAPI:
    """Testes para get_messages_for_api."""

    def test_includes_system_prompt(self):
        """get_messages_for_api deve incluir system prompt."""
        client = MagicMock()
        conv = Conversation(client=client, system="You are helpful")

        conv.add_user_message("Hello")
        messages = conv.get_messages_for_api()

        assert len(messages) == 2
        assert messages[0].role == "system"
        assert messages[0].content == "You are helpful"

    def test_without_system_prompt(self):
        """get_messages_for_api sem system prompt."""
        client = MagicMock()
        conv = Conversation(client=client)

        conv.add_user_message("Hello")
        messages = conv.get_messages_for_api()

        assert len(messages) == 1
        assert messages[0].role == "user"


class TestEdgeCases:
    """Testes para edge cases criticos (A4 bill-review)."""

    @pytest.mark.asyncio
    async def test_chat_with_unconfigured_client(self):
        """chat deve falhar com ConfigurationError se client nao configurado."""
        from forge_llm.domain.exceptions import ConfigurationError

        client = MagicMock()
        client.is_configured = False

        conv = Conversation(client=client)
        conv.add_user_message("Hello")

        with pytest.raises(ConfigurationError, match="não está configurado"):
            await conv.chat("Test")

    def test_from_dict_with_invalid_client(self):
        """from_dict deve falhar com ValidationError se client invalido."""
        from forge_llm.domain.exceptions import ValidationError

        # Client sem interface necessaria
        invalid_client = object()

        data = {
            "system_prompt": "Test",
            "messages": [],
        }

        with pytest.raises(ValidationError, match="interface Client"):
            Conversation.from_dict(data, invalid_client)

    def test_enhanced_message_from_dict_missing_message(self):
        """EnhancedMessage.from_dict deve falhar se message ausente."""
        from forge_llm.domain.exceptions import ValidationError

        with pytest.raises(ValidationError, match="message.*obrigatório"):
            EnhancedMessage.from_dict({})

    def test_enhanced_message_from_dict_missing_role(self):
        """EnhancedMessage.from_dict deve falhar se role ausente."""
        from forge_llm.domain.exceptions import ValidationError

        data = {"message": {"content": "Hello"}}

        with pytest.raises(ValidationError, match="role.*content.*obrigatórios"):
            EnhancedMessage.from_dict(data)

    def test_enhanced_message_from_dict_missing_content(self):
        """EnhancedMessage.from_dict deve falhar se content ausente."""
        from forge_llm.domain.exceptions import ValidationError

        data = {"message": {"role": "user"}}

        with pytest.raises(ValidationError, match="role.*content.*obrigatórios"):
            EnhancedMessage.from_dict(data)

    def test_metadata_from_dict_invalid_timestamp(self):
        """MessageMetadata.from_dict deve falhar com timestamp invalido."""
        from forge_llm.domain.exceptions import ValidationError

        data = {"timestamp": "not-a-valid-timestamp"}

        with pytest.raises(ValidationError, match="Timestamp inválido"):
            MessageMetadata.from_dict(data)

    def test_trim_messages_protection_against_infinite_loop(self):
        """_trim_messages deve ter protecao contra loop infinito."""
        client = MagicMock()
        # max_tokens muito baixo
        conv = Conversation(client=client, max_tokens=10, model="gpt-4o-mini")

        # Adicionar mensagem grande
        conv.add_user_message("This is a very long message " * 100)

        # Nao deve travar em loop infinito
        # Se chegou aqui, passou
        assert conv.message_count >= 1
