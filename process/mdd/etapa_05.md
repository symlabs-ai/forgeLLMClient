# 🧩 Etapa 5 — Avaliação e Retroalimentação Estratégica (atualizada com interação dos stakeholders)

## 🎯 Propósito

A Etapa 5 é o fechamento simbiótico do ciclo do **Market Driven Development (MDD)**.
Ela tem como objetivo **avaliar o desempenho real do produto no mercado**, analisando os dados obtidos na Etapa 4 e promovendo uma **interpretação colaborativa com os stakeholders (usuários, decisores e criadores)**.

O papel do **MDD Coach** é atuar como **facilitador e analista estratégico** — ele organiza os resultados, apresenta os dados de forma compreensível e provoca a reflexão coletiva que levará à decisão final do ciclo.
A decisão, portanto, **pertence ao stakeholder**: continuar, revisar ou encerrar o projeto.

> **Pergunta norteadora:**
> **“O que o mercado nos ensinou — e o que decidimos fazer com esse aprendizado?”**

---

## ⚙️ Entradas e Saídas

| Tipo         | Artefato                                                                                                             | Descrição                                                                     |
| ------------ | -------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| **Entradas** | `project/output/sites/site_01–03/`, `project/data/validacao/`                                                        | Dados de interação e engajamento coletados das páginas de validação (A/B/C).  |
| **Saídas**   | `docs/resultados_validacao.md`, `docs/revisao_estrategica.md`, `docs/aprovacao_mvp.md` ou `docs/rejeicao_projeto.md` | Relatórios de análise, interpretação coletiva e decisão final do stakeholder. |

📁 **Templates:**

* `process/templates/template_resultados_validacao.md`
* `process/templates/template_revisao_estrategica.md`
* `process/templates/template_aprovacao_mvp.md`
* `process/templates/template_rejeicao_projeto.md`

---

## 🧱 Estrutura Operacional

A avaliação ocorre em **três fases interligadas**, conduzidas pelo MDD Coach com participação ativa dos stakeholders.

### 1. Coleta e Consolidação de Dados

O **MDD Publisher** (ou módulo analítico) compila as métricas da Etapa 4 em `project/data/validacao/`, incluindo:

* Visualizações, cliques e conversões;
* Tempo médio de leitura;
* Engajamento por versão (A/B/C).

O **MDD Coach** prepara uma síntese inicial com gráficos e indicadores simples, tornando os dados compreensíveis para os stakeholders.

### 2. Apresentação e Interpretação Colaborativa

O **MDD Coach** organiza uma sessão de análise com os stakeholders.
Durante essa sessão:

* Apresenta os resultados e insights do `resultados_validacao.md`;
* Faz perguntas provocativas para estimular a reflexão:

  > “Qual dessas versões representou melhor a essência do produto?”
  > “Há sinais de interesse real ou apenas curiosidade superficial?”
  > “Esses resultados refletem o que esperávamos ouvir do mercado?”
* Registra as percepções e sugestões dos stakeholders no próprio `resultados_validacao.md`, em uma seção chamada **Feedback Coletivo**.

### 3. Decisão Final

A decisão **não é do MDD Coach**, mas dos stakeholders.
Após a análise colaborativa, o grupo define um dos caminhos:

* **Revisão Estratégica:** ajustes no posicionamento, mensagem ou produto.
* **Aprovação de MVP:** a proposta está validada e pode avançar para o desenvolvimento.
* **Encerramento:** a hipótese é encerrada, mas o aprendizado é documentado.

O MDD Coach registra essa decisão no artefato correspondente e fecha o ciclo.

---

## 🧩 Estrutura do Documento de Avaliação

```markdown
# 📊 Resultados da Validação de Mercado

## 🎯 Visão Geral
Resumo dos testes realizados e do propósito da validação.

## 📈 Principais Métricas
| Indicador | Versão A | Versão B | Versão C |
|------------|-----------|-----------|-----------|
| Visualizações | [valor] | [valor] | [valor] |
| Cliques no CTA | [valor] | [valor] | [valor] |
| Conversões | [valor] | [valor] | [valor] |

## 🧠 Interpretação Inicial do MDD Coach
Análise qualitativa dos resultados, identificando o que funcionou e o que precisa de ajuste.

> “Os usuários responderam melhor a mensagens que enfatizam autonomia e velocidade.”

## 💬 Feedback dos Stakeholders
Síntese das percepções e sugestões dos participantes após a apresentação dos dados.

> “A versão B é mais clara, mas a versão C gera mais engajamento emocional.”

## 🧭 Decisão Final
Registro da decisão consensual:
- Revisar, avançar ou encerrar o projeto.
- Motivos e próximos passos definidos pelos stakeholders.

---

*Documento gerado pelo MDD Coach em colaboração com stakeholders a partir dos dados de validação simbiótica.*
```

---

## 🔍 Critérios de Qualidade

A avaliação deve:

* Ser **colaborativa** — incluir as interpretações dos stakeholders;
* Ser **explicável** — apresentar dados de forma acessível e contextualizada;
* Ser **decisiva** — culminar em uma decisão clara e registrada;
* Alimentar o próximo ciclo MDD com base em aprendizado compartilhado.

---

## 🤖 Papéis dos Symbiotas

| Symbiota          | Função                     | Ação                                                                                         |
| ----------------- | -------------------------- | -------------------------------------------------------------------------------------------- |
| **MDD Coach**     | Facilitador e Mediador     | Apresenta os dados, conduz a interpretação coletiva e registra as decisões dos stakeholders. |
| **MDD Publisher** | Coletor e Analista Técnico | Consolida as métricas, prepara gráficos e relatórios quantitativos.                          |

---

## 🔁 Fluxo Simbiótico Simplificado

1. O MDD Publisher coleta e organiza as métricas da Etapa 4.
2. O MDD Coach analisa os dados e apresenta os resultados aos stakeholders.
3. O grupo discute e fornece feedback coletivo.
4. Os stakeholders decidem: **revisar, aprovar ou encerrar**.
5. O MDD Coach registra a decisão no artefato correspondente e inicia a retroalimentação do processo.

---

## ✅ Resultado Esperado

O projeto deve conter:

* `project/docs/resultados_validacao.md` → análise simbiótica e registro das percepções coletivas.
* `project/docs/revisao_estrategica.md`, `aprovacao_mvp.md` ou `rejeicao_projeto.md` → decisão final validada pelos stakeholders.
* `project/data/validacao/` → base de métricas consolidadas.

Esses artefatos encerram o ciclo atual e **reabrem o aprendizado** com base em dados reais e feedback humano.
