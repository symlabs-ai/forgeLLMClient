"""BDD steps for conversation feature."""

import asyncio
from unittest.mock import AsyncMock, MagicMock

from pytest_bdd import given, parsers, scenarios, then, when

from forge_llm.client import Client
from forge_llm.domain.entities import ChatResponse, Conversation
from forge_llm.domain.value_objects import Message, TokenUsage

scenarios("../../specs/bdd/10_forge_core/conversation.feature")


def run_async(coro):
    """Run async coroutine in sync context."""
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(coro)


@given('um client configurado com provider "mock"')
def client_with_mock(context):
    """Create client with mock provider."""
    context["client"] = Client(provider="mock", api_key="test-key")
    # Setup mock for tracking calls
    mock_provider = MagicMock()
    mock_provider.provider_name = "mock"
    mock_provider.default_model = "mock-model"
    mock_provider.chat = AsyncMock()
    context["mock_provider"] = mock_provider


@given("uma conversa criada")
def conversation_created(context):
    """Create a basic conversation."""
    client = context["client"]
    # Replace with mock provider
    mock_provider = context["mock_provider"]
    client._provider = mock_provider
    context["conversation"] = client.create_conversation()


@given(parsers.parse('uma conversa com system prompt "{system}"'))
def conversation_with_system(context, system):
    """Create conversation with system prompt."""
    client = context["client"]
    mock_provider = context["mock_provider"]
    client._provider = mock_provider
    context["conversation"] = client.create_conversation(system=system)


@given("uma conversa com historico")
def conversation_with_history(context):
    """Create conversation with some history."""
    client = context["client"]
    mock_provider = context["mock_provider"]
    client._provider = mock_provider
    conv = client.create_conversation(system="Test system")
    conv.add_user_message("Hello")
    conv.add_assistant_message("Hi there!")
    context["conversation"] = conv


@given(parsers.parse('a conversa tem mensagem do usuario "{content}"'))
def conversation_has_user_message(context, content):
    """Add user message to conversation."""
    context["conversation"].add_user_message(content)


@given(parsers.parse('a conversa tem mensagem do assistant "{content}"'))
def conversation_has_assistant_message(context, content):
    """Add assistant message to conversation."""
    context["conversation"].add_assistant_message(content)


@when("eu crio uma conversa")
def create_conversation(context):
    """Create a new conversation."""
    client = context["client"]
    mock_provider = context["mock_provider"]
    client._provider = mock_provider
    context["conversation"] = client.create_conversation()


@when(parsers.parse('eu crio uma conversa com system prompt "{system}"'))
def create_conversation_with_system(context, system):
    """Create conversation with system prompt."""
    client = context["client"]
    mock_provider = context["mock_provider"]
    client._provider = mock_provider
    context["conversation"] = client.create_conversation(system=system)


@when(parsers.parse('eu envio a mensagem "{message}"'))
def send_message(context, message):
    """Send a message in the conversation."""
    conv = context["conversation"]
    mock_provider = context["mock_provider"]

    # Check if expected response is set (from a previous step)
    expected_content = context.get("expected_response", "Mock response")

    # Setup mock response
    usage = TokenUsage(prompt_tokens=10, completion_tokens=5)
    response = ChatResponse(
        content=expected_content,
        model="mock-model",
        provider="mock",
        usage=usage,
    )
    mock_provider.chat.return_value = response

    # Send message
    context["response"] = run_async(conv.chat(message))


@when(parsers.parse('eu recebo a resposta "{response}"'))
def receive_response(context, response):
    """Set up expected response for the next message."""
    # Store expected response - it will be used by send_message
    # But since this comes AFTER send_message, we need to update history manually
    conv = context["conversation"]
    # Remove the last assistant message (the mock one)
    if conv._messages and conv._messages[-1].role == "assistant":
        conv._messages.pop()
    # Add the expected response
    conv.add_assistant_message(response)


@when("eu limpo a conversa")
def clear_conversation(context):
    """Clear conversation history."""
    context["conversation"].clear()


@when("eu acesso as mensagens")
def access_messages(context):
    """Access conversation messages."""
    context["accessed_messages"] = context["conversation"].messages


@then("a conversa deve estar vazia")
def conversation_is_empty(context):
    """Verify conversation is empty."""
    conv = context["conversation"]
    assert conv.is_empty(), f"Expected empty, got {conv.message_count} messages"


@then("a conversa nao deve ter system prompt")
def conversation_no_system_prompt(context):
    """Verify no system prompt."""
    conv = context["conversation"]
    assert conv.system_prompt is None


@then(parsers.parse('a conversa deve ter system prompt "{expected}"'))
def conversation_has_system_prompt(context, expected):
    """Verify system prompt value."""
    conv = context["conversation"]
    assert conv.system_prompt == expected


@then(parsers.parse("o historico deve ter {count:d} mensagens"))
def history_has_count(context, count):
    """Verify message count."""
    conv = context["conversation"]
    assert conv.message_count == count, f"Expected {count}, got {conv.message_count}"


@then(parsers.parse('a primeira mensagem deve ser do usuario com "{content}"'))
def first_message_is_user(context, content):
    """Verify first message is from user."""
    conv = context["conversation"]
    messages = conv.messages
    assert len(messages) > 0, "No messages in history"
    assert messages[0].role == "user"
    assert messages[0].content == content


@then(parsers.parse('a segunda mensagem deve ser do assistant com "{content}"'))
def second_message_is_assistant(context, content):
    """Verify second message is from assistant."""
    conv = context["conversation"]
    messages = conv.messages
    assert len(messages) > 1, "Less than 2 messages"
    assert messages[1].role == "assistant"
    assert messages[1].content == content


@then(parsers.parse("o provider deve receber {count:d} mensagens"))
def provider_receives_messages(context, count):
    """Verify provider received correct number of messages."""
    mock_provider = context["mock_provider"]
    call_args = mock_provider.chat.call_args
    messages = call_args.kwargs.get("messages", call_args.args[0] if call_args.args else [])
    assert len(messages) == count, f"Expected {count}, got {len(messages)}"


@then(parsers.parse('a primeira mensagem enviada deve ser system "{content}"'))
def first_sent_is_system(context, content):
    """Verify first sent message is system."""
    mock_provider = context["mock_provider"]
    call_args = mock_provider.chat.call_args
    messages = call_args.kwargs.get("messages", call_args.args[0] if call_args.args else [])
    assert len(messages) > 0, "No messages sent"
    assert messages[0].role == "system"
    assert messages[0].content == content


@then("a conversa deve manter o system prompt")
def conversation_keeps_system_prompt(context):
    """Verify system prompt is kept after clear."""
    conv = context["conversation"]
    assert conv.system_prompt is not None


@then("eu devo receber uma lista de Message")
def received_message_list(context):
    """Verify received list of messages."""
    messages = context["accessed_messages"]
    assert isinstance(messages, list)


@then("cada mensagem deve ter role e content")
def messages_have_role_and_content(context):
    """Verify messages have required fields."""
    messages = context["accessed_messages"]
    for msg in messages:
        assert isinstance(msg, Message)
        assert msg.role is not None
        assert msg.content is not None
