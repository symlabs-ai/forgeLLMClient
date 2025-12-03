# MDD Publisher — Scripts de Exportação

Este diretório contém os scripts que convertem artefatos Markdown (`project/docs/*.md`) em formatos publicáveis (HTML, PDF, DOCX) e geram sites A/B/C.

- Logs: `project/output/logs/export_history.log`
- Saídas: `project/output/docs/` e `project/output/sites/`
- Templates (quando aplicável): `process/templates/`

---

## Requisitos

- Python 3.10+
- Opcional (melhor qualidade/formatos):
  - `markdown` (melhor conversão MD→HTML; sem ele há fallback simples)
  - `weasyprint` ou `pdfkit` + `wkhtmltopdf` (para PDF)
  - `python-docx` (para DOCX)

Dica (ambiente virtual):

```
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows (PowerShell/CMD)

pip install markdown weasyprint pdfkit python-docx
# Se usar pdfkit, instale o wkhtmltopdf no sistema
```

---

## Uso Rápido

HTML (genérico):
```
python symbiotas/mdd_publisher/scripts/export_html.py \
  --input project/docs/sumario_executivo.md
```
Saída padrão: `project/output/docs/sumario_executivo.html`

PDF:
```
python symbiotas/mdd_publisher/scripts/export_pdf.py \
  --input project/docs/sumario_executivo.md
```
- Tenta `weasyprint`; se indisponível, tenta `pdfkit`; se nenhuma disponível, falha com mensagem.
- Saída: `project/output/docs/sumario_executivo.pdf`

DOCX:
```
python symbiotas/mdd_publisher/scripts/export_docx.py \
  --input project/docs/sumario_executivo.md
```
- Requer `python-docx`.
- Saída: `project/output/docs/sumario_executivo.docx`

Pitch (HTML):
```
python symbiotas/mdd_publisher/scripts/export_pitch_html.py \
  --input project/docs/pitch_deck.md
```
- Saída: `project/output/docs/pitch_deck.html`

Sites A/B/C (HTML):
```
python symbiotas/mdd_publisher/scripts/export_site_html.py
```
- Espera por: `project/docs/sites/site_A.md`, `site_B.md`, `site_C.md`
- Gera: `project/output/sites/site_01/index.html`, `site_02/index.html`, `site_03/index.html`

---

## Comportamento Padrão

- Se `--output` não for informado (quando disponível), o caminho é inferido sob `project/output/` replicando a estrutura de `project/docs/` e trocando a extensão.
- Todos os scripts registram eventos de exportação em `project/output/logs/export_history.log`.
- A conversão MD→HTML usa o pacote `markdown`, quando disponível; caso contrário, aplica um fallback básico (títulos, parágrafos, bloco de código, citação e `hr`).

---

## Solução de Problemas

- PDF falha informando ausência de backend: instale `weasyprint` ou `pdfkit` e `wkhtmltopdf` (binário do sistema).
- DOCX falha informando ausência de pacote: instale `python-docx`.
- Resultado HTML simples demais: instale `markdown` para uma melhor conversão.

---

## Exemplo End‑to‑End

1) Crie/edite `project/docs/sumario_executivo.md`.
2) Exporte HTML e PDF:
```
python symbiotas/mdd_publisher/scripts/export_html.py --input project/docs/sumario_executivo.md
python symbiotas/mdd_publisher/scripts/export_pdf.py  --input project/docs/sumario_executivo.md
```
3) Verifique saídas em `project/output/docs/` e o log em `project/output/logs/export_history.log`.
