import logging
import re
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path


# Exceções customizadas
class ExportError(Exception):
    """Erro base para falhas de exportação no MDD Publisher."""
    pass


class MissingDependencyError(ExportError):
    """Erro quando uma dependência necessária não está disponível."""
    pass


class InvalidInputError(ExportError):
    """Erro quando o arquivo de entrada é inválido."""
    pass


def ensure_dir(path: Path) -> None:
    """Cria diretório recursivamente se não existir."""
    path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path, encoding: str = "utf-8") -> str:
    """Lê arquivo de texto com validação."""
    if not path.exists():
        raise InvalidInputError(f"Arquivo não encontrado: {path}")
    return path.read_text(encoding=encoding)


def write_text(path: Path, content: str, encoding: str = "utf-8") -> None:
    """Escreve arquivo de texto criando diretórios necessários."""
    ensure_dir(path.parent)
    path.write_text(content, encoding=encoding)


def log_export(message: str, base_dir: Path = Path("project/output/logs")) -> None:
    """
    Registra mensagem de exportação com rotação automática de logs.

    Logs são rotacionados quando atingem 10MB, mantendo até 5 backups.
    """
    ensure_dir(base_dir)
    log_path = base_dir / "export_history.log"

    # Configura logger com rotação
    logger = logging.getLogger("mdd_publisher")
    if not logger.handlers:
        handler = RotatingFileHandler(
            log_path,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
            encoding="utf-8"
        )
        formatter = logging.Formatter("[%(asctime)s] %(message)s", "%Y-%m-%d %H:%M:%S")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

    logger.info(message)


def md_to_html_basic(markdown_text: str) -> str:
    """
    Converte Markdown para HTML.
    - Se o módulo 'markdown' estiver disponível, usa-o.
    - Caso contrário, aplica uma conversão melhorada com suporte a:
      * Títulos (h1-h6)
      * **Bold**, *Italic*, `code inline`
      * [Links](url)
      * Listas ordenadas e não-ordenadas
      * Blockquotes
      * Código em bloco
      * Linhas horizontais
    """
    try:
        import markdown  # type: ignore
        return markdown.markdown(
            markdown_text,
            extensions=[
                "extra",
                "smarty",
                "sane_lists",
                "toc",
                "fenced_code",
                "tables",
            ],
            output_format="html5",
        )
    except Exception:
        # Conversão melhorada com regex como fallback
        lines = markdown_text.splitlines()
        html_lines = ["<div class=\"md-fallback\">"]
        in_code = False
        in_list = False
        list_type: str | None = None  # 'ul' ou 'ol'

        for ln in lines:
            # Código em bloco (fenced)
            if ln.strip().startswith("```"):
                if not in_code:
                    html_lines.append("<pre><code>")
                    in_code = True
                else:
                    html_lines.append("</code></pre>")
                    in_code = False
                continue

            if in_code:
                html_lines.append(_escape_html(ln))
                continue

            # Fecha lista se necessário
            if in_list and not (
                ln.strip().startswith(("-", "*")) or re.match(r"^\d+\.\s", ln.strip())
            ):
                html_lines.append("</ul>" if list_type == 'ul' else "</ol>")
                in_list = False
                list_type = None

            # Títulos (h1-h6)
            if ln.startswith("#### "):
                html_lines.append(f"<h4>{_inline_format(ln[5:].strip())}</h4>")
            elif ln.startswith("### "):
                html_lines.append(f"<h3>{_inline_format(ln[4:].strip())}</h3>")
            elif ln.startswith("## "):
                html_lines.append(f"<h2>{_inline_format(ln[3:].strip())}</h2>")
            elif ln.startswith("# "):
                html_lines.append(f"<h1>{_inline_format(ln[2:].strip())}</h1>")
            # Linha horizontal
            elif ln.strip() == "---":
                html_lines.append("<hr />")
            # Blockquote
            elif ln.startswith("> "):
                html_lines.append(f"<blockquote>{_inline_format(ln[2:].strip())}</blockquote>")
            # Lista não-ordenada
            elif ln.strip().startswith(("-", "*")) and len(ln.strip()) > 2:
                if not in_list:
                    html_lines.append("<ul>")
                    in_list = True
                    list_type = 'ul'
                html_lines.append(f"<li>{_inline_format(ln.strip()[2:].strip())}</li>")
            # Lista ordenada
            elif re.match(r"^\d+\.\s", ln.strip()):
                if not in_list:
                    html_lines.append("<ol>")
                    in_list = True
                    list_type = 'ol'
                content = re.sub(r"^\d+\.\s+", "", ln.strip())
                html_lines.append(f"<li>{_inline_format(content)}</li>")
            # Parágrafo
            elif ln.strip():
                html_lines.append(f"<p>{_inline_format(ln)}</p>")
            else:
                html_lines.append("")

        if in_list:
            html_lines.append("</ul>" if list_type == 'ul' else "</ol>")

        html_lines.append("</div>")
        return "\n".join(html_lines)


def _inline_format(text: str) -> str:
    """Aplica formatação inline (bold, italic, code, links)."""
    # Links [texto](url)
    text = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', text)
    # Bold **texto**
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Italic *texto*
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    # Code inline `texto`
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    return text


def _escape_html(text: str) -> str:
    """Escapa caracteres HTML especiais."""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


BASE_STYLE = """
body { font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif; margin: 2rem auto; max-width: 860px; color: #0d1117; background: #ffffff; }
code, pre { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }
pre { background: #f6f8fa; padding: 1rem; border-radius: 8px; overflow: auto; }
h1, h2, h3 { color: #0d1117; }
a { color: #2b70c9; text-decoration: none; }
a:hover { text-decoration: underline; }
hr { border: none; border-top: 1px solid #eaecef; margin: 2rem 0; }
blockquote { margin: 1rem 0; padding: .5rem 1rem; background: #f6f8fa; border-left: 4px solid #b4c7e7; }
table { border-collapse: collapse; }
td, th { border: 1px solid #eaecef; padding: .5rem .75rem; }
""".strip()


def wrap_html(title: str, body_html: str, extra_css: str | None = None) -> str:
    css = BASE_STYLE + ("\n" + extra_css if extra_css else "")
    return f"""<!doctype html>
<html lang=\"pt-BR\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>{title}</title>
  <style>{css}</style>
  <meta name=\"generator\" content=\"MDD Publisher\" />
  <meta name=\"color-scheme\" content=\"light\" />
  <meta name=\"theme-color\" content=\"#2b70c9\" />
</head>
<body>
{body_html}
</body>
</html>"""


def default_output_for_md(md_path: Path, output_root: Path, new_ext: str) -> Path:
    """
    Calcula caminho de saída padrão preservando estrutura de diretórios.

    Se o arquivo de entrada está em project/docs/, replica a hierarquia
    em output_root. Caso contrário, usa apenas o nome do arquivo.
    """
    # Tenta importar config para usar caminhos centralizados
    try:
        from pathlib import Path as P
        script_dir = P(__file__).parent.parent
        sys.path.insert(0, str(script_dir))
        from config import DOCS_DIR
        rel = md_path.relative_to(DOCS_DIR)
        return output_root / rel.with_suffix(new_ext)
    except Exception:
        # Fallback: tenta path relativo genérico
        try:
            rel = md_path.relative_to(Path("project/docs"))
            return output_root / rel.with_suffix(new_ext)
        except Exception:
            return output_root / md_path.with_suffix(new_ext).name
