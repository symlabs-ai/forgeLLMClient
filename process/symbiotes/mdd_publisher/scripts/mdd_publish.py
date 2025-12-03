#!/usr/bin/env python3
"""
CLI unificado para MDD Publisher - Exportar artefatos em múltiplos formatos.

Este script simplifica o uso dos exporters, permitindo converter Markdown
para HTML, PDF, DOCX, Pitch ou Sites A/B/C com um único comando.

Uso:
  python symbiotas/mdd_publisher/scripts/mdd_publish.py \\
    --input project/docs/visao.md \\
    --format html

Formatos suportados: html, pdf, docx, pitch, sites
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


def export_html(input_path: Path, output_path: Path | None = None) -> int:
    """Exporta para HTML genérico."""
    from export_html import export_html as _export_html
    try:
        result = _export_html(input_path, output_path)
        print(f"✓ HTML gerado: {result}")
        return 0
    except Exception as e:
        print(f"✗ Erro ao exportar HTML: {e}", file=sys.stderr)
        return 1


def export_pdf(input_path: Path, output_path: Path | None = None) -> int:
    """Exporta para PDF."""
    from export_pdf import export_pdf as _export_pdf
    try:
        result = _export_pdf(input_path, output_path)
        print(f"✓ PDF gerado: {result}")
        return 0
    except Exception as e:
        print(f"✗ Erro ao exportar PDF: {e}", file=sys.stderr)
        return 1


def export_docx(input_path: Path, output_path: Path | None = None) -> int:
    """Exporta para DOCX."""
    from export_docx import export_docx as _export_docx
    try:
        result = _export_docx(input_path, output_path)
        print(f"✓ DOCX gerado: {result}")
        return 0
    except Exception as e:
        print(f"✗ Erro ao exportar DOCX: {e}", file=sys.stderr)
        return 1


def export_pitch(input_path: Path, output_path: Path | None = None) -> int:
    """Exporta pitch deck para HTML estilizado."""
    from export_pitch_html import export_pitch_html
    try:
        result = export_pitch_html(input_path, output_path)
        print(f"✓ Pitch HTML gerado: {result}")
        return 0
    except Exception as e:
        print(f"✗ Erro ao exportar Pitch: {e}", file=sys.stderr)
        return 1


def export_sites(
    input_dir: Path | None = None,
    output_dir: Path | None = None,
    templates_dir: Path | None = None,
    strict: bool = False
) -> int:
    """Exporta sites A/B/C."""
    from export_site_html import main as _export_sites_main

    # Constrói argumentos para o main
    args_list = []
    if input_dir:
        args_list.extend(["--input-dir", str(input_dir)])
    if output_dir:
        args_list.extend(["--output-dir", str(output_dir)])
    if templates_dir:
        args_list.extend(["--templates-dir", str(templates_dir)])
    if strict:
        args_list.append("--strict")

    # Injeta argumentos e executa
    original_argv = sys.argv
    try:
        sys.argv = ["export_site_html.py"] + args_list
        return _export_sites_main()
    finally:
        sys.argv = original_argv


def main() -> int:
    parser = argparse.ArgumentParser(
        description="MDD Publisher - CLI unificado para exportar artefatos",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:

  # Exportar para HTML
  python mdd_publish.py --input project/docs/visao.md --format html

  # Exportar para PDF
  python mdd_publish.py --input project/docs/sumario_executivo.md --format pdf

  # Exportar para DOCX
  python mdd_publish.py --input project/docs/hipotese.md --format docx

  # Exportar pitch deck
  python mdd_publish.py --input project/docs/pitch_deck.md --format pitch

  # Exportar todos os sites A/B/C
  python mdd_publish.py --format sites
  python mdd_publish.py --format sites --strict  # Com validação rigorosa

  # Exportar todos os formatos de um arquivo
  python mdd_publish.py --input project/docs/visao.md --format all
        """
    )

    parser.add_argument(
        "--input",
        type=Path,
        help="Caminho do arquivo .md de entrada (não necessário para --format sites)"
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Caminho do arquivo de saída (opcional, inferido por padrão)"
    )
    parser.add_argument(
        "--format",
        required=True,
        choices=["html", "pdf", "docx", "pitch", "sites", "all"],
        help="Formato de exportação"
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        help="Diretório de entrada (somente para --format sites)"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Diretório de saída (somente para --format sites)"
    )
    parser.add_argument(
        "--templates-dir",
        type=Path,
        help="Diretório com templates HTML (somente para --format sites)"
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Validação rigorosa de variáveis (somente para --format sites)"
    )

    args = parser.parse_args()

    # Validações
    if args.format != "sites" and args.format != "all" and not args.input:
        parser.error("--input é obrigatório para formatos html, pdf, docx e pitch")

    if args.format == "sites":
        return export_sites(
            input_dir=args.input_dir,
            output_dir=args.output_dir,
            templates_dir=args.templates_dir,
            strict=args.strict
        )

    # Valida arquivo de entrada
    if args.input and not args.input.exists():
        print(f"✗ Arquivo de entrada não encontrado: {args.input}", file=sys.stderr)
        return 2

    # Exporta formato único
    if args.format == "html":
        return export_html(args.input, args.output)
    if args.format == "pdf":
        return export_pdf(args.input, args.output)
    if args.format == "docx":
        return export_docx(args.input, args.output)
    if args.format == "pitch":
        return export_pitch(args.input, args.output)
    if args.format == "all":
        # Exporta todos os formatos
        print(f"Exportando '{args.input}' para todos os formatos...\n")
        results = []

        print("→ HTML...")
        results.append(export_html(args.input))

        print("→ PDF...")
        results.append(export_pdf(args.input))

        print("→ DOCX...")
        results.append(export_docx(args.input))

        # Verifica se algum falhou
        if any(r != 0 for r in results):
            print("\n⚠ Algumas exportações falharam")
            return 1
        print("\n✓ Todas as exportações concluídas com sucesso!")
        return 0

    return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n✗ Interrompido pelo usuário", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"\n✗ Erro fatal: {e}", file=sys.stderr)
        log_export(f"ERRO FATAL no CLI unificado: {e}")
        sys.exit(1)
