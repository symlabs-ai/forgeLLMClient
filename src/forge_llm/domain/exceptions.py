"""Excecoes de dominio do ForgeLLMClient."""


class ForgeError(Exception):
    """Excecao base do ForgeLLMClient."""

    pass


class ValidationError(ForgeError):
    """Erro de validacao de dados."""

    pass


class ProviderError(ForgeError):
    """Erro ao comunicar com provedor LLM."""

    def __init__(
        self,
        message: str,
        provider: str,
        status_code: int | None = None,
    ) -> None:
        super().__init__(message)
        self.provider = provider
        self.status_code = status_code


class AuthenticationError(ProviderError):
    """Erro de autenticacao com provedor."""

    def __init__(self, message: str, provider: str) -> None:
        super().__init__(message, provider, status_code=401)


class RateLimitError(ProviderError):
    """Erro de rate limit do provedor."""

    def __init__(
        self,
        message: str,
        provider: str,
        retry_after: int | None = None,
    ) -> None:
        super().__init__(message, provider, status_code=429)
        self.retry_after = retry_after


class ConfigurationError(ForgeError):
    """Erro de configuracao."""

    pass


class ToolNotFoundError(ForgeError):
    """Ferramenta nao encontrada."""

    def __init__(self, tool_name: str, available_tools: list[str]) -> None:
        super().__init__(f"Tool '{tool_name}' nao encontrada")
        self.tool_name = tool_name
        self.available_tools = available_tools


class ToolCallNotFoundError(ForgeError):
    """Tool call nao encontrado."""

    def __init__(self, tool_call_id: str) -> None:
        super().__init__(f"tool_call not found: '{tool_call_id}'")
        self.tool_call_id = tool_call_id


class APITimeoutError(ProviderError):
    """Erro de timeout na chamada de API."""

    def __init__(
        self,
        message: str,
        provider: str,
        timeout: float | None = None,
    ) -> None:
        super().__init__(message, provider, status_code=408)
        self.timeout = timeout


class APIError(ProviderError):
    """Erro generico de API."""

    def __init__(
        self,
        message: str,
        provider: str,
        status_code: int | None = None,
        retryable: bool = False,
    ) -> None:
        super().__init__(message, provider, status_code)
        self.retryable = retryable


class RetryExhaustedError(ForgeError):
    """Erro quando todas as tentativas de retry foram esgotadas."""

    def __init__(
        self,
        message: str,
        provider: str,
        attempts: int,
        last_error: Exception | None = None,
    ) -> None:
        super().__init__(message)
        self.provider = provider
        self.attempts = attempts
        self.last_error = last_error
