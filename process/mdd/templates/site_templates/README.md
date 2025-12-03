# Templates de Sites para Validação A/B/C

Este diretório contém os templates HTML/CSS usados para gerar as landing pages de validação de mercado (Etapa 4 do MDD).

## Estrutura

Cada template está em seu próprio diretório:

```
site_templates/
├── template_01/
├── template_02/
└── template_03/
```

Cada diretório contém:
- `index.html` — Estrutura HTML base com placeholders `{{variavel}}`
- `style.css` — Estilos visuais (responsivos)
- `config.json` — Metadados, incluindo `variaveis_obrigatorias`

## Placeholders e Variáveis

Use placeholders `{{nome_da_variavel}}` no HTML. Os valores vêm de:
- Front matter YAML do `.md` (prioridade alta)
- Conteúdo do `.md` (títulos/seções inferidas)
- `extra_vars` passadas pelo script

Em modo `--strict`, o Publisher valida as `variaveis_obrigatorias` do `config.json` do template antes de renderizar.

## Uso

Renderize via:
```
python symbiotas/mdd_publisher/scripts/export_site_html.py \
  --input-dir project/docs/sites \
  --output-dir project/output/sites \
  --templates-dir process/templates/site_templates \
  [--strict]
```

Os arquivos esperados são `site_A.md`, `site_B.md`, `site_C.md` e mapeiam para `template_01`, `template_02`, `template_03` respectivamente.
