"""Tests for TokenCounter."""

import pytest

from forge_llm.domain.value_objects import Message
from forge_llm.utils.token_counter import TokenCounter


class TestTokenCounterBasics:
    """Testes basicos para TokenCounter."""

    def test_token_counter_creation(self):
        """TokenCounter deve ser criado com modelo padrao."""
        counter = TokenCounter()
        assert counter.model == "gpt-4o-mini"

    def test_token_counter_custom_model(self):
        """TokenCounter deve aceitar modelo customizado."""
        counter = TokenCounter(model="gpt-4")
        assert counter.model == "gpt-4"

    def test_token_counter_fallback_encoding(self):
        """TokenCounter deve usar fallback para modelos desconhecidos."""
        counter = TokenCounter(model="unknown-model")
        assert counter is not None


class TestTokenCounterText:
    """Testes de contagem de texto."""

    def test_count_empty_text(self):
        """Texto vazio deve retornar 0."""
        counter = TokenCounter()
        assert counter.count_text("") == 0

    def test_count_simple_text(self):
        """Deve contar tokens em texto simples."""
        counter = TokenCounter()
        count = counter.count_text("Hello world")
        assert count > 0
        assert count < 10  # "Hello world" deve ter poucos tokens

    def test_count_longer_text(self):
        """Textos mais longos devem ter mais tokens."""
        counter = TokenCounter()
        short = counter.count_text("Hi")
        long = counter.count_text("Hello, this is a much longer sentence with more words.")
        assert long > short


class TestTokenCounterMessages:
    """Testes de contagem de mensagens."""

    def test_count_single_message(self):
        """Deve contar tokens de uma mensagem."""
        counter = TokenCounter()
        messages = [Message(role="user", content="Hello")]
        count = counter.count_messages(messages)
        # Deve incluir overhead da mensagem
        assert count >= TokenCounter.MESSAGE_OVERHEAD

    def test_count_multiple_messages(self):
        """Deve contar tokens de multiplas mensagens."""
        counter = TokenCounter()
        messages = [
            Message(role="user", content="Hello"),
            Message(role="assistant", content="Hi there!"),
            Message(role="user", content="How are you?"),
        ]
        count = counter.count_messages(messages)
        # 3 mensagens = 3 * overhead + conteudo
        assert count >= TokenCounter.MESSAGE_OVERHEAD * 3

    def test_count_empty_messages(self):
        """Lista vazia deve retornar 0."""
        counter = TokenCounter()
        count = counter.count_messages([])
        assert count == 0


class TestTokenCounterEstimate:
    """Testes de estimativa de tokens restantes."""

    def test_estimate_remaining_basic(self):
        """Deve calcular tokens restantes."""
        counter = TokenCounter()
        messages = [Message(role="user", content="Hello")]
        remaining = counter.estimate_remaining(messages, max_tokens=1000)
        assert remaining > 0
        assert remaining < 1000

    def test_estimate_remaining_near_limit(self):
        """Deve retornar 0 quando proximo do limite."""
        counter = TokenCounter()
        messages = [Message(role="user", content="Hello")]
        used = counter.count_messages(messages)
        remaining = counter.estimate_remaining(messages, max_tokens=used)
        assert remaining == 0

    def test_estimate_remaining_over_limit(self):
        """Deve retornar 0 quando excede limite."""
        counter = TokenCounter()
        messages = [Message(role="user", content="Hello")]
        remaining = counter.estimate_remaining(messages, max_tokens=1)
        assert remaining == 0


class TestTokenCounterModels:
    """Testes de diferentes modelos."""

    @pytest.mark.parametrize("model", [
        "gpt-4o",
        "gpt-4o-mini",
        "gpt-4-turbo",
        "gpt-4",
        "gpt-3.5-turbo",
    ])
    def test_supported_models(self, model):
        """Deve funcionar com modelos conhecidos."""
        counter = TokenCounter(model=model)
        count = counter.count_text("Test text")
        assert count > 0
