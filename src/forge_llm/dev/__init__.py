"""Modulo de desenvolvimento para agentes de IA.

Este modulo fornece ferramentas para agentes de codigo de IA (Claude Code,
Cursor, GitHub Copilot, Aider, etc.) trabalharem com o ForgeLLM de forma
programatica.

Seguindo o padrao ForgeBase, este modulo expoe:
- get_agent_quickstart(): Retorna guia de uso em markdown
- get_documentation_path(): Retorna caminho para documentacao
- ComponentDiscovery: API para descoberta de componentes

Uso:
    from forge_llm.dev import get_agent_quickstart

    guide = get_agent_quickstart()
    print(guide)

    from forge_llm.dev.api import ComponentDiscovery

    discovery = ComponentDiscovery()
    result = discovery.scan_project()
"""

from pathlib import Path

__all__ = [
    "get_agent_quickstart",
    "get_documentation_path",
    "resources",
]


def get_documentation_path() -> Path:
    """Retorna o caminho para a pasta de recursos de documentacao.

    Returns:
        Path para a pasta resources/ dentro do modulo dev
    """
    return Path(__file__).parent / "resources"


def get_agent_quickstart() -> str:
    """Retorna o guia rapido para agentes de IA em formato markdown.

    Este metodo permite que agentes de codigo carreguem o guia
    programaticamente, mesmo quando o pacote foi instalado via pip.

    Returns:
        Conteudo do arquivo agent_quickstart.md

    Example:
        >>> from forge_llm.dev import get_agent_quickstart
        >>> guide = get_agent_quickstart()
        >>> print(guide[:50])
        # ForgeLLM - Guia Rapido para Agentes de IA
    """
    quickstart_path = get_documentation_path() / "agent_quickstart.md"
    return quickstart_path.read_text(encoding="utf-8")


# Submodulo para recursos
class _ResourcesModule:
    """Namespace para acessar recursos como atributos."""

    @property
    def agent_quickstart(self) -> str:
        """Acessa o guia rapido."""
        return get_agent_quickstart()


resources = _ResourcesModule()
