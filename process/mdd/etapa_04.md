# 🧩 Etapa 4 — Validação Pública Inicial (atualizada com caminho de templates definitivo)

## 🎯 Propósito

A Etapa 4 do **Market Driven Development (MDD)** é o momento em que o produto **sai do plano estratégico e começa a dialogar com o mercado real**.
O objetivo é **testar hipóteses de valor e narrativa** por meio de páginas experimentais (sites A/B/C), que traduzem a essência do produto em comunicação clara, atrativa e mensurável.

Essas páginas são concebidas como **documentos Markdown ricos e semânticos**, redigidos pelo **MDD Coach** e renderizados em HTML interativo pelo **MDD Publisher**.
Elas seguem uma estrutura narrativa modular, inspirada em sites de storytelling visual (como os do Gamma).

> **Pergunta norteadora:**
> **“Como o mercado reage quando nossa proposta é contada de forma clara, emocional e visual?”**

---

## ⚙️ Entradas e Saídas

| Tipo         | Artefato                                                               | Descrição                                                                                                                                                                                   |
| ------------ | ---------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Entradas** | `docs/visao.md`, `docs/sumario_executivo.md`, `docs/pitch_deck.md`     | Fornecem o conteúdo base (propósito, valor e diferenciais) para compor as narrativas públicas.                                                                                              |
| **Saídas**   | `docs/sites/site_A.md`, `docs/sites/site_B.md`, `docs/sites/site_C.md` | Três variações narrativas da proposta de valor (emocional, funcional, social). |
| **Saídas (HTML)** | `output/docs/sites/site_A.html`, `.../site_B.html`, `.../site_C.html` | Renderizações HTML geradas automaticamente pelo **MDD Publisher** a partir dos `.md` (opcionais, não bloqueiam o fluxo). |
| **Entregas** | `docs/sites/site_A_gamma_prompt.md` (e B/C)                             | Prompt texto para Gamma.app gerar a landing (sem tags XML/HTML; sem inventar números/conteúdos além do script). |

📁 **Templates:**

* Estrutura textual: `process/templates/template_site.md`
* Templates visuais definitivos: `process/templates/site_templates/template_01`, `process/templates/site_templates/template_02`, `process/templates/site_templates/template_03`

---

## 🧱 Estrutura Narrativa (modelo simbiótico)

Cada arquivo `.md` segue um padrão modular e visual, projetado para ser interpretado pelo Publisher como blocos interativos no HTML.
Esse formato torna a renderização automática possível sem perda de expressividade.

```markdown
# 🧠 [Título do Site / Proposta]
_Apresentação visual curta (equivalente à Hero Section)_

> Frase de impacto ou tagline que resume a promessa de valor.

---

## 🎯 Contexto / Problema
Explique o cenário, a dor e a oportunidade que originam o produto.
Use **negrito** para pontos críticos e *itálico* para nuances.

- Situação de mercado atual.
- Falhas ou ineficiências existentes.
- Consequências para o público.

---

## 💡 Solução / Proposta
Apresente a ideia central e a transformação que o produto oferece.

> “Nossa solução transforma X em Y, de forma simples e eficiente.”

- Elemento 1 da proposta.
- Elemento 2 da proposta.
- Elemento 3 da proposta.

---

## ⚙️ Como Funciona
Descreva visualmente a arquitetura ou os estágios do processo.

| Etapa | Descrição |
|-------|------------|
| Input | Onde o problema começa. |
| Engine | Onde a inteligência opera. |
| Output | Onde o valor é entregue. |

---

## 🌟 Benefícios e Diferenciais
Mostre os ganhos concretos da solução.

✅ Reduz custos operacionais.
🚀 Aumenta a produtividade.
🔒 Garante segurança e compliance.

---

## 🧭 Casos de Uso
Apresente exemplos reais ou hipotéticos que demonstram valor.

**Exemplo 1:** [descrição breve].
**Exemplo 2:** [descrição breve].
**Exemplo 3:** [descrição breve].

---

## 🗺️ Roadmap e Próximos Passos
Mostre maturidade e planejamento.

1. **MVP:** protótipo funcional validado.
2. **Beta:** abertura controlada para early adopters.
3. **Lançamento:** disponibilização pública.

---

## 📩 Chamada à Ação
> Quer testar ou saber mais?
> [Clique aqui](#) e participe do início dessa jornada.

---

## 📎 Rodapé / Créditos
_Autores, datas, contatos e fontes de referência._
```

Essa estrutura se traduz automaticamente em seções HTML distintas, que o Publisher converte em blocos visuais — hero, cards, colunas, timeline e CTA.

---

## 🧩 Ação do MDD Publisher

Após o MDD Coach concluir as três versões (`site_A.md`, `site_B.md`, `site_C.md`), o **MDD Publisher** executa o seguinte pipeline:

1. Detecta os arquivos em `project/docs/sites/`.
2. Associa cada arquivo a um template visual correspondente (`process/templates/site_templates/template_01`, `template_02`, `template_03`).
3. Executa o script `export_site_html.py` em `symbiotas/mdd_publisher/scripts/`.
4. Converte os `.md` em HTML completos, armazenando-os em:

   * `project/output/sites/site_01/`
   * `project/output/sites/site_02/`
   * `project/output/sites/site_03/`
   * (equivalente a outputs opcionais `project/output/docs/sites/site_A.html`, `.../site_B.html`, `.../site_C.html`)
5. Gera também prompts Gamma por variação: `project/docs/sites/site_A_gamma_prompt.md` (e B/C), incluindo:
   - Proibição de tags XML/HTML no prompt (ex.: sem <title>, <h1>, etc.);
   - Uso estrito do conteúdo do `.md` correspondente (sem inventar números, métricas, depoimentos ou seções extra);
   - Listagem dos quadros/seções com textos exatos.
6. Registra os eventos em `project/output/logs/export_history.log`.

Cada site é publicado com design responsivo, CTAs ativos e rastreamento de métricas (cliques, tempo de leitura, conversão).

---

## 🔍 Critérios de Qualidade

Um bom site de validação deve:

* Ter **impacto visual imediato** (frase de efeito + layout limpo).
* Ser **curto e navegável** (tempo de leitura ideal: 2–3 minutos).
* Destacar **uma proposta de valor por versão (A/B/C)**.
* Incluir **CTA rastreável e claro**.
* Refletir a **voz e o propósito** definidos na visão e no sumário executivo.

---

## 🤖 Papéis dos Symbiotas

| Symbiota          | Função            | Ação                                                                           |
| ----------------- | ----------------- | ------------------------------------------------------------------------------ |
| **MDD Coach**     | Criador Narrativo | Redige e organiza as versões A/B/C com base na estrutura narrativa simbiótica. |
| **MDD Publisher** | Publicador Visual | Converte os `.md` em experiências web, aplica templates e registra logs.       |

---

## 🔁 Fluxo Simbiótico Simplificado

1. O MDD Coach cria três narrativas (`site_A.md`, `site_B.md`, `site_C.md`) baseadas na visão, sumário e pitch.
2. O MDD Publisher converte cada arquivo usando os templates visuais numerados (`template_01`, `template_02`, `template_03`).
3. As versões finais são publicadas em `project/output/sites/site_01–03/`.
4. As métricas coletadas alimentam a análise da Etapa 5.

---

## ✅ Resultado Esperado

O projeto deve conter:

* `project/docs/sites/site_A.md` → narrativa de valor (benefício emocional).
* `project/output/docs/sites/site_A.html` → versão HTML opcional (gerada pelo Publisher).
* `project/docs/sites/site_B.md` → narrativa de valor (benefício funcional).
* `project/output/docs/sites/site_B.html` → versão HTML opcional (gerada pelo Publisher).
* `project/docs/sites/site_C.md` → narrativa de valor (benefício social).
* `project/output/docs/sites/site_C.html` → versão HTML opcional (gerada pelo Publisher).
* `project/output/sites/site_01–03/` → versões HTML publicadas e rastreáveis.

Essas páginas representam o **primeiro contato real entre o produto e o mercado**, permitindo validar se a mensagem desperta atenção, confiança e engajamento.
