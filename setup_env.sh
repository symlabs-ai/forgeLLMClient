#!/usr/bin/env bash
set -euo pipefail

# =============================================================================
# setup_env.sh - Configuracao completa do ambiente de desenvolvimento
# ForgeLLMClient
# =============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"
TEMP_DIR="$SCRIPT_DIR/temp"
SCRIPTS_DIR="$SCRIPT_DIR/scripts"

echo "=============================================="
echo " ForgeLLMClient - Setup do Ambiente"
echo "=============================================="

# -----------------------------------------------------------------------------
# 1. Criar/Recriar virtualenv com Python 3.12
# -----------------------------------------------------------------------------
echo ""
echo "[1/6] Configurando virtualenv com Python 3.12..."

if [ -d "$VENV_DIR" ]; then
    echo "      Removendo venv existente..."
    rm -rf "$VENV_DIR"
fi

python3.12 -m venv "$VENV_DIR"
echo "      Virtualenv criado em $VENV_DIR"

# Ativar venv
source "$VENV_DIR/bin/activate"
echo "      Virtualenv ativado"

# -----------------------------------------------------------------------------
# 2. Atualizar pip
# -----------------------------------------------------------------------------
echo ""
echo "[2/6] Atualizando pip..."
pip install --upgrade pip

# -----------------------------------------------------------------------------
# 3. Instalar ForgeBase do repositorio git
# -----------------------------------------------------------------------------
echo ""
echo "[3/6] Instalando ForgeBase (pode demorar - clonando repositorio)..."
pip install --no-cache-dir --progress-bar on git+https://github.com/symlabs-ai/forgebase.git

# -----------------------------------------------------------------------------
# 4. Instalar dependencias de desenvolvimento
# -----------------------------------------------------------------------------
echo ""
echo "[4/6] Instalando dependencias de desenvolvimento..."
pip install --progress-bar on -r "$TEMP_DIR/requirements-dev.txt"

# -----------------------------------------------------------------------------
# 5. Configurar arquivos de automacao (scripts/)
# -----------------------------------------------------------------------------
echo ""
echo "[5/6] Configurando arquivos de automacao..."

# Criar diretorio scripts/ se nao existir
mkdir -p "$SCRIPTS_DIR"

# Copiar arquivos de configuracao do temp para scripts/
cp "$TEMP_DIR/pre-commit-config.yaml" "$SCRIPTS_DIR/.pre-commit-config.yaml"
cp "$TEMP_DIR/ruff.toml" "$SCRIPTS_DIR/ruff.toml"

# Ajustar path do ruff.toml no pre-commit config
sed -i 's|scripts/ruff.toml|ruff.toml|g' "$SCRIPTS_DIR/.pre-commit-config.yaml"

echo "      Arquivos copiados para scripts/"

# -----------------------------------------------------------------------------
# 6. Instalar e configurar pre-commit hooks
# -----------------------------------------------------------------------------
echo ""
echo "[6/6] Configurando pre-commit hooks..."

# Instalar pre-commit se nao estiver instalado
if ! command -v pre-commit >/dev/null 2>&1; then
    pip install pre-commit
fi

# Instalar hooks
pre-commit install --config "$SCRIPTS_DIR/.pre-commit-config.yaml"

echo "      Pre-commit hooks instalados"

# Rodar baseline (opcional, pode falhar em arquivos existentes)
echo ""
echo "      Rodando pre-commit baseline (pode haver warnings)..."
pre-commit run --config "$SCRIPTS_DIR/.pre-commit-config.yaml" --all-files || true

# -----------------------------------------------------------------------------
# Resumo final
# -----------------------------------------------------------------------------
echo ""
echo "=============================================="
echo " Setup concluido!"
echo "=============================================="
echo ""
echo " Para ativar o ambiente:"
echo "   source .venv/bin/activate"
echo ""
echo " Estrutura criada:"
echo "   .venv/                    - Virtualenv Python 3.12"
echo "   scripts/.pre-commit-config.yaml"
echo "   scripts/ruff.toml"
echo ""
echo " Dependencias instaladas:"
echo "   - ForgeBase (framework)"
echo "   - pytest, pytest-bdd, pytest-cov"
echo "   - ruff, mypy, hypothesis"
echo "   - import-linter, deptry"
echo "   - pre-commit"
echo ""
echo " Comandos uteis:"
echo "   pytest tests/             - Rodar testes"
echo "   pytest tests/bdd/ -m ci_fast  - Testes BDD rapidos"
echo "   ruff check src/           - Verificar lint"
echo "   ruff format src/          - Formatar codigo"
echo "   mypy src/                 - Verificar tipos"
echo ""
