# 🧩 Etapa 2 — Síntese Executiva

## 🎯 Propósito

A Etapa 2 do Market Driven Development (MDD) transforma a **visão** formulada na etapa anterior em um **documento executivo conciso e estratégico**, capaz de orientar decisões e comunicar o valor do produto a stakeholders, diretores e investidores potenciais.

O objetivo é traduzir a visão conceitual em um **plano de entendimento de mercado e negócio**, mantendo o foco na clareza e na testabilidade.

> **Pergunta norteadora:**
> **"Como comunicamos esta visão de forma que qualquer tomador de decisão entenda o seu valor e propósito?"**

---

## ⚙️ Entradas e Saídas

| Tipo        | Artefato                    | Descrição                                                                                                                                                                                                                                         |
| ----------- | --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Entrada** | `docs/visao.md`             | Documento de visão desenvolvido na Etapa 1.                                                                                                                                                                                                       |
| **Saída**   | `docs/sumario_executivo.md` | Documento estratégico que estrutura a visão em formato executivo. É salvo em `project/docs/sumario_executivo.md`. Após validação, o **MDD Publisher** gera automaticamente versões publicáveis em PDF e HTML no diretório `project/output/docs/`. |

📁 **Template:** `process/templates/template_sumario_executivo.md`

---

## 🧱 Estrutura Operacional

A síntese executiva é construída a partir do **MDD Coach**, que atua como **editor estratégico** — guiando o humano na estruturação de um resumo que una propósito, valor e viabilidade.
Após a redação e validação do arquivo, o **MDD Publisher** entra em ação para criar as versões publicáveis (PDF e HTML).

### 1. Revisão da Visão

O MDD Coach lê o conteúdo de `docs/visao.md` e confirma com o stakeholder se a visão está consolidada.
Perguntas de alinhamento ajudam a garantir consistência e clareza:

* “A visão reflete o propósito real do produto?”
* “Os elementos de valor e mercado estão explícitos e objetivos?”

### 2. Conversa de Estruturação

O MDD Coach conduz o stakeholder em uma entrevista de estruturação para preencher os blocos do sumário executivo:

* “Qual é o contexto e a oportunidade deste produto?”
* “Qual é o problema central e qual a solução proposta?”
* “Qual é o modelo de negócio pretendido?”
* “Quais os riscos e como serão mitigados?”

### 3. Redação e Montagem do Documento

Com base nas respostas, o MDD Coach redige o `docs/sumario_executivo.md` segundo o modelo do template.

O arquivo é salvo em `project/docs/` e validado com o stakeholder antes da publicação.

---

## 🧩 Ação do MDD Publisher

Após a validação do `sumario_executivo.md`, o **MDD Publisher** executa o seguinte fluxo:

1. Detecta o novo arquivo em `project/docs/`.
2. Identifica o tipo de documento e o template visual adequado (`process/templates/style_pdf.json` ou `style_html.json`).
3. Executa os scripts de conversão localizados em `symbiotas/mdd_publisher/scripts/`:

   * `export_pdf.py` → gera `project/output/docs/sumario_executivo.pdf`
   * `export_html.py` → gera `project/output/docs/sumario_executivo.html`
4. Registra o evento no log `project/output/logs/export_history.log`.

---

## 🔍 Critérios de Qualidade

O sumário executivo deve:

* Comunicar o essencial do produto em **até 3 páginas**;
* Focar na **compreensão do valor**, não em jargões técnicos;
* Manter consistência entre visão e estratégia;
* Estar disponível em versões **Markdown (fonte)**, **PDF (formal)** e **HTML (web)**.

---

## 🤖 Papéis dos Symbiotas

| Symbiota          | Função             | Ação                                                                |
| ----------------- | ------------------ | ------------------------------------------------------------------- |
| **MDD Coach**     | Editor Estratégico | Conduz o diálogo, redige e valida o `sumario_executivo.md`.         |
| **MDD Publisher** | Publicador Visual  | Converte o documento em PDF e HTML, aplica estilos e registra logs. |

---

## 🔁 Fluxo Simbiótico Simplificado

1. O MDD Coach cria e valida o `project/docs/sumario_executivo.md` usando o template.
2. O MDD Publisher detecta o arquivo finalizado e gera automaticamente as versões publicáveis (`project/output/docs/sumario_executivo.pdf` e `.html`).
3. Ambos registram logs de execução e revisão.

---

## ✅ Resultado Esperado

O projeto deve conter:

* `project/docs/sumario_executivo.md` → versão simbiótica textual;
* `project/output/docs/sumario_executivo.pdf` → versão formal executiva;
* `project/output/docs/sumario_executivo.html` → versão web interativa.

Esses arquivos consolidam a transição entre a visão e o plano estratégico, servindo como base para a construção do `docs/pitch_deck.md` e as próximas etapas do MDD.

---

> **Resumo:** A Etapa 2 conclui o ciclo estratégico inicial. Após a escrita pelo MDD Coach, o MDD Publisher gera versões formais e web, garantindo que o conhecimento simbiótico se torne comunicação tangível e compartilhável.
