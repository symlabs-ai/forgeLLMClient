"""Testes para Entidades - TDD RED phase."""

from datetime import datetime

import pytest


class TestChatResponse:
    """Testes para entidade ChatResponse."""

    def test_chat_response_creation(self):
        """ChatResponse deve aceitar campos obrigatorios."""
        from forge_llm.domain.entities import ChatResponse
        from forge_llm.domain.value_objects import TokenUsage

        usage = TokenUsage(prompt_tokens=10, completion_tokens=20)
        response = ChatResponse(
            content="Ola!",
            model="gpt-4",
            provider="openai",
            usage=usage,
        )
        assert response.content == "Ola!"
        assert response.model == "gpt-4"
        assert response.provider == "openai"

    def test_chat_response_has_usage(self):
        """ChatResponse deve ter TokenUsage."""
        from forge_llm.domain.entities import ChatResponse
        from forge_llm.domain.value_objects import TokenUsage

        usage = TokenUsage(prompt_tokens=10, completion_tokens=20)
        response = ChatResponse(
            content="Ola!",
            model="gpt-4",
            provider="openai",
            usage=usage,
        )
        assert response.usage.total_tokens == 30

    def test_chat_response_default_finish_reason(self):
        """ChatResponse deve ter finish_reason padrao 'stop'."""
        from forge_llm.domain.entities import ChatResponse
        from forge_llm.domain.value_objects import TokenUsage

        usage = TokenUsage(prompt_tokens=10, completion_tokens=20)
        response = ChatResponse(
            content="Ola!",
            model="gpt-4",
            provider="openai",
            usage=usage,
        )
        assert response.finish_reason == "stop"

    def test_chat_response_custom_finish_reason(self):
        """ChatResponse deve aceitar finish_reason customizado."""
        from forge_llm.domain.entities import ChatResponse
        from forge_llm.domain.value_objects import TokenUsage

        usage = TokenUsage(prompt_tokens=10, completion_tokens=20)
        response = ChatResponse(
            content="",
            model="gpt-4",
            provider="openai",
            usage=usage,
            finish_reason="tool_calls",
        )
        assert response.finish_reason == "tool_calls"

    def test_chat_response_empty_tool_calls_by_default(self):
        """ChatResponse deve ter lista vazia de tool_calls por padrao."""
        from forge_llm.domain.entities import ChatResponse
        from forge_llm.domain.value_objects import TokenUsage

        usage = TokenUsage(prompt_tokens=10, completion_tokens=20)
        response = ChatResponse(
            content="Ola!",
            model="gpt-4",
            provider="openai",
            usage=usage,
        )
        assert response.tool_calls == []

    def test_chat_response_has_tool_calls_property(self):
        """ChatResponse.has_tool_calls deve retornar True quando ha tool calls."""
        from forge_llm.domain.entities import ChatResponse, ToolCall
        from forge_llm.domain.value_objects import TokenUsage

        usage = TokenUsage(prompt_tokens=10, completion_tokens=20)
        tool_call = ToolCall(name="calculator", arguments={"a": 1, "b": 2})
        response = ChatResponse(
            content="",
            model="gpt-4",
            provider="openai",
            usage=usage,
            tool_calls=[tool_call],
        )
        assert response.has_tool_calls is True

    def test_chat_response_has_tool_calls_false_when_empty(self):
        """ChatResponse.has_tool_calls deve retornar False quando vazio."""
        from forge_llm.domain.entities import ChatResponse
        from forge_llm.domain.value_objects import TokenUsage

        usage = TokenUsage(prompt_tokens=10, completion_tokens=20)
        response = ChatResponse(
            content="Ola!",
            model="gpt-4",
            provider="openai",
            usage=usage,
        )
        assert response.has_tool_calls is False

    def test_chat_response_has_created_at(self):
        """ChatResponse deve ter created_at."""
        from forge_llm.domain.entities import ChatResponse
        from forge_llm.domain.value_objects import TokenUsage

        usage = TokenUsage(prompt_tokens=10, completion_tokens=20)
        response = ChatResponse(
            content="Ola!",
            model="gpt-4",
            provider="openai",
            usage=usage,
        )
        assert isinstance(response.created_at, datetime)

    def test_chat_response_empty_model_raises(self):
        """ChatResponse com model vazio deve levantar erro."""
        from forge_llm.domain.entities import ChatResponse
        from forge_llm.domain.exceptions import ValidationError
        from forge_llm.domain.value_objects import TokenUsage

        usage = TokenUsage(prompt_tokens=10, completion_tokens=20)
        with pytest.raises(ValidationError):
            ChatResponse(
                content="Ola!",
                model="",
                provider="openai",
                usage=usage,
            )

    def test_chat_response_empty_provider_raises(self):
        """ChatResponse com provider vazio deve levantar erro."""
        from forge_llm.domain.entities import ChatResponse
        from forge_llm.domain.exceptions import ValidationError
        from forge_llm.domain.value_objects import TokenUsage

        usage = TokenUsage(prompt_tokens=10, completion_tokens=20)
        with pytest.raises(ValidationError):
            ChatResponse(
                content="Ola!",
                model="gpt-4",
                provider="",
                usage=usage,
            )

    def test_chat_response_has_id(self):
        """ChatResponse deve ter id opcional."""
        from forge_llm.domain.entities import ChatResponse
        from forge_llm.domain.value_objects import TokenUsage

        usage = TokenUsage(prompt_tokens=10, completion_tokens=20)
        response = ChatResponse(
            id="resp_123",
            content="Ola!",
            model="gpt-4",
            provider="openai",
            usage=usage,
        )
        assert response.id == "resp_123"


class TestToolCall:
    """Testes para entidade ToolCall."""

    def test_tool_call_creation(self):
        """ToolCall deve aceitar name e arguments."""
        from forge_llm.domain.entities import ToolCall

        tc = ToolCall(name="calculator", arguments={"a": 1, "b": 2})
        assert tc.name == "calculator"
        assert tc.arguments == {"a": 1, "b": 2}

    def test_tool_call_with_id(self):
        """ToolCall deve aceitar id opcional."""
        from forge_llm.domain.entities import ToolCall

        tc = ToolCall(id="call_123", name="calculator", arguments={})
        assert tc.id == "call_123"

    def test_tool_call_empty_name_raises(self):
        """ToolCall com name vazio deve levantar erro."""
        from forge_llm.domain.entities import ToolCall
        from forge_llm.domain.exceptions import ValidationError

        with pytest.raises(ValidationError):
            ToolCall(name="", arguments={})

    def test_tool_call_arguments_must_be_dict(self):
        """ToolCall arguments deve ser dict."""
        from forge_llm.domain.entities import ToolCall
        from forge_llm.domain.exceptions import ValidationError

        with pytest.raises(ValidationError):
            ToolCall(name="calc", arguments="invalid")  # type: ignore

    def test_tool_call_to_dict(self):
        """ToolCall deve converter para dict."""
        from forge_llm.domain.entities import ToolCall

        tc = ToolCall(id="call_123", name="calculator", arguments={"x": 10})
        d = tc.to_dict()
        assert d == {
            "id": "call_123",
            "name": "calculator",
            "arguments": {"x": 10},
        }
