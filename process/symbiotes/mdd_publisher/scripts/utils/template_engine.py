#!/usr/bin/env python3
"""
Motor de templates para sites A/B/C do MDD Publisher.

Permite substituição de variáveis em templates HTML usando
marcadores {{variavel}} e extração automática de metadados MD.
"""
from __future__ import annotations

import json
import re
from pathlib import Path


def extract_frontmatter(md_content: str) -> dict[str, str]:
    """
    Extrai YAML front matter de arquivo Markdown.

    Front matter esperado:
    ---
    titulo: Meu Título
    cta_texto: Clique Aqui
    ---

    Args:
        md_content: Conteúdo do arquivo Markdown

    Returns:
        Dicionário com variáveis extraídas
    """
    frontmatter_pattern = r'^---\s*\n(.*?)\n---\s*\n'
    match = re.match(frontmatter_pattern, md_content, re.DOTALL)

    if not match:
        return {}

    yaml_content = match.group(1)
    variables: dict[str, str] = {}

    # Parser YAML simples (apenas key: value)
    for line in yaml_content.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            # Remove aspas simples ou duplas ao redor do valor
            variables[key.strip()] = value.strip().strip("\"'")

    return variables


def extract_from_markdown(md_content: str) -> dict[str, str]:
    """
    Extrai variáveis automaticamente do Markdown baseado em padrões.

    Regras:
    - Primeiro # h1 vira 'titulo_principal'
    - Primeira linha de texto vira 'subtitulo'
    - Seções ## viram variáveis lowercase

    Args:
        md_content: Conteúdo Markdown

    Returns:
        Dicionário de variáveis inferidas
    """
    variables: dict[str, str] = {}
    lines = md_content.split('\n')

    # Extrai título principal (primeiro H1)
    for line in lines:
        if line.startswith('# ') and 'titulo_principal' not in variables:
            variables['titulo_principal'] = line[2:].strip()
            break

    # Extrai seções (H2+)
    current_section = None
    section_content = []

    for line in lines:
        if line.startswith('## '):
            if current_section and section_content:
                # Salva seção anterior
                section_key = current_section.lower().replace(' ', '_')
                variables[section_key] = ' '.join(section_content).strip()
            current_section = line[3:].strip()
            section_content = []
        elif current_section and line.strip() and not line.startswith('#'):
            section_content.append(line.strip())

    # Salva última seção
    if current_section and section_content:
        section_key = current_section.lower().replace(' ', '_')
        variables[section_key] = ' '.join(section_content).strip()

    return variables


def apply_template(template_path: Path, variables: dict[str, str], strict: bool = False) -> str:
    """
    Aplica variáveis a um template HTML.

    Substitui todos os marcadores {{variavel}} pelos valores fornecidos.

    Args:
        template_path: Caminho para o arquivo index.html do template
        variables: Dicionário de variáveis a substituir
        strict: Se True, lança erro se variável obrigatória ausente

    Returns:
        HTML renderizado com variáveis substituídas

    Raises:
        FileNotFoundError: Se template não existir
        ValueError: Se strict=True e variável obrigatória ausente
    """
    if not template_path.exists():
        raise FileNotFoundError(f"Template não encontrado: {template_path}")

    template_html = template_path.read_text(encoding='utf-8')

    # Encontra todas as variáveis no template
    placeholders = set(re.findall(r'\{\{(\w+)\}\}', template_html))

    if strict:
        # Verifica variáveis obrigatórias
        missing = placeholders - set(variables.keys())
        if missing:
            raise ValueError(f"Variáveis obrigatórias ausentes: {', '.join(missing)}")

    # Substitui variáveis
    for key, value in variables.items():
        template_html = template_html.replace(f'{{{{{key}}}}}', value)

    # Limpa variáveis não substituídas (opcional)
    template_html = re.sub(r'\{\{(\w+)\}\}', '', template_html)

    return template_html


def load_template_config(template_dir: Path) -> dict | None:
    """
    Carrega configuração do template (config.json).

    Args:
        template_dir: Diretório do template

    Returns:
        Dicionário de configuração ou None se não existir
    """
    config_path = template_dir / 'config.json'
    if not config_path.exists():
        return None

    try:
        return json.loads(config_path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return None


def render_site(
    md_path: Path,
    template_dir: Path,
    output_path: Path,
    extra_vars: dict[str, str] | None = None,
    strict: bool = False
) -> Path:
    """
    Renderiza um site completo a partir de MD + template.

    Processo:
    1. Lê arquivo Markdown
    2. Extrai front matter (se existir)
    3. Extrai variáveis do conteúdo MD
    4. Aplica ao template HTML
    5. Salva em output_path

    Args:
        md_path: Arquivo .md com conteúdo e variáveis
        template_dir: Diretório do template (contém index.html, style.css, config.json)
        output_path: Caminho de saída para index.html
        extra_vars: Variáveis adicionais a aplicar
        strict: Se True, valida variáveis obrigatórias

    Returns:
        Path do arquivo gerado

    Raises:
        FileNotFoundError: Se arquivos não existirem
        ValueError: Se strict=True e houver variáveis ausentes
    """
    if not md_path.exists():
        raise FileNotFoundError(f"Arquivo MD não encontrado: {md_path}")

    md_content = md_path.read_text(encoding='utf-8')

    # Extrai variáveis de múltiplas fontes
    variables: dict[str, str] = {}

    # 1. Front matter (prioridade alta)
    variables.update(extract_frontmatter(md_content))

    # 2. Conteúdo MD (prioridade média)
    variables.update(extract_from_markdown(md_content))

    # 3. Variáveis extras (prioridade máxima)
    if extra_vars:
        variables.update(extra_vars)

    # Se strict, valida variáveis obrigatórias definidas no config.json do template
    if strict:
        cfg = load_template_config(template_dir)
        required = set(cfg.get('variaveis_obrigatorias', [])) if cfg else set()
        if required:
            missing = required - set(variables.keys())
            if missing:
                raise ValueError(f"Variáveis obrigatórias ausentes (config.json): {', '.join(sorted(missing))}")

    # Renderiza template
    template_html_path = template_dir / 'index.html'
    rendered_html = apply_template(template_html_path, variables, strict=strict)

    # Salva output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(rendered_html, encoding='utf-8')

    # Copia CSS se existir
    css_source = template_dir / 'style.css'
    if css_source.exists():
        css_dest = output_path.parent / 'style.css'
        css_dest.write_text(css_source.read_text(encoding='utf-8'), encoding='utf-8')

    return output_path
