#!/usr/bin/env python3
"""
Configuração centralizada para os scripts do MDD Publisher.

Este módulo define caminhos e configurações reutilizáveis,
eliminando hardcoding e facilitando manutenção.
"""
from pathlib import Path

# Detecta automaticamente a raiz do projeto
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent.parent

# Diretórios principais
DOCS_DIR = PROJECT_ROOT / "project" / "docs"
OUTPUT_DIR = PROJECT_ROOT / "project" / "output" / "docs"
OUTPUT_SITES_DIR = PROJECT_ROOT / "project" / "output" / "sites"
LOGS_DIR = PROJECT_ROOT / "project" / "output" / "logs"
TEMPLATES_DIR = PROJECT_ROOT / "process" / "templates"

# Configurações de log
LOG_FILE = LOGS_DIR / "export_history.log"
LOG_MAX_BYTES = 10 * 1024 * 1024  # 10MB
LOG_BACKUP_COUNT = 5

# Extensões suportadas
SUPPORTED_INPUT_EXTENSIONS = [".md", ".markdown"]
SUPPORTED_OUTPUT_FORMATS = ["html", "pdf", "docx"]


def ensure_directories():
    """Cria diretórios necessários se não existirem."""
    for directory in [OUTPUT_DIR, OUTPUT_SITES_DIR, LOGS_DIR]:
        directory.mkdir(parents=True, exist_ok=True)
