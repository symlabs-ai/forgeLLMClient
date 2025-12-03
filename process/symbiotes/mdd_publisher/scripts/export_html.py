#!/usr/bin/env python3
"""
Exporta Markdown (.md) para HTML.

Uso:
  python symbiotas/mdd_publisher/scripts/export_html.py \
         --input project/docs/sumario_executivo.md \
         [--output project/output/docs/sumario_executivo.html]

Se --output não for informado, salvará em `project/output/docs/` replicando a estrutura
de `project/docs/` e trocando a extensão para .html.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
UTILS_DIR = SCRIPT_DIR / "utils"
if str(UTILS_DIR) not in sys.path:
    sys.path.insert(0, str(UTILS_DIR))

from helpers import (
    ExportError,
    default_output_for_md,
    log_export,
    md_to_html_basic,
    read_text,
    wrap_html,
    write_text,
)

# Importa configuração centralizada
try:
    from config import OUTPUT_DIR
except ImportError:
    OUTPUT_DIR = Path("project/output/docs")


def export_html(input_md: Path, output_html: Path | None = None) -> Path:
    """
    Exporta arquivo Markdown para HTML.

    Args:
        input_md: Caminho do arquivo .md de entrada
        output_html: Caminho opcional do .html de saída

    Returns:
        Path do arquivo HTML gerado

    Raises:
        InvalidInputError: Se o arquivo de entrada não existir
    """
    text = read_text(input_md)
    body = md_to_html_basic(text)
    html = wrap_html(title=input_md.stem, body_html=body)
    out_path = output_html or default_output_for_md(input_md, OUTPUT_DIR, ".html")
    write_text(out_path, html)
    log_export(f"HTML exportado: {input_md} -> {out_path}")
    return out_path


def main() -> int:
    ap = argparse.ArgumentParser(description="MDD Publisher - Exportar Markdown para HTML")
    ap.add_argument("--input", required=True, help="Caminho do arquivo .md de entrada")
    ap.add_argument("--output", required=False, help="Caminho do .html de saída")
    args = ap.parse_args()

    in_path = Path(args.input)
    if not in_path.exists():
        print(f"[ERRO] Arquivo de entrada não encontrado: {in_path}", file=sys.stderr)
        return 2
    out_path = Path(args.output) if args.output else None
    try:
        final_path = export_html(in_path, out_path)
        print(str(final_path))
        return 0
    except ExportError as ee:
        print(f"[ERRO] {ee}", file=sys.stderr)
        return 1
    except Exception as exc:
        log_export(f"FALHA ao exportar HTML: {in_path} - {exc}")
        print(f"[ERRO] Falha ao exportar HTML: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
