"""Registry de provedores LLM."""

from typing import Any

from forge_llm.application.ports.provider_port import ProviderPort
from forge_llm.domain.exceptions import ConfigurationError


class ProviderNotFoundError(ConfigurationError):
    """Provedor nao encontrado no registry."""

    def __init__(self, provider_name: str, available: list[str]) -> None:
        super().__init__(
            f"Provedor '{provider_name}' nao encontrado. "
            f"Disponiveis: {', '.join(available)}"
        )
        self.provider_name = provider_name
        self.available_providers = available


class ProviderRegistry:
    """
    Registry central de provedores disponiveis.

    Permite registrar, obter e listar provedores.
    """

    _providers: dict[str, type[ProviderPort]] = {}

    @classmethod
    def register(cls, name: str, provider_class: type[ProviderPort]) -> None:
        """
        Registrar um provider.

        Args:
            name: Nome identificador do provider
            provider_class: Classe do provider
        """
        cls._providers[name] = provider_class

    @classmethod
    def get(cls, name: str) -> type[ProviderPort]:
        """
        Obter classe de provider pelo nome.

        Args:
            name: Nome do provider

        Returns:
            Classe do provider

        Raises:
            ProviderNotFoundError: Se provider nao existe
        """
        if name not in cls._providers:
            raise ProviderNotFoundError(name, list(cls._providers.keys()))
        return cls._providers[name]

    @classmethod
    def create(
        cls,
        name: str,
        api_key: str | None = None,
        **kwargs: Any,
    ) -> ProviderPort:
        """
        Criar instancia de provider.

        Args:
            name: Nome do provider
            api_key: API key (se necessario)
            **kwargs: Argumentos adicionais

        Returns:
            Instancia do provider
        """
        provider_class = cls.get(name)

        # Mocks nao precisam de api_key
        if name in ("mock", "mock-tools", "mock-no-tokens", "mock-alt"):
            return provider_class(**kwargs)

        # Outros providers precisam de api_key
        if api_key is None:
            raise ConfigurationError(
                f"api_key e obrigatorio para o provedor '{name}'"
            )

        return provider_class(api_key=api_key, **kwargs)

    @classmethod
    def list_available(cls) -> list[str]:
        """Listar providers disponiveis."""
        return list(cls._providers.keys())

    @classmethod
    def clear(cls) -> None:
        """Limpar registry (para testes)."""
        cls._providers.clear()


# Registrar providers padrao
def _register_default_providers() -> None:
    """Registrar providers padrao."""
    from forge_llm.providers.anthropic_provider import AnthropicProvider
    from forge_llm.providers.mock_alt_provider import MockAltProvider
    from forge_llm.providers.mock_no_tokens_provider import MockNoTokensProvider
    from forge_llm.providers.mock_provider import MockProvider
    from forge_llm.providers.mock_tools_provider import MockToolsProvider
    from forge_llm.providers.openai_provider import OpenAIProvider
    from forge_llm.providers.openrouter_provider import OpenRouterProvider

    ProviderRegistry.register("mock", MockProvider)
    ProviderRegistry.register("mock-tools", MockToolsProvider)
    ProviderRegistry.register("mock-no-tokens", MockNoTokensProvider)
    ProviderRegistry.register("mock-alt", MockAltProvider)
    ProviderRegistry.register("openai", OpenAIProvider)
    ProviderRegistry.register("anthropic", AnthropicProvider)
    ProviderRegistry.register("openrouter", OpenRouterProvider)


_register_default_providers()
