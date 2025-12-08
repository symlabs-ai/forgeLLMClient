"""API de desenvolvimento para agentes de IA.

Este modulo expoe as APIs do ForgeBase configuradas para o ForgeLLM,
permitindo que agentes de IA descubram componentes, verifiquem qualidade,
gerem codigo e executem testes.

Uso:
    from forge_llm.dev.api import ComponentDiscovery

    discovery = ComponentDiscovery()
    result = discovery.scan_project()
"""

from forgebase.dev.api import (
    ComponentDiscovery as _BaseComponentDiscovery,
)
from forgebase.dev.api import (
    QualityChecker,
    ScaffoldGenerator,
    TestRunner,
)

__all__ = [
    "ComponentDiscovery",
    "QualityChecker",
    "ScaffoldGenerator",
    "TestRunner",
]


class ComponentDiscovery(_BaseComponentDiscovery):  # type: ignore[misc]
    """Descoberta de componentes para ForgeLLM.

    Esta classe herda de forgebase.dev.api.ComponentDiscovery e
    configura automaticamente o package_name para 'forge_llm'.

    Uso:
        discovery = ComponentDiscovery()
        result = discovery.scan_project()

        for port in result.ports:
            print(f"{port.name} em {port.file_path}")
    """

    def __init__(self, package_name: str = "forge_llm") -> None:
        """Inicializa ComponentDiscovery para ForgeLLM.

        Args:
            package_name: Nome do pacote a escanear (default: forge_llm)
        """
        super().__init__(package_name=package_name)
