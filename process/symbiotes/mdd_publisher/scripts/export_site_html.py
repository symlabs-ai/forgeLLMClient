#!/usr/bin/env python3
"""
Renderiza variações de sites A/B/C de `project/docs/sites/` para `project/output/sites/site_01..03/`.

Mapeamento padrão:
  site_A.md -> output/sites/site_01/index.html
  site_B.md -> output/sites/site_02/index.html
  site_C.md -> output/sites/site_03/index.html

Uso:
  python symbiotas/mdd_publisher/scripts/export_site_html.py \
         [--input-dir project/docs/sites] [--output-dir project/output/sites]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
UTILS_DIR = SCRIPT_DIR / "utils"
if str(UTILS_DIR) not in sys.path:
    sys.path.insert(0, str(UTILS_DIR))

from helpers import log_export
from template_engine import render_site

# Importa configuração centralizada
try:
    from config import PROJECT_ROOT
except ImportError:
    PROJECT_ROOT = Path(__file__).parent.parent.parent.parent


def export_single(
    input_md: Path,
    site_dir: Path,
    template_dir: Path,
    strict_validation: bool = False
) -> Path:
    """
    Exporta um único site usando template engine.

    Args:
        input_md: Arquivo .md com conteúdo e front matter
        site_dir: Diretório de saída (ex: project/output/sites/site_01/)
        template_dir: Diretório do template HTML a usar
        strict_validation: Se True, valida todas as variáveis obrigatórias

    Returns:
        Path do arquivo index.html gerado
    """
    out_path = site_dir / "index.html"

    try:
        render_site(
            md_path=input_md,
            template_dir=template_dir,
            output_path=out_path,
            strict=strict_validation
        )
        log_export(f"Site exportado com template: {input_md} -> {out_path}")
        return out_path
    except Exception as e:
        log_export(f"ERRO ao exportar site {input_md}: {e}")
        raise


def main() -> int:
    ap = argparse.ArgumentParser(description="MDD Publisher - Exportar sites A/B/C para HTML com templates")
    ap.add_argument("--input-dir", default="project/docs/sites", help="Diretório com os .md")
    ap.add_argument("--output-dir", default="project/output/sites", help="Diretório base de saída")
    ap.add_argument("--templates-dir", default="process/templates/site_templates", help="Diretório com templates HTML")
    ap.add_argument("--strict", action="store_true", help="Validar variáveis obrigatórias")
    args = ap.parse_args()

    in_dir = Path(args.input_dir)
    out_dir = Path(args.output_dir)
    templates_base = Path(args.templates_dir)

    if not in_dir.exists():
        print(f"[ERRO] Diretório de entrada não encontrado: {in_dir}", file=sys.stderr)
        return 2

    # Mapeamento: arquivo MD -> diretório de saída + template a usar
    mapping = {
        "site_A.md": {
            "output_dir": out_dir / "site_01",
            "template": templates_base / "template_01"
        },
        "site_B.md": {
            "output_dir": out_dir / "site_02",
            "template": templates_base / "template_02"
        },
        "site_C.md": {
            "output_dir": out_dir / "site_03",
            "template": templates_base / "template_03"
        },
    }

    code = 0
    for fname, config in mapping.items():
        src = in_dir / fname
        if not src.exists():
            log_export(f"Aviso: arquivo não encontrado (pular): {src}")
            continue

        template_dir = config["template"]
        if not template_dir.exists():
            log_export(f"AVISO: Template não encontrado {template_dir}, pulando {fname}")
            continue

        try:
            export_single(
                input_md=src,
                site_dir=config["output_dir"],
                template_dir=template_dir,
                strict_validation=args.strict
            )
            print(f"✓ {fname} renderizado com sucesso usando {template_dir.name}")
        except Exception as exc:
            log_export(f"FALHA ao exportar site {src}: {exc}")
            print(f"✗ Erro ao exportar {fname}: {exc}", file=sys.stderr)
            code = 1

    return code


if __name__ == "__main__":
    raise SystemExit(main())
