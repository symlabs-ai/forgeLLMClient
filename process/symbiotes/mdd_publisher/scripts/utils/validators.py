#!/usr/bin/env python3
"""
Validação de schemas para artefatos MDD.

Este módulo verifica se os arquivos Markdown seguem a estrutura esperada
para cada tipo de artefato do processo MDD, prevenindo erros na exportação.
"""
from __future__ import annotations

import re
from pathlib import Path

# Schemas de validação: seções obrigatórias por tipo de artefato
REQUIRED_SECTIONS: dict[str, list[str]] = {
    'hipotese.md': [
        r'^#\s+Hip[óo]tese',
        r'^##\s+Problema',
        r'^##\s+Solu[çc][ãa]o\s+Proposta',
    ],
    'visao.md': [
        r'^#\s+Vis[ãa]o',
        r'^##\s+Problema',
        r'^##\s+Solu[çc][ãa]o',
        r'^##\s+M[ée]trica',
    ],
    'sumario_executivo.md': [
        r'^#\s+Sum[áa]rio\s+Executivo',
        r'^##\s+Oportunidade',
        r'^##\s+Mercado',
    ],
    'pitch_deck.md': [
        r'^#\s+Pitch',
        r'^##\s+Problema',
        r'^##\s+Solu[çc][ãa]o',
    ],
    'resultados_validacao.md': [
        r'^#\s+Resultados',
        r'^##\s+M[ée]tricas',
    ],
}


class ValidationError(Exception):
    """Erro quando um artefato não passa na validação de schema."""
    pass


def validate_artifact(md_path: Path, strict: bool = False) -> list[str]:
    """
    Valida se um artefato Markdown segue o schema esperado.

    Args:
        md_path: Caminho do arquivo .md a validar
        strict: Se True, lança exceção em vez de retornar lista de erros

    Returns:
        Lista de mensagens de erro (vazia se válido)

    Raises:
        ValidationError: Se strict=True e houver erros
        FileNotFoundError: Se o arquivo não existir
    """
    if not md_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {md_path}")

    text = md_path.read_text(encoding='utf-8')
    errors: list[str] = []

    # Obtém schema esperado para este tipo de arquivo
    required_patterns = REQUIRED_SECTIONS.get(md_path.name, [])

    if not required_patterns:
        # Arquivo não tem schema definido (não é erro, apenas aviso)
        return []

    # Verifica cada seção obrigatória
    for pattern in required_patterns:
        if not re.search(pattern, text, re.MULTILINE | re.IGNORECASE):
            # Extrai descrição legível do padrão
            section_name = pattern.replace(r'^#\s+', '').replace(r'^##\s+', '').replace(r'\s+', ' ')
            section_name = re.sub(r'\[.*?\]', '', section_name)  # Remove regex classes
            errors.append(f"Seção obrigatória ausente: {section_name}")

    if strict and errors:
        raise ValidationError(f"Validação falhou para {md_path.name}: {'; '.join(errors)}")

    return errors


def validate_all_artifacts(docs_dir: Path, strict: bool = False) -> dict[str, list[str]]:
    """
    Valida todos os artefatos em um diretório.

    Args:
        docs_dir: Diretório contendo os arquivos .md
        strict: Se True, para na primeira falha

    Returns:
        Dicionário {nome_arquivo: [erros]}
    """
    results: dict[str, list[str]] = {}

    for md_file in docs_dir.glob('*.md'):
        if md_file.name in REQUIRED_SECTIONS:
            errors = validate_artifact(md_file, strict=strict)
            if errors:
                results[md_file.name] = errors

    return results


def get_schema_info(artifact_name: str) -> str:
    """
    Retorna informação sobre o schema esperado para um artefato.

    Args:
        artifact_name: Nome do arquivo (ex: 'visao.md')

    Returns:
        String descritiva do schema esperado
    """
    patterns = REQUIRED_SECTIONS.get(artifact_name, [])
    if not patterns:
        return f"Nenhum schema definido para '{artifact_name}'"

    sections = []
    for pattern in patterns:
        # Converte regex para descrição legível
        clean = pattern.replace(r'^#\s+', '# ').replace(r'^##\s+', '## ')
        clean = re.sub(r'\[.*?\]', lambda m: m.group(0)[1], clean)
        sections.append(clean)

    return f"Schema esperado para '{artifact_name}':\n" + "\n".join(f"  - {s}" for s in sections)


if __name__ == "__main__":
    # Exemplo de uso standalone
    import sys
    from pathlib import Path

    if len(sys.argv) < 2:
        print("Uso: python validators.py <caminho_para_artefato.md>")
        sys.exit(1)

    md_path = Path(sys.argv[1])
    try:
        errors = validate_artifact(md_path, strict=False)
        if errors:
            print(f"❌ Validação falhou para {md_path.name}:")
            for error in errors:
                print(f"  - {error}")
            sys.exit(1)
        else:
            print(f"✅ {md_path.name} válido!")
            sys.exit(0)
    except FileNotFoundError as e:
        print(f"❌ Erro: {e}")
        sys.exit(2)
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        sys.exit(3)
