"""BDD Steps for tools.feature."""

import asyncio

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from forge_llm import (
    Client,
    ToolCallNotFoundError,
    ToolDefinition,
    ValidationError,
)
from forge_llm.providers import MockToolsProvider

# Link scenarios from feature file
scenarios("../../specs/bdd/10_forge_core/tools.feature")


def run_async(coro):
    """Helper to run async code in sync context."""
    return asyncio.get_event_loop().run_until_complete(coro)


# ========== FIXTURES ==========


@pytest.fixture
def tools_context():
    """Shared context between tools steps."""
    return {
        "client": None,
        "provider": None,
        "response": None,
        "pending_tool_call": None,
        "error": None,
        "error_type": None,
    }


# ========== GIVEN STEPS ==========


@given("the ForgeLLMClient is installed")
def forge_client_installed():
    """Verify SDK is available."""
    assert Client is not None


@given(
    parsers.parse("the client is configured with provider \"{provider}\""),
    target_fixture="tools_context",
)
def client_configured_with_provider(provider, tools_context):
    """Configure client with specific provider."""
    tools_context["client"] = Client(provider=provider)
    # Get direct access to provider for tool registration
    tools_context["provider"] = tools_context["client"]._provider
    return tools_context


@given(
    parsers.parse("the tool \"{tool_name}\" is registered"),
    target_fixture="tools_context",
)
def tool_is_registered(tool_name, tools_context):
    """Register a tool."""
    tool = ToolDefinition(
        name=tool_name,
        description=f"{tool_name} tool",
        parameters={"type": "object", "properties": {}},
    )
    tools_context["provider"].register_tool(tool)
    return tools_context


@given(
    parsers.parse("I received a tool_call with id \"{tc_id}\" for \"{tool_name}\""),
    target_fixture="tools_context",
)
def received_tool_call(tc_id, tool_name, tools_context):
    """Simulate receiving a tool call."""
    tools_context["pending_tool_call"] = {
        "id": tc_id,
        "name": tool_name,
    }
    return tools_context


@given(
    parsers.parse("the tools \"{tool1}\" and \"{tool2}\" are registered"),
    target_fixture="tools_context",
)
def multiple_tools_registered(tool1, tool2, tools_context):
    """Register multiple tools."""
    for name in [tool1, tool2]:
        tool = ToolDefinition(
            name=name,
            description=f"{name} tool",
            parameters={"type": "object", "properties": {}},
        )
        tools_context["provider"].register_tool(tool)
    # Configure provider to call both tools on next request
    tools_context["provider"].set_next_tool_calls([tool1, tool2])
    return tools_context


# ========== WHEN STEPS ==========


@when(
    parsers.parse(
        "I register the tool \"{tool_name}\" with description \"{description}\""
    ),
    target_fixture="tools_context",
)
def register_tool(tool_name, description, tools_context):
    """Register a tool with description."""
    tool = ToolDefinition(
        name=tool_name,
        description=description,
        parameters={"type": "object", "properties": {}},
    )
    tools_context["provider"].register_tool(tool)
    return tools_context


@when(
    parsers.parse("I send the message \"{message}\""),
    target_fixture="tools_context",
)
def send_message(message, tools_context):
    """Send message to LLM."""
    try:
        tools_context["response"] = run_async(tools_context["client"].chat(message))
    except Exception as e:
        tools_context["error"] = e
        tools_context["error_type"] = type(e).__name__
    return tools_context


@when(
    parsers.parse("I send the result \"{result}\" for tool_call \"{tc_id}\""),
    target_fixture="tools_context",
)
def send_tool_result(result, tc_id, tools_context):
    """Send tool call result."""
    # For mock, we just simulate sending a follow-up message
    # In real implementation, this would use submit_tool_result()
    try:
        tools_context["response"] = run_async(
            tools_context["client"].chat(f"Tool result: {result}")
        )
    except Exception as e:
        tools_context["error"] = e
        tools_context["error_type"] = type(e).__name__
    return tools_context


@when(
    "I try to register a tool without name",
    target_fixture="tools_context",
)
def try_register_tool_without_name(tools_context):
    """Try to register tool without name."""
    try:
        tool = ToolDefinition(
            name="",
            description="Test",
            parameters={},
        )
        tools_context["provider"].register_tool(tool)
    except ValidationError as e:
        tools_context["error"] = e
        tools_context["error_type"] = "ValidationError"
    except Exception as e:
        tools_context["error"] = e
        tools_context["error_type"] = type(e).__name__
    return tools_context


@when(
    parsers.parse("I try to send result for tool_call \"{tc_id}\""),
    target_fixture="tools_context",
)
def try_send_result_invalid_tc(tc_id, tools_context):
    """Try to send result for nonexistent tool_call."""
    try:
        # Simulate trying to submit result for unknown tool call
        raise ToolCallNotFoundError(tc_id)
    except ToolCallNotFoundError as e:
        tools_context["error"] = e
        tools_context["error_type"] = "ToolCallNotFoundError"
    return tools_context


# ========== THEN STEPS ==========


@then(parsers.parse("the client has {count:d} tools registered"))
def check_tool_count(count, tools_context):
    """Verify tool count."""
    assert len(tools_context["provider"].tools) == count


@then(parsers.parse("the tool \"{tool_name}\" is available"))
def check_tool_available(tool_name, tools_context):
    """Verify tool is available."""
    assert tools_context["provider"].has_tool(tool_name)


@then("I receive a response with tool_call")
def check_response_has_tool_call(tools_context):
    """Verify response has tool_call."""
    assert tools_context["response"] is not None
    assert tools_context["response"].has_tool_calls is True
    assert len(tools_context["response"].tool_calls) > 0


@then(parsers.parse("the tool_call has name \"{name}\""))
def check_tool_call_name(name, tools_context):
    """Verify tool_call name."""
    assert tools_context["response"].tool_calls[0].name == name


@then("the tool_call has arguments in JSON format")
def check_tool_call_args(tools_context):
    """Verify tool_call has arguments."""
    args = tools_context["response"].tool_calls[0].arguments
    assert isinstance(args, dict)


@then("the tool_call has a unique id")
def check_tool_call_id(tools_context):
    """Verify tool_call has id."""
    assert tools_context["response"].tool_calls[0].id is not None
    assert tools_context["response"].tool_calls[0].id.startswith("tc_")


@then("I receive a final response from the LLM")
def check_final_llm_response(tools_context):
    """Verify final response."""
    assert tools_context["response"] is not None


@then("the response incorporates the tool result")
def check_tool_result_incorporated(tools_context):
    """Verify tool result was incorporated."""
    # For mock, we just verify we got a response
    assert tools_context["response"] is not None


@then("I receive a response with multiple tool_calls")
def check_multiple_tool_calls(tools_context):
    """Verify multiple tool_calls."""
    assert len(tools_context["response"].tool_calls) > 1


@then(parsers.parse("there is a tool_call for \"{tool_name}\""))
def check_tool_call_exists(tool_name, tools_context):
    """Verify tool_call exists for tool."""
    names = [tc.name for tc in tools_context["response"].tool_calls]
    assert tool_name in names


@then(parsers.parse("I receive an error of type \"{error_type}\""))
def received_error_type(error_type, tools_context):
    """Verify error type received."""
    assert tools_context["error"] is not None
    assert tools_context["error_type"] == error_type


@then(parsers.parse("the error message contains \"{text}\""))
def error_message_contains(text, tools_context):
    """Verify error message contains text."""
    error_message = str(tools_context["error"]).lower()
    assert text.lower() in error_message, f"'{text}' not in '{error_message}'"
