#!/usr/bin/env python3
"""
Renderiza `project/docs/pitch_deck.md` em HTML específico de pitch.

Uso:
  python symbiotas/mdd_publisher/scripts/export_pitch_html.py \
         --input project/docs/pitch_deck.md \
         [--output project/output/docs/pitch_deck.html]
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
    log_export,
    md_to_html_basic,
    read_text,
    wrap_html,
    write_text,
)

PITCH_CSS = """
/* Estilos básicos focados em apresentação de pitch */
body { background: #ffffff; color: #0d1117; }
.slide { margin: 2.5rem 0; padding: 1.5rem; border-radius: 12px; background: #f7f9fb; border: 1px solid #eaecef; }
.slide h1, .slide h2 { margin-top: 0; }
.cta { display: inline-block; margin-top: 1rem; background: #2b70c9; color: #fff; padding: .6rem 1rem; border-radius: 8px; }
""".strip()


def export_pitch_html(input_md: Path, output_html: Path | None = None) -> Path:
    text = read_text(input_md)
    body = md_to_html_basic(text)
    # Simples: encapsula em um container .slide
    slide_wrapped = f"<div class=\"slide\">\n{body}\n</div>"
    html = wrap_html(title="Pitch de Valor", body_html=slide_wrapped, extra_css=PITCH_CSS)
    out_path = output_html or Path("project/output/docs/pitch_deck.html")
    write_text(out_path, html)
    log_export(f"Pitch HTML exportado: {input_md} -> {out_path}")
    return out_path


def main() -> int:
    ap = argparse.ArgumentParser(description="MDD Publisher - Exportar Pitch Deck para HTML")
    ap.add_argument("--input", required=True, help="Caminho do arquivo pitch_deck.md")
    ap.add_argument("--output", required=False, help="Caminho do .html de saída")
    args = ap.parse_args()

    in_path = Path(args.input)
    if not in_path.exists():
        print(f"[ERRO] Arquivo de entrada não encontrado: {in_path}", file=sys.stderr)
        return 2
    out_path = Path(args.output) if args.output else None
    try:
        final_path = export_pitch_html(in_path, out_path)
        print(str(final_path))
        return 0
    except Exception as exc:
        log_export(f"FALHA ao exportar Pitch HTML: {in_path} - {exc}")
        print(f"[ERRO] Falha ao exportar Pitch HTML: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
