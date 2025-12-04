"""Tests for ConversationMemory."""

import pytest

from forge_llm.domain.value_objects import Message
from forge_llm.utils.conversation_memory import ConversationMemory


class TestConversationMemoryBasics:
    """Testes basicos para ConversationMemory."""

    def test_memory_creation_defaults(self):
        """ConversationMemory deve usar valores padrao."""
        memory = ConversationMemory()
        assert memory.max_tokens == 4000
        assert memory.system_message is None
        assert len(memory) == 0

    def test_memory_creation_custom(self):
        """ConversationMemory deve aceitar parametros customizados."""
        memory = ConversationMemory(
            max_tokens=2000,
            model="gpt-4",
            system_message="You are helpful",
        )
        assert memory.max_tokens == 2000
        assert memory.system_message == "You are helpful"


class TestConversationMemoryAdd:
    """Testes de adicao de mensagens."""

    def test_add_message(self):
        """Deve adicionar mensagem ao historico."""
        memory = ConversationMemory()
        memory.add(Message(role="user", content="Hello"))
        assert len(memory) == 1

    def test_add_user_shortcut(self):
        """add_user deve criar Message de usuario."""
        memory = ConversationMemory()
        memory.add_user("Hello")
        messages = memory.get_messages()
        assert len(messages) == 1
        assert messages[0].role == "user"
        assert messages[0].content == "Hello"

    def test_add_assistant_shortcut(self):
        """add_assistant deve criar Message de assistente."""
        memory = ConversationMemory()
        memory.add_assistant("Hi there!")
        messages = memory.get_messages()
        assert len(messages) == 1
        assert messages[0].role == "assistant"


class TestConversationMemoryGetMessages:
    """Testes de obtencao de mensagens."""

    def test_get_messages_empty(self):
        """Lista vazia quando sem mensagens."""
        memory = ConversationMemory()
        messages = memory.get_messages()
        assert messages == []

    def test_get_messages_with_system(self):
        """Deve incluir system message no inicio."""
        memory = ConversationMemory(system_message="Be helpful")
        memory.add_user("Hi")
        messages = memory.get_messages()
        assert len(messages) == 2
        assert messages[0].role == "system"
        assert messages[0].content == "Be helpful"
        assert messages[1].role == "user"

    def test_get_messages_order(self):
        """Mensagens devem manter ordem de adicao."""
        memory = ConversationMemory()
        memory.add_user("First")
        memory.add_assistant("Second")
        memory.add_user("Third")
        messages = memory.get_messages()
        assert messages[0].content == "First"
        assert messages[1].content == "Second"
        assert messages[2].content == "Third"


class TestConversationMemoryTruncation:
    """Testes de truncamento automatico."""

    def test_truncation_removes_old_messages(self):
        """Deve remover mensagens antigas quando excede limite."""
        # Limite muito baixo para forcar truncamento
        memory = ConversationMemory(max_tokens=50)

        # Adicionar varias mensagens
        for i in range(10):
            memory.add_user(f"Message {i} with some content")

        # Deve ter menos que 10 mensagens devido truncamento
        assert len(memory) < 10
        assert len(memory) >= 1

    def test_truncation_keeps_recent(self):
        """Truncamento deve manter mensagens mais recentes."""
        memory = ConversationMemory(max_tokens=100)

        memory.add_user("Old message")
        memory.add_user("New message with more content to trigger truncation")
        memory.add_user("Latest message")

        messages = memory.get_messages()
        # Ultima mensagem deve estar presente
        assert any("Latest" in m.content for m in messages)


class TestConversationMemoryClear:
    """Testes de limpeza."""

    def test_clear_removes_messages(self):
        """clear deve remover todas as mensagens."""
        memory = ConversationMemory()
        memory.add_user("Hello")
        memory.add_assistant("Hi")
        memory.clear()
        assert len(memory) == 0

    def test_clear_keeps_system(self):
        """clear deve manter system message."""
        memory = ConversationMemory(system_message="Be helpful")
        memory.add_user("Hello")
        memory.clear()
        assert len(memory) == 0  # User messages cleared
        messages = memory.get_messages()
        assert len(messages) == 1  # System message still included
        assert messages[0].role == "system"
        assert memory.system_message == "Be helpful"


class TestConversationMemorySystem:
    """Testes de system message."""

    def test_set_system_message(self):
        """Deve permitir alterar system message."""
        memory = ConversationMemory()
        memory.set_system_message("New system")
        assert memory.system_message == "New system"

    def test_remove_system_message(self):
        """Deve permitir remover system message."""
        memory = ConversationMemory(system_message="Original")
        memory.set_system_message(None)
        assert memory.system_message is None


class TestConversationMemoryProperties:
    """Testes de propriedades."""

    def test_token_count(self):
        """token_count deve retornar total de tokens."""
        memory = ConversationMemory()
        memory.add_user("Hello world")
        assert memory.token_count > 0

    def test_message_count(self):
        """message_count deve retornar numero de mensagens."""
        memory = ConversationMemory()
        memory.add_user("1")
        memory.add_assistant("2")
        assert memory.message_count == 2
