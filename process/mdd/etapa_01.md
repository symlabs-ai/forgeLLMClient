# 🧩 Etapa 1 — Concepção da Visão (versão atualizada)

## 🎯 Propósito

A primeira etapa do Market Driven Development (MDD) transforma uma **hipótese bruta de mercado**, registrada pelo stakeholder, em uma **visão clara, inspiradora e validável**. É aqui que o produto começa a ganhar forma — não como código, mas como propósito.

O objetivo é responder à pergunta:

> **"O que o mercado está pedindo, e como podemos expressar isso em uma visão de produto?"**

---

## ⚙️ Entradas e Saídas

| Tipo        | Artefato         | Descrição                                                                                                                                                                   |
| ----------- | ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Entrada** | `hipotese.md` | Documento com a hipótese inicial de mercado. Se o arquivo não existir, o Symbiota solicitará que o stakeholder registre uma nova hipótese em `project/docs/hipotese.md`. |
| **Saída**   | `visao.md`    | Documento de visão (Visão Canvas), contendo a proposta de valor e a direção estratégica inicial em `project/docs/visao.md`.                                                                            |

Os templates de cada documento estão disponíveis em:

```
process/templates/
├── template_hipotese.md
├── template_visao.md
```

---

## 🧱 Estrutura Operacional

A visão é construída por meio de um **processo dialógico** entre o humano e o symbiota `MDD Coach` (`/symbiotas/mdd_coach/prompt.md`).

### 1. Diálogo com o Stakeholder — *O ciclo de perguntas do MDD Coach*

O `MDD Coach` conduz o processo de descoberta, guiando o stakeholder por meio de perguntas abertas e provocativas que ajudam a lapidar a hipótese e transformá-la em visão.

| Rodada                       | Foco                                 | Perguntas típicas                                                                   |
| ---------------------------- | ------------------------------------ | ----------------------------------------------------------------------------------- |
| **1. Propósito**             | Entender o porquê da hipótese.       | “Por que essa ideia é importante agora?” / “Que mudança você gostaria de provocar?” |
| **2. Dor e Oportunidade**    | Identificar o problema central.      | “Quem sofre com isso?” / “O que as pessoas estão tentando fazer e não conseguem?”   |
| **3. Público e Contexto**    | Delimitar quem é o mercado inicial.  | “Quem seria o primeiro a se interessar?” / “Em que situação essa dor aparece?”      |
| **4. Valor e Diferenciação** | Explorar o diferencial e a promessa. | “Por que alguém escolheria sua solução?” / “Qual é a transformação que ela gera?”   |
| **5. Validação e Métrica**   | Antever sinais de tração.            | “Como saberemos se essa visão está sendo confirmada pelo mercado?”                  |

Cada sessão de diálogo é registrada em `/project/docs/sessions/mdd_coach/YYYY-MM-DD.md`, capturando perguntas, respostas e sínteses parciais.

---

## 🧩 Formalização da Visão

Após o diálogo, o próprio **MDD Coach** é responsável por **redigir e entregar o arquivo final `visao.md`** dentro de `project/docs/`.
O conteúdo segue o formato do **Visão Canvas**, conforme o template em `process/templates/template_visao.md`:

```markdown
# visão.md

## 1. Nome e Identidade
Nome inicial do produto e uma frase que capture seu espírito.

## 2. Proposta de Valor Central
Qual transformação o produto busca gerar no mercado?

## 3. Problema de Mercado
Que dor, vazio ou fricção deu origem a esta ideia?

## 4. Solução Intencionada
Como o produto resolve ou preenche esse vazio?

## 5. Público-Alvo Principal
Quem é o grupo mais diretamente beneficiado?

## 6. Potência de Mercado (Market Pulse)
Dimensão e urgência da oportunidade percebida.

## 7. Diferencial Estratégico
Por que essa solução é única ou difícil de replicar?

## 8. Métrica de Validação
Como saberei que a visão está no caminho certo?

## 9. Horizonte e Ambição
O que o produto pode se tornar se tiver êxito?

## 10. Palavras-Chave e Conceitos
Lista de conceitos-âncora que definem o tom e a identidade do produto.
```

---

## 🔍 Critérios de Qualidade

Uma visão bem formulada deve:

* Ser compreensível em até **2 minutos de leitura**;
* Comunicar **propósito e direção**, não detalhes operacionais;
* Conter **métricas claras de validação**;
* Ser **inspiradora e pragmática**, equilibrando intuição e mercado.

---

## 🤖 Papel do Symbiota

Nesta etapa, há **apenas um symbiota**: o **`MDD Coach`**.
Ele desempenha as funções de:

* Guiar o diálogo com o stakeholder;
* Sintetizar as respostas em uma proposta coerente;
* Redigir e salvar o `visao.md`;
* Assegurar que o documento final siga o template e esteja armazenado corretamente em `project/docs/`.

#### 🔁 Fluxo simbiótico simplificado:
```
1. **Verificação de hipótese:**

   * O MDD Coach verifica se existe o arquivo `project/docs/hipotese.md`.
   * Caso não exista, ele solicita ao stakeholder que registre sua hipótese inicial e cria o arquivo conforme o modelo padrão.

2. **Diálogo guiado:**

   * O MDD Coach conduz uma conversa estruturada com o stakeholder, fazendo perguntas para compreender propósito, problema, público e valor.
   * As respostas são registradas em uma sessão dentro de `symbiotas/mdd_coach/sessions/`.

3. **Síntese da visão:**

   * Com base no diálogo, o MDD Coach elabora o documento `project/docs/visao.md` utilizando o template de visão disponível em `process/templates/template_visao.md`.

4. **Revisão e comentários:**

   * O MDD Coach revisa a consistência e completude da visão criada, identificando lacunas e sugerindo melhorias.

5. **Encerramento da etapa:**

   * O documento `visao.md` torna-se o artefato final da Etapa 1 e serve como entrada para a Etapa 2 (Síntese Executiva).
```

## ✅ Resultado Esperado

Ao final desta etapa, deve existir um arquivo `visao.md` que:

* Expresse **o propósito essencial do produto**;
* Traduza **a hipótese em uma visão estruturada**;
* Seja **resultado direto da interação humano–symbiota**;
* Sirva como **entrada oficial** para a Etapa 2 (Síntese Executiva).

---

> **Resumo:** A Etapa 1 do MDD é um processo de coautoria guiado pelo MDD Coach, onde o diálogo se transforma em direção e a intuição em visão tangível.
