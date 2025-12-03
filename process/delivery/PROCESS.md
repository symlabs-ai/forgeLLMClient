# Delivery Process

**Da sprint de implementação até a entrega contínua, revisão e aprendizado.**

---

## 🌐 Visão Geral

O **Delivery Process** é o macro‑processo que:

- organiza o trabalho em **sprints e sessões**,
- conduz as **cerimônias de review** (técnico, processo e negócio),
- conecta o incremento pronto às **entregas** (deploy) e ao **monitoramento contínuo**.

Ele agrupa, de forma coesa, dois subprocessos:

1. **Sprint Management** – organização do trabalho em sprints e sessões.
2. **Review & Feedback** – validação técnica, de processo e de negócio antes de consolidar a entrega.

Em um projeto alvo, esses subprocessos vivem dentro de `process/delivery/`:

- `process/delivery/sprint/SPRINT_PROCESS.md`
- `process/delivery/review/REVIEW_PROCESS.md`

---

## 🔁 Fluxo Macro de Delivery

```text
Execution (backlog técnico pronto + código testado)
        │
        ▼
  Delivery
   1) Sprint Management
   2) Review & Feedback
        │
        ▼
 Deploy + Monitoramento (entrega contínua)
```

---

## 1️⃣ Sprint Management – "COMO organizar o trabalho em ciclos?"

- Define **como** o backlog técnico vindo da Execução será consumido:
  - sprints com sessões de 2–3h,
  - planning focado em itens claros de backlog,
  - session review (demo + aprovação),
  - acompanhamento de progresso (`progress.md`).
- Documento de referência:
  `process/delivery/sprint/SPRINT_PROCESS.md`

**Pergunta central:**
> Como organizar o fluxo de entregas em ciclos curtos, previsíveis e bem documentados?

---

## 2️⃣ Review & Feedback – "COMO validar, entregar e aprender?"

- Estrutura a **Sprint Review em 3 dias**:
  - **Dia 1 – bill-review (symbiota técnico)**:
    - valida código, arquitetura, testes, padrões,
    - gera `project/sprints/sprint-N/review.md`.
  - **Dia 2 – Jorge the Forge (symbiota de processo)**:
    - audita a aderência ao ForgeProcess,
    - gera `project/sprints/sprint-N/jorge-process-review.md`.
  - **Dia 3 – Stakeholder Review & Deploy**:
    - apresenta incrementos,
    - valida valor de negócio,
    - decide release / ajustes / rollback.
- Documento de referência:
  `process/delivery/review/REVIEW_PROCESS.md`

**Perguntas centrais:**
> O que foi entregue está tecnicamente sólido?
> Seguiu o processo combinado?
> Entrega valor real para o stakeholder?

---

## 🗂️ Estrutura de Pastas Alvo (Delivery)

Em um projeto que adota o ForgeProcess, o macro‑processo de delivery se distribui assim:

```text
process/
  └── delivery/
        ├── PROCESS.md                       ← Este documento (overview de delivery)
        ├── sprint/
        │     └── SPRINT_PROCESS.md
        └── review/
              └── REVIEW_PROCESS.md
```

> Este repositório guarda esses arquivos em `processes/forgeprocess/delivery/...`.
> Em um projeto alvo, ferramentas como `symforge init -p forgeprocess myproject` deverão
> copiar esse conteúdo para `process/delivery/` com o layout mostrado acima.

---

## 🔗 Relação com o PROCESS.md raiz

O `process/PROCESS.md` (documento raiz) enxerga:

- **MDD + BDD** como fase de **Concepção** (valor + comportamento).
- **Execution** como fase de **codificação** (design técnico + TDD).
- **Delivery** (este processo) como fase de:
  - organizar o trabalho em sprints,
  - revisar técnica e processualmente,
  - entregar incrementos e observar impacto,
  - alimentar um novo ciclo de MDD com o aprendizado.
