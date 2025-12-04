"""BDD Steps for config.feature."""

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from forge_llm import Client, ConfigurationError, ProviderNotFoundError

# Link scenarios from feature file
scenarios("../../specs/bdd/10_forge_core/config.feature")


# ========== FIXTURES ==========


@pytest.fixture
def client_context():
    """Shared context between steps."""
    return {
        "client": None,
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
    target_fixture="client_context",
)
def client_configured_with_provider(provider, client_context):
    """Configure client with specific provider."""
    if provider == "mock":
        client_context["client"] = Client(provider=provider)
    else:
        client_context["client"] = Client(provider=provider, api_key="test-key")
    return client_context


# ========== WHEN STEPS ==========


@when(
    parsers.parse("I configure the client with provider \"{provider}\""),
    target_fixture="client_context",
)
def configure_client_with_provider(provider, client_context):
    """Configure client with provider."""
    client_context["client"] = Client(provider=provider)
    return client_context


@when(
    parsers.parse(
        "I configure the client with provider \"{provider}\" and api_key \"{api_key}\""
    ),
    target_fixture="client_context",
)
def configure_client_with_provider_and_key(provider, api_key, client_context):
    """Configure client with provider and API key."""
    client_context["client"] = Client(provider=provider, api_key=api_key)
    return client_context


@when(
    parsers.parse(
        "I configure the client with provider \"{provider}\" and model \"{model}\""
    ),
    target_fixture="client_context",
)
def configure_client_with_provider_and_model(provider, model, client_context):
    """Configure client with provider and model."""
    client_context["client"] = Client(
        provider=provider, api_key="test-key", model=model
    )
    return client_context


@when(
    parsers.parse("I reconfigure the client to provider \"{provider}\""),
    target_fixture="client_context",
)
def reconfigure_client_to_provider(provider, client_context):
    """Reconfigure client to new provider."""
    if provider == "mock":
        client_context["client"].configure(provider)
    else:
        client_context["client"].configure(provider, api_key="test-key")
    return client_context


@when(
    parsers.parse("I try to configure the client with provider \"{provider}\""),
    target_fixture="client_context",
)
def try_configure_invalid_provider(provider, client_context):
    """Try to configure client with invalid provider."""
    try:
        client_context["client"] = Client(provider=provider)
    except ProviderNotFoundError as e:
        client_context["error"] = e
        client_context["error_type"] = "ProviderNotFoundError"
    except ConfigurationError as e:
        client_context["error"] = e
        client_context["error_type"] = "ConfigurationError"
    return client_context


@when(
    parsers.parse("I try to configure the client with provider \"{provider}\" without api_key"),
    target_fixture="client_context",
)
def try_configure_without_api_key(provider, client_context):
    """Try to configure client without API key."""
    try:
        client_context["client"] = Client(provider=provider)
    except ConfigurationError as e:
        client_context["error"] = e
        client_context["error_type"] = "ConfigurationError"
    return client_context


# ========== THEN STEPS ==========


@then("the client is ready for use")
def client_is_ready(client_context):
    """Verify client is configured."""
    assert client_context["client"] is not None
    assert client_context["client"].is_configured is True


@then(parsers.parse("the active provider is \"{provider}\""))
def active_provider_is(provider, client_context):
    """Verify active provider."""
    assert client_context["client"].provider_name == provider


@then(parsers.parse("the active model is \"{model}\""))
def active_model_is(model, client_context):
    """Verify active model."""
    assert client_context["client"].model == model


@then(parsers.parse("I receive an error of type \"{error_type}\""))
def received_error_type(error_type, client_context):
    """Verify error type received."""
    assert client_context["error"] is not None
    assert client_context["error_type"] == error_type


@then(parsers.parse("the error message contains \"{text}\""))
def error_message_contains(text, client_context):
    """Verify error message contains text."""
    error_message = str(client_context["error"]).lower()
    assert text.lower() in error_message, f"'{text}' not in '{error_message}'"
