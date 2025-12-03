# 🧭 Market Driven Development (MDD)

O **Market Driven Development (MDD)** é uma metodologia de desenvolvimento de produtos guiada por **sinais reais de mercado**, não por suposições internas.
Cada ciclo do MDD transforma uma **hipótese** em um **produto validado**, por meio de artefatos simples, versionáveis e legíveis em **Markdown (.md)**.
Todos os documentos em `.md` são a *fonte da verdade* — PDFs, slides e sites são **projeções renderizadas** desses arquivos.

---

## ⚙️ Macroetapas do MDD

O processo completo é composto por **seis macroetapas** e um conjunto padronizado de **artefatos Markdown**.

---

### 1) Concepção da Visão

📥 *Entrada:* `docs/hipotese.md`
📤 *Saída:* `docs/visao.md`

A partir de uma hipótese inicial, cria-se uma **visão clara e inspiradora** do produto.
É o momento de formular **propósito**, **problema de mercado**, **proposta de valor** e a **métrica inicial de validação**.
A visão é breve — normalmente um ou dois parágrafos — e segue o formato **Visão Canvas**.

> 🧩 Artefatos:
>
> * `docs/hipotese.md`
> * `docs/visao.md`
> * Templates em: `process/templates/template_hipotese.md` e `process/templates/template_visao.md`

---

### 2) Síntese Executiva

📥 *Entrada:* `docs/visao.md`
📤 *Saída:* `docs/sumario_executivo.md`
🗂️ *Exportável:* `output/docs/sumario_executivo.pdf`

Transforma a visão em um **plano estratégico conciso**, articulando **oportunidade**, **tamanho/potência de mercado**, **modelo de negócio** e **roadmap inicial**.
Base para discussão com fundadores, diretoria e investidores.

> 🧩 Artefatos:
>
> * `docs/sumario_executivo.md`
> * Template: `process/templates/template_sumario_executivo.md`
> * Renderização: `output/docs/sumario_executivo.pdf`

---

### 3) Pitch de Valor

📥 *Entrada:* `docs/visao.md` + `docs/sumario_executivo.md`
📤 *Saída:* `docs/pitch_deck.md`
🗂️ *Exportável:* `output/docs/pitch_deck.pptx`

Converte o sumário em **narrativa visual e emocional** para investidores/parceiros.
O original permanece em Markdown; o `.pptx` é gerado por ferramenta externa.

> 🧩 Artefatos:
>
> * `docs/pitch_deck.md`
> * Template: `process/templates/template_pitch_deck.md`
> * Renderização: `output/docs/pitch_deck.pptx`

---

### 4) Validação Pública Inicial (Landing Tests)

📥 *Entrada:* `docs/visao.md` + `docs/sumario_executivo.md` + `docs/pitch_deck.md`
📤 *Saídas:* `docs/sites/site_A.md`, `docs/sites/site_B.md`, `docs/sites/site_C.md`
🗂️ *Exportáveis:* `output/docs/sites_renderizados/`

Criação de **landing pages experimentais** para validar interesse real do público.
Cada variação (A/B/C) ajusta narrativa, promessa e CTA.
Páginas são convertidas em HTML (ex.: **Gama**, **Next.js**, **Jekyll**).

> 🧩 Artefatos:
>
> * `docs/sites/site_A.md`, `docs/sites/site_B.md`, `docs/sites/site_C.md`
> * Template: `process/templates/template_site.md`
> * Renderização: `output/docs/sites_renderizados/`

---

### 5) Avaliação e Retroalimentação Estratégica

📥 *Entrada:* `docs/resultados_validacao.md`
📤 *Saídas possíveis:* `docs/revisao_estrategica.md` **ou** `docs/aprovacao_mvp.md` **ou** `docs/rejeicao_projeto.md`

Etapa de **reflexão simbiótica**: análise de dados dos sites/formulários e decisão sobre próximo passo: **aprovar**, **revisar**, **encerrar**.
Fecha o ciclo atual e pode iniciar um novo.

> 🧩 Artefatos:
>
> * `docs/resultados_validacao.md`
> * `docs/revisao_estrategica.md`
> * `docs/aprovacao_mvp.md`
> * `docs/rejeicao_projeto.md`
> * Templates: `process/templates/template_resultados_validacao.md`, `template_revisao_estrategica.md`, `template_aprovacao_mvp.md`, `template_rejeicao_projeto.md`

---

### 6) Handoff para Especificação de Comportamento

📥 *Entrada:* `docs/aprovacao_mvp.md` (A decisão final da etapa anterior)
📤 *Saída Formal:* Início do **BDD Process**

Com a validação de mercado e a aprovação do MVP, o ciclo MDD é concluído. O controle é formalmente transferido para o **BDD Process**, que usará a visão e a aprovação como base para detalhar os comportamentos do sistema. O MDD não cria especificações BDD; ele autoriza sua criação.

---

## 🗂️ Estrutura de Pastas Alvo (projetos ForgeProcess)

> **Nota sobre este repositório**
> Este repositório **não** cria diretórios de projeto como `project/`, `process/`, `docs/` ou `output/`.
> Ele apenas define a **estrutura padrão** que será criada em projetos reais por ferramentas como
> `symforge init -p forgeprocess myproject`.
>
> - **Templates** ficam em `process/templates/` (no projeto alvo).
> - **Artefatos entregues** ficam em `docs/`.
> - **Renderizações** ficam em `output/docs/`.

```plaintext
project/
 +-- process/
 ¦    +-- docs/
 ¦    ¦     +-- templates/
 ¦    ¦     ¦     +-- template_hipotese.md
 ¦    ¦     ¦     +-- template_visao.md
 ¦    ¦     ¦     +-- template_sumario_executivo.md
 ¦    ¦     ¦     +-- template_pitch_deck.md
 ¦    ¦     ¦     +-- template_site.md
 ¦    ¦     ¦     +-- template_resultados_validacao.md
 ¦    ¦     ¦     +-- template_revisao_estrategica.md
 ¦    ¦     ¦     +-- template_aprovacao_mvp.md
 ¦    ¦     ¦     +-- template_rejeicao_projeto.md
 ¦    ¦
 ¦    +-- symbiotas/
 ¦          +-- mdd_coach/
 ¦                +-- prompt.md
 ¦
 +-- docs/
 ¦    +-- hipotese.md
 ¦    +-- visao.md
 ¦    +-- sumario_executivo.md
 ¦    +-- pitch_deck.md
 ¦    +-- sites/
 ¦    ¦     +-- site_A.md
 ¦    ¦     +-- site_B.md
 ¦    ¦     +-- site_C.md
 ¦    +-- resultados_validacao.md
 ¦    +-- revisao_estrategica.md
 ¦    +-- aprovacao_mvp.md
 ¦    +-- rejeicao_projeto.md
 ¦
 +-- output/
 ¦    +-- docs/
 ¦    ¦     +-- sumario_executivo.pdf
 ¦    ¦     +-- pitch_deck.pptx
 ¦    ¦     +-- sites_renderizados/
 ¦    +-- logs/
 ¦         +-- execucao_mdd.log
 ¦
 +-- data/
      +-- validacao/
  +-- specs/
       +-- bdd/
            +-- 00_glossario.md
            +-- 10_forge_core/
            +-- 20_symclient_http/
            +-- 21_symclient_stdio/
            +-- 30_plugins_provedores/
            +-- 40_mcp_tecnospeed/
            +-- 41_llm_broker_tecnospeed/
            +-- 50_observabilidade/
            +-- 60_seguranca/
```

---

## 📈 Diagrama do Fluxo do Processo (PlantUML — fundo branco)

```plantuml
@startuml
!option handwritten true

skinparam backgroundColor #FFFFFF
skinparam defaultTextAlignment center
skinparam node {
  BackgroundColor #F7F9FB
  BorderColor #2B70C9
  FontColor #0D1117
  FontSize 14
  FontName Consolas
}
skinparam note {
  BackgroundColor #E8EEF5
  BorderColor #B4C7E7
  FontColor #1C1C1C
}
skinparam arrow {
  Color #2B70C9
  FontColor #0D1117
  Thickness 2
}
skinparam legend {
  BackgroundColor #F7F9FB
  BorderColor #B4C7E7
  FontColor #0D1117
}

'tags principais
node "Etapa 1\n**Concepção da Visão**\n\nEntrada: docs/hipotese.md\nSaída: docs/visao.md" as E1
note right of E1
Cria a visão clara e inspiradora
com base na hipótese do mercado.
Define propósito, problema,
público e métrica inicial.
end note

node "Etapa 2\n**Síntese Executiva**\n\nEntrada: docs/visao.md\nSaída: docs/sumario_executivo.md" as E2
note right of E2
Transforma a visão em plano estratégico:
mercado, modelo de negócio, roadmap.
end note

node "Etapa 3\n**Pitch de Valor**\n\nEntrada: visao.md + sumario_executivo.md\nSaída: docs/pitch_deck.md" as E3
note right of E3
Converte o sumário em narrativa visual
para investidores e parceiros.
end note

node "Etapa 4\n**Validação Pública Inicial**\n\nEntrada: visao.md + sumario_executivo.md + pitch_deck.md\nSaída: docs/sites A/B/C (.md)" as E4
note right of E4
Cria variações de landing pages (.md)
para testar interesse real do mercado.
Coleta conversões e feedbacks.
end note

node "Etapa 5\n**Avaliação Estratégica**\n\nEntrada: docs/resultados_validacao.md\nSaídas: revisao_estrategica.md / aprovacao_mvp.md / rejeicao_projeto.md" as E5
note right of E5
Analisa resultados de validação e decide:
Aprovar, Revisar ou Encerrar o ciclo.
end note

E1 --> E2 : Gera sumário estratégico
E2 --> E3 : Gera narrativa de pitch
E3 --> E4 : Gera sites de teste (A/B/C)
E4 --> E5 : Coleta dados e feedback

node "Etapa 6\n**Handoff para BDD**\n\nEntrada: docs/aprovacao_mvp.md\nSaída: Início do BDD Process" as E6

node "docs/aprovacao_mvp.md\n🚀 Avançar para MVP" as OK
node "docs/revisao_estrategica.md\n🔁 Reavaliar proposta" as REV
node "docs/rejeicao_projeto.md\n🛑 Encerrar ciclo" as REJ

E5 --> OK : Aprovação
E5 --> REV : Revisão
E5 --> REJ : Rejeição

OK --> E6 : Handoff para Especificação

REV -[#2B70C9]-> E2 : Retorna ao ciclo
REJ -[#8b949e]-> E1 : Arquiva aprendizado

legend right
  == LEGENDA ==
  🧩 Artefatos: arquivos Markdown (.md)
  👥 Público:
    - Interno → Etapas 1 e 2
    - Investidores → Etapa 3
    - Consumidores → Etapa 4
  🔁 Feedback simbiótico:
    - Etapa 5 alimenta novas visões
endlegend

@enduml
```

---

## 🧠 Nota de filosofia prática

> O MDD não existe para **acelerar a entrega**; ele existe para **acelerar o aprendizado**.
> Cada artefato é uma conversa entre o humano e o mercado — e o produto é o resultado dessa escuta mútua.
