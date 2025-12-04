"""Testes para Value Objects - TDD RED phase."""

import pytest


class TestMessage:
    """Testes para Value Object Message."""

    def test_message_creation_with_user_role(self):
        """Message deve aceitar role 'user'."""
        from forge_llm.domain.value_objects import Message

        msg = Message(role="user", content="Ola")
        assert msg.role == "user"
        assert msg.content == "Ola"

    def test_message_creation_with_assistant_role(self):
        """Message deve aceitar role 'assistant'."""
        from forge_llm.domain.value_objects import Message

        msg = Message(role="assistant", content="Ola, como posso ajudar?")
        assert msg.role == "assistant"

    def test_message_creation_with_system_role(self):
        """Message deve aceitar role 'system'."""
        from forge_llm.domain.value_objects import Message

        msg = Message(role="system", content="Voce e um assistente.")
        assert msg.role == "system"

    def test_message_creation_with_tool_role(self):
        """Message deve aceitar role 'tool' com tool_call_id."""
        from forge_llm.domain.value_objects import Message

        msg = Message(role="tool", content="42", tool_call_id="call_123")
        assert msg.role == "tool"
        assert msg.tool_call_id == "call_123"

    def test_message_invalid_role_raises_error(self):
        """Message com role invalido deve levantar ValidationError."""
        from forge_llm.domain.exceptions import ValidationError
        from forge_llm.domain.value_objects import Message

        with pytest.raises(ValidationError):
            Message(role="invalid", content="test")

    def test_message_tool_role_requires_tool_call_id(self):
        """Message com role 'tool' sem tool_call_id deve levantar erro."""
        from forge_llm.domain.exceptions import ValidationError
        from forge_llm.domain.value_objects import Message

        with pytest.raises(ValidationError):
            Message(role="tool", content="result")

    def test_message_to_dict(self):
        """Message deve converter para dict."""
        from forge_llm.domain.value_objects import Message

        msg = Message(role="user", content="Ola")
        d = msg.to_dict()
        assert d == {"role": "user", "content": "Ola"}

    def test_message_to_dict_with_name(self):
        """Message com name deve incluir no dict."""
        from forge_llm.domain.value_objects import Message

        msg = Message(role="user", content="Ola", name="joao")
        d = msg.to_dict()
        assert d["name"] == "joao"

    def test_message_equality(self):
        """Duas Messages com mesmos valores devem ser iguais."""
        from forge_llm.domain.value_objects import Message

        msg1 = Message(role="user", content="Ola")
        msg2 = Message(role="user", content="Ola")
        assert msg1 == msg2

    def test_message_immutability(self):
        """Message deve ser imutavel."""
        from forge_llm.domain.value_objects import Message

        msg = Message(role="user", content="Ola")
        with pytest.raises(AttributeError):
            msg.content = "Outro"


class TestTokenUsage:
    """Testes para Value Object TokenUsage."""

    def test_token_usage_creation(self):
        """TokenUsage deve aceitar prompt e completion tokens."""
        from forge_llm.domain.value_objects import TokenUsage

        usage = TokenUsage(prompt_tokens=10, completion_tokens=20)
        assert usage.prompt_tokens == 10
        assert usage.completion_tokens == 20

    def test_token_usage_total_calculated(self):
        """TokenUsage deve calcular total automaticamente."""
        from forge_llm.domain.value_objects import TokenUsage

        usage = TokenUsage(prompt_tokens=10, completion_tokens=20)
        assert usage.total_tokens == 30

    def test_token_usage_total_explicit(self):
        """TokenUsage deve aceitar total explicito."""
        from forge_llm.domain.value_objects import TokenUsage

        usage = TokenUsage(prompt_tokens=10, completion_tokens=20, total_tokens=35)
        assert usage.total_tokens == 35

    def test_token_usage_negative_prompt_tokens_raises(self):
        """TokenUsage com prompt_tokens negativo deve levantar erro."""
        from forge_llm.domain.exceptions import ValidationError
        from forge_llm.domain.value_objects import TokenUsage

        with pytest.raises(ValidationError):
            TokenUsage(prompt_tokens=-1, completion_tokens=20)

    def test_token_usage_negative_completion_tokens_raises(self):
        """TokenUsage com completion_tokens negativo deve levantar erro."""
        from forge_llm.domain.exceptions import ValidationError
        from forge_llm.domain.value_objects import TokenUsage

        with pytest.raises(ValidationError):
            TokenUsage(prompt_tokens=10, completion_tokens=-1)

    def test_token_usage_to_dict(self):
        """TokenUsage deve converter para dict."""
        from forge_llm.domain.value_objects import TokenUsage

        usage = TokenUsage(prompt_tokens=10, completion_tokens=20)
        d = usage.to_dict()
        assert d == {
            "prompt_tokens": 10,
            "completion_tokens": 20,
            "total_tokens": 30,
        }

    def test_token_usage_equality(self):
        """Dois TokenUsage com mesmos valores devem ser iguais."""
        from forge_llm.domain.value_objects import TokenUsage

        u1 = TokenUsage(prompt_tokens=10, completion_tokens=20)
        u2 = TokenUsage(prompt_tokens=10, completion_tokens=20)
        assert u1 == u2


class TestToolDefinition:
    """Testes para Value Object ToolDefinition."""

    def test_tool_definition_creation(self):
        """ToolDefinition deve aceitar name, description e parameters."""
        from forge_llm.domain.value_objects import ToolDefinition

        tool = ToolDefinition(
            name="calculator",
            description="Faz calculos matematicos",
            parameters={"type": "object", "properties": {}},
        )
        assert tool.name == "calculator"
        assert tool.description == "Faz calculos matematicos"

    def test_tool_definition_empty_name_raises(self):
        """ToolDefinition com name vazio deve levantar erro."""
        from forge_llm.domain.exceptions import ValidationError
        from forge_llm.domain.value_objects import ToolDefinition

        with pytest.raises(ValidationError):
            ToolDefinition(name="", description="desc", parameters={})

    def test_tool_definition_empty_description_raises(self):
        """ToolDefinition com description vazia deve levantar erro."""
        from forge_llm.domain.exceptions import ValidationError
        from forge_llm.domain.value_objects import ToolDefinition

        with pytest.raises(ValidationError):
            ToolDefinition(name="calc", description="", parameters={})

    def test_tool_definition_to_dict(self):
        """ToolDefinition deve converter para dict."""
        from forge_llm.domain.value_objects import ToolDefinition

        tool = ToolDefinition(
            name="calculator",
            description="Faz calculos",
            parameters={"type": "object"},
        )
        d = tool.to_dict()
        assert d == {
            "name": "calculator",
            "description": "Faz calculos",
            "parameters": {"type": "object"},
        }
