#!/usr/bin/env python3
"""
Exporta Markdown (.md) para PDF.

Requer uma das bibliotecas opcionais para renderização:
- weasyprint (HTML -> PDF) ou
- pdfkit + wkhtmltopdf (HTML -> PDF)

Fallback: se nenhuma estiver disponível, o script falha com mensagem clara e
registra no log.

Uso:
  python symbiotas/mdd_publisher/scripts/export_pdf.py \
         --input project/docs/sumario_executivo.md \
         [--output project/output/docs/sumario_executivo.pdf]
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
UTILS_DIR = SCRIPT_DIR / "utils"
if str(UTILS_DIR) not in sys.path:
    sys.path.insert(0, str(UTILS_DIR))

from helpers import (
    ExportError,
    MissingDependencyError,
    default_output_for_md,
    log_export,
    md_to_html_basic,
    read_text,
    wrap_html,
)

# Importa configuração centralizada
try:
    from config import OUTPUT_DIR
except ImportError:
    # Fallback para compatibilidade
    OUTPUT_DIR = Path("project/output/docs")


def _html_to_pdf_weasyprint(html: str, output_pdf: Path) -> None:
    try:
        from weasyprint import HTML  # type: ignore
    except Exception as e:  # pragma: no cover
        raise MissingDependencyError("weasyprint não disponível") from e
    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    HTML(string=html).write_pdf(str(output_pdf))


def _html_to_pdf_pdfkit(html: str, output_pdf: Path) -> None:
    try:
        import pdfkit  # type: ignore
    except Exception as e:  # pragma: no cover
        raise MissingDependencyError("pdfkit não disponível") from e
    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    pdfkit.from_string(html, str(output_pdf))


def _html_to_pdf_wkhtmltopdf_cli(html: str, output_pdf: Path) -> None:
    """Fallback direto usando o binário wkhtmltopdf, sem depender do pacote pdfkit.

    Requer que `wkhtmltopdf` esteja disponível no PATH.
    """
    exe = shutil.which("wkhtmltopdf")
    if not exe:
        raise MissingDependencyError("wkhtmltopdf não encontrado no PATH")
    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as tmp:
        tmp.write(html)
        tmp_path = tmp.name
    # Executa o binário
    try:
        subprocess.run([exe, tmp_path, str(output_pdf)], check=True, capture_output=True)
    finally:
        try:
            Path(tmp_path).unlink(missing_ok=True)
        except Exception:
            pass


def export_pdf(input_md: Path, output_pdf: Path | None = None) -> Path:
    """
    Exporta arquivo Markdown para PDF usando weasyprint ou pdfkit.

    Args:
        input_md: Caminho do arquivo .md de entrada
        output_pdf: Caminho opcional do .pdf de saída

    Returns:
        Path do arquivo PDF gerado

    Raises:
        ExportError: Se nenhum backend de PDF estiver disponível
        InvalidInputError: Se o arquivo de entrada não existir
    """
    text = read_text(input_md)
    body = md_to_html_basic(text)
    html = wrap_html(title=input_md.stem, body_html=body)
    out_path = output_pdf or default_output_for_md(input_md, OUTPUT_DIR, ".pdf")

    # Tenta conversores em ordem
    tried: list[str] = []
    try:
        _html_to_pdf_weasyprint(html, out_path)
        log_export(f"PDF exportado (weasyprint): {input_md} -> {out_path}")
        return out_path
    except Exception as e:
        tried.append(f"weasyprint: {e}")
    try:
        _html_to_pdf_pdfkit(html, out_path)
        log_export(f"PDF exportado (pdfkit): {input_md} -> {out_path}")
        return out_path
    except Exception as e:
        tried.append(f"pdfkit: {e}")
    try:
        _html_to_pdf_wkhtmltopdf_cli(html, out_path)
        log_export(f"PDF exportado (wkhtmltopdf CLI): {input_md} -> {out_path}")
        return out_path
    except Exception as e:
        tried.append(f"wkhtmltopdf: {e}")

    # Fallback: registra erro e aborta
    details = "; ".join(tried)
    log_export(f"FALHA ao exportar PDF: {input_md} -> {out_path} ({details})")
    raise ExportError(
        "Nenhum backend de PDF disponível. Instale 'weasyprint' ou 'pdfkit+wkhtmltopdf'."
    )


def main() -> int:
    ap = argparse.ArgumentParser(description="MDD Publisher - Exportar Markdown para PDF")
    ap.add_argument("--input", required=True, help="Caminho do arquivo .md de entrada")
    ap.add_argument("--output", required=False, help="Caminho do .pdf de saída")
    args = ap.parse_args()

    in_path = Path(args.input)
    if not in_path.exists():
        print(f"[ERRO] Arquivo de entrada não encontrado: {in_path}", file=sys.stderr)
        return 2
    out_path = Path(args.output) if args.output else None
    try:
        final_path = export_pdf(in_path, out_path)
        print(str(final_path))
        return 0
    except ExportError as ee:
        print(f"[ERRO] {ee}", file=sys.stderr)
        return 1
    except Exception as exc:
        log_export(f"FALHA ao exportar PDF: {in_path} - {exc}")
        print(f"[ERRO] Falha ao exportar PDF: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
