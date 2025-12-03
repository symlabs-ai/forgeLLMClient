# 🧩 Etapa 3 — Pitch de Valor (atualizada)

## 🎯 Propósito

A Etapa 3 do Market Driven Development (MDD) tem como objetivo **converter o conteúdo estratégico da visão e do sumário executivo em uma narrativa visual e persuasiva** — o **Pitch de Valor**.
Essa etapa transforma o raciocínio simbiótico em comunicação clara e atraente, capaz de envolver investidores, parceiros e stakeholders.

O resultado é um **documento de apresentação (.md)** renderizado em **HTML interativo** pelo MDD Publisher.

> **Pergunta norteadora:**
> **“Como contamos a história deste produto de forma que o mercado queira ouvi-la?”**

---

## ⚙️ Entradas e Saídas

| Tipo         | Artefato                                     | Descrição                                                                                                                                                                           |
| ------------ | -------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Entradas** | `docs/visao.md`, `docs/sumario_executivo.md` | Documentos base que contêm a essência da visão e o plano estratégico.                                                                                                               |
| **Saída**    | `docs/pitch_deck.md`                         | Documento que organiza o conteúdo da visão e do sumário em formato narrativo e visual. O MDD Publisher gera automaticamente a versão HTML em `project/output/docs/pitch_deck.html`. |
| **Entrega**  | `docs/pitch_deck_gamma_prompt.md`            | Prompt texto para geração de slides no Gamma.app (sem tags XML/HTML; não inventar números/seções além do script). |

📁 **Template:** `process/templates/template_pitch_deck.md`

---

## 🧱 Estrutura Operacional

Nesta etapa, o **MDD Coach** e o **MDD Publisher** trabalham de forma coordenada:

* O **MDD Coach** estrutura a narrativa textual do pitch.
* O **MDD Publisher** aplica o template visual e gera a versão HTML publicável.

### 1. Estruturação da Narrativa

O MDD Coach orienta o humano a transformar os dados estratégicos da visão e do sumário em uma **história envolvente**, com início, meio e fim.
O foco é conectar racionalidade (mercado e estratégia) com emoção (propósito e impacto).

Perguntas de apoio:

* “Como podemos apresentar essa visão como uma jornada?”
* “Qual o problema central que move esta história?”
* “O que torna esta solução inevitável agora?”
* “Como traduzir a estratégia em uma sequência visual?”

### 2. Redação do Pitch

O conteúdo do `pitch_deck.md` é estruturado em blocos narrativos:

```markdown
# Pitch de Valor — [Nome do Produto]

## Bloco 1 — Propósito
[Apresente o propósito e o problema que o produto resolve.]

## Bloco 2 — Oportunidade de Mercado
[Destaque a dimensão e urgência da oportunidade.]

## Bloco 3 — Solução e Diferencial
[Explique como o produto resolve o problema de forma única.]

## Bloco 4 — Modelo de Negócio
[Mostre como o valor é capturado e sustentado.]

## Bloco 5 — Roadmap e Validação
[Descreva próximos passos e evidências de tração.]

## Bloco 6 — Encerramento
[Mensagem final e chamada à ação.]

---

*Documento gerado pelo symbiota MDD Coach a partir de `docs/visao.md` e `docs/sumario_executivo.md`.*
```

---

### 3. Renderização do Pitch

Após a validação do documento pelo MDD Coach, o **MDD Publisher** entra em ação:

1. Detecta o arquivo `project/docs/pitch_deck.md`.
2. Identifica o tipo de documento e aplica o template `process/templates/style_pitch.json` e `style_pitch.css`.
3. Executa o script `export_pitch_html.py` localizado em `symbiotas/mdd_publisher/scripts/`.
4. Gera a saída `project/output/docs/pitch_deck.html`.
5. Gera também `project/docs/pitch_deck_gamma_prompt.md` com instruções para o Gamma.app:
   - Não usar tags XML/HTML no prompt (ex.: sem <title>, <h1>, etc.);
   - Usar apenas o conteúdo do `pitch_deck.md` (sem inventar números, nomes de terceiros ou seções não previstas);
   - Listar a estrutura de slides (títulos e bullets) mantendo a ordem do script.
6. Registra o evento no log `project/output/logs/export_history.log`.

> 🔧 O MDD Publisher possui **scripts dedicados** para cada tipo de documento (ex.: `export_sumario_pdf.py`, `export_pitch_html.py`, `export_site_html.py`), garantindo personalização e fidelidade visual a cada tipo de artefato.

---

## 🔍 Critérios de Qualidade

Um bom pitch deve:

* Ser **curto, coerente e visualmente impactante** (ideal: até 6 blocos narrativos);
* Transmitir propósito, diferenciação e valor de mercado;
* Ter design limpo e responsivo no HTML final;
* Ser **consistente** com a visão e o sumário executivo.

---

## 🤖 Papéis dos Symbiotas

| Symbiota          | Função                    | Ação                                                                                      |
| ----------------- | ------------------------- | ----------------------------------------------------------------------------------------- |
| **MDD Coach**     | Roteirista e Estrategista | Constrói a narrativa textual do `pitch_deck.md` com base na visão e no sumário executivo. |
| **MDD Publisher** | Publicador Visual         | Converte o `pitch_deck.md` em HTML, aplica estilos visuais e registra logs de exportação. |

---

## 🔁 Fluxo Simbiótico Simplificado

1. O MDD Coach importa conteúdo de `docs/visao.md` e `docs/sumario_executivo.md`.
2. Conduz a criação do `docs/pitch_deck.md` com estrutura narrativa.
3. O MDD Publisher detecta o arquivo, aplica o template e executa o script `export_pitch_html.py`.
4. O resultado é salvo em `project/output/docs/pitch_deck.html`.
5. Ambos registram logs das ações executadas.

---

## ✅ Resultado Esperado

O projeto deve conter:

* `project/docs/pitch_deck.md` → narrativa textual do pitch;
* `project/output/docs/pitch_deck.html` → versão visual web do pitch.

Esses arquivos compõem o material de **comunicação de valor** do produto, servindo como ponte entre a estratégia interna e a validação de mercado (Etapa 4).

---

> **Resumo:** A Etapa 3 é a tradução visual e emocional da estratégia. O MDD Coach estrutura o discurso; o MDD Publisher o transforma em uma experiência web — tornando o raciocínio simbiótico comunicável e interativo.
