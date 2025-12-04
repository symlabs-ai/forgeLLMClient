"""Testes para excecoes de dominio - TDD RED phase."""

import pytest


class TestForgeError:
    """Testes para excecao base ForgeError."""

    def test_forge_error_is_exception(self):
        """ForgeError deve ser uma Exception."""
        from forge_llm.domain.exceptions import ForgeError

        assert issubclass(ForgeError, Exception)

    def test_forge_error_with_message(self):
        """ForgeError deve aceitar mensagem."""
        from forge_llm.domain.exceptions import ForgeError

        error = ForgeError("Erro de teste")
        assert str(error) == "Erro de teste"


class TestProviderError:
    """Testes para ProviderError."""

    def test_provider_error_inherits_forge_error(self):
        """ProviderError deve herdar de ForgeError."""
        from forge_llm.domain.exceptions import ForgeError, ProviderError

        assert issubclass(ProviderError, ForgeError)

    def test_provider_error_has_provider_attribute(self):
        """ProviderError deve ter atributo provider."""
        from forge_llm.domain.exceptions import ProviderError

        error = ProviderError("Erro", provider="openai")
        assert error.provider == "openai"

    def test_provider_error_has_status_code(self):
        """ProviderError deve ter atributo status_code opcional."""
        from forge_llm.domain.exceptions import ProviderError

        error = ProviderError("Erro", provider="openai", status_code=500)
        assert error.status_code == 500

    def test_provider_error_status_code_default_none(self):
        """ProviderError status_code deve ser None por padrao."""
        from forge_llm.domain.exceptions import ProviderError

        error = ProviderError("Erro", provider="openai")
        assert error.status_code is None


class TestAuthenticationError:
    """Testes para AuthenticationError."""

    def test_authentication_error_inherits_forge_error(self):
        """AuthenticationError deve herdar de ForgeError."""
        from forge_llm.domain.exceptions import AuthenticationError, ForgeError

        assert issubclass(AuthenticationError, ForgeError)

    def test_authentication_error_has_provider(self):
        """AuthenticationError deve ter atributo provider."""
        from forge_llm.domain.exceptions import AuthenticationError

        error = AuthenticationError("API key invalida", provider="openai")
        assert error.provider == "openai"


class TestRateLimitError:
    """Testes para RateLimitError."""

    def test_rate_limit_error_inherits_forge_error(self):
        """RateLimitError deve herdar de ForgeError."""
        from forge_llm.domain.exceptions import ForgeError, RateLimitError

        assert issubclass(RateLimitError, ForgeError)

    def test_rate_limit_error_has_retry_after(self):
        """RateLimitError deve ter atributo retry_after."""
        from forge_llm.domain.exceptions import RateLimitError

        error = RateLimitError("Rate limit", provider="openai", retry_after=60)
        assert error.retry_after == 60

    def test_rate_limit_error_retry_after_default_none(self):
        """RateLimitError retry_after deve ser None por padrao."""
        from forge_llm.domain.exceptions import RateLimitError

        error = RateLimitError("Rate limit", provider="openai")
        assert error.retry_after is None


class TestConfigurationError:
    """Testes para ConfigurationError."""

    def test_configuration_error_inherits_forge_error(self):
        """ConfigurationError deve herdar de ForgeError."""
        from forge_llm.domain.exceptions import ConfigurationError, ForgeError

        assert issubclass(ConfigurationError, ForgeError)


class TestValidationError:
    """Testes para ValidationError."""

    def test_validation_error_inherits_forge_error(self):
        """ValidationError deve herdar de ForgeError."""
        from forge_llm.domain.exceptions import ForgeError, ValidationError

        assert issubclass(ValidationError, ForgeError)


class TestToolNotFoundError:
    """Testes para ToolNotFoundError."""

    def test_tool_not_found_error_inherits_forge_error(self):
        """ToolNotFoundError deve herdar de ForgeError."""
        from forge_llm.domain.exceptions import ForgeError, ToolNotFoundError

        assert issubclass(ToolNotFoundError, ForgeError)

    def test_tool_not_found_error_has_tool_name(self):
        """ToolNotFoundError deve ter atributo tool_name."""
        from forge_llm.domain.exceptions import ToolNotFoundError

        error = ToolNotFoundError("calculator", available_tools=["search", "weather"])
        assert error.tool_name == "calculator"

    def test_tool_not_found_error_has_available_tools(self):
        """ToolNotFoundError deve ter lista de tools disponiveis."""
        from forge_llm.domain.exceptions import ToolNotFoundError

        error = ToolNotFoundError("calculator", available_tools=["search", "weather"])
        assert error.available_tools == ["search", "weather"]


class TestAPITimeoutError:
    """Testes para APITimeoutError."""

    def test_api_timeout_error_inherits_forge_error(self):
        """APITimeoutError deve herdar de ForgeError."""
        from forge_llm.domain.exceptions import APITimeoutError, ForgeError

        assert issubclass(APITimeoutError, ForgeError)

    def test_api_timeout_error_has_provider(self):
        """APITimeoutError deve ter atributo provider."""
        from forge_llm.domain.exceptions import APITimeoutError

        error = APITimeoutError("Timeout", provider="openai")
        assert error.provider == "openai"

    def test_api_timeout_error_has_timeout(self):
        """APITimeoutError deve ter atributo timeout."""
        from forge_llm.domain.exceptions import APITimeoutError

        error = APITimeoutError("Timeout", provider="openai", timeout=30.0)
        assert error.timeout == 30.0

    def test_api_timeout_error_timeout_default_none(self):
        """APITimeoutError timeout deve ser None por padrao."""
        from forge_llm.domain.exceptions import APITimeoutError

        error = APITimeoutError("Timeout", provider="openai")
        assert error.timeout is None


class TestAPIError:
    """Testes para APIError."""

    def test_api_error_inherits_forge_error(self):
        """APIError deve herdar de ForgeError."""
        from forge_llm.domain.exceptions import APIError, ForgeError

        assert issubclass(APIError, ForgeError)

    def test_api_error_has_provider(self):
        """APIError deve ter atributo provider."""
        from forge_llm.domain.exceptions import APIError

        error = APIError("API error", provider="openai")
        assert error.provider == "openai"

    def test_api_error_has_status_code(self):
        """APIError deve ter atributo status_code."""
        from forge_llm.domain.exceptions import APIError

        error = APIError("API error", provider="openai", status_code=500)
        assert error.status_code == 500

    def test_api_error_has_retryable_flag(self):
        """APIError deve ter flag retryable."""
        from forge_llm.domain.exceptions import APIError

        error = APIError("API error", provider="openai", retryable=True)
        assert error.retryable is True

    def test_api_error_retryable_default_false(self):
        """APIError retryable deve ser False por padrao."""
        from forge_llm.domain.exceptions import APIError

        error = APIError("API error", provider="openai")
        assert error.retryable is False


class TestRetryExhaustedError:
    """Testes para RetryExhaustedError."""

    def test_retry_exhausted_error_inherits_forge_error(self):
        """RetryExhaustedError deve herdar de ForgeError."""
        from forge_llm.domain.exceptions import ForgeError, RetryExhaustedError

        assert issubclass(RetryExhaustedError, ForgeError)

    def test_retry_exhausted_error_has_provider(self):
        """RetryExhaustedError deve ter atributo provider."""
        from forge_llm.domain.exceptions import RetryExhaustedError

        error = RetryExhaustedError("All retries failed", provider="openai", attempts=3)
        assert error.provider == "openai"

    def test_retry_exhausted_error_has_attempts(self):
        """RetryExhaustedError deve ter atributo attempts."""
        from forge_llm.domain.exceptions import RetryExhaustedError

        error = RetryExhaustedError("All retries failed", provider="openai", attempts=3)
        assert error.attempts == 3

    def test_retry_exhausted_error_has_last_error(self):
        """RetryExhaustedError deve ter atributo last_error."""
        from forge_llm.domain.exceptions import RateLimitError, RetryExhaustedError

        last = RateLimitError("Rate limit", "openai")
        error = RetryExhaustedError(
            "All retries failed", provider="openai", attempts=3, last_error=last
        )
        assert error.last_error is last

    def test_retry_exhausted_error_last_error_default_none(self):
        """RetryExhaustedError last_error deve ser None por padrao."""
        from forge_llm.domain.exceptions import RetryExhaustedError

        error = RetryExhaustedError("All retries failed", provider="openai", attempts=3)
        assert error.last_error is None
