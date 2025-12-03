# Execution Process

**Do comportamento especificado (BDD) até o design técnico e o código testado.**

---

## 🌐 Visão Geral

O **Execution Process** é o macro‑processo que conecta o que foi
especificado em **BDD** com um **backlog técnico claro** e um **código testado**.

Ele agrupa, de forma coesa, dois subprocessos:

1. **Roadmap Planning** – arquitetura, sequenciamento e backlog executável.
2. **TDD Workflow** – implementação guiada por testes (Red–Green–Refactor).

Em um projeto alvo, esses subprocessos vivem dentro de `process/execution/`:

- `process/execution/roadmap_planning/ROADMAP_PLANNING_PROCESS.md`
- `process/execution/tdd/TDD_PROCESS.md`

---

## 🔁 Fluxo Macro de Execução

```text
BDD (O QUÊ fazer)
        │
        ▼
 Execution
   1) Roadmap Planning
   2) TDD Workflow
        │
        ▼
 Backlog técnico implementado e testado
```

---

## 1️⃣ Roadmap Planning – "QUANDO e COMO?"

- Traduz as features BDD em um **plano executável**:
  - decisões de stack e arquitetura (ADRs, HLD, LLD),
  - análise de dependências,
  - estimativas e priorização,
  - criação de `ROADMAP.md` e `BACKLOG.md`.
- Documento de referência:
  `process/execution/roadmap_planning/ROADMAP_PLANNING_PROCESS.md`

**Pergunta central:**
> Em que ordem, com quais decisões técnicas e por quem estas features serão implementadas?

---

## 2️⃣ TDD Workflow – "COMO implementar com prova?"

- Detalha o ciclo **Red → Green → Refactor** por feature:
  - partir de cenários BDD e itens do backlog,
  - escrever testes antes do código,
  - implementar o mínimo para passar,
  - refatorar com segurança.
- Documento de referência:
  `process/execution/tdd/TDD_PROCESS.md`

**Pergunta central:**
> Como transformar especificações BDD em código confiável, com testes guiando cada passo?

---

## 🗂️ Estrutura de Pastas Alvo (Execução)

Em um projeto que adota o ForgeProcess, o macro‑processo de execução se distribui assim:

```text
process/
  └── execution/
        ├── PROCESS.md                        ← Este documento (overview da execução)
        ├── roadmap_planning/
        │     └── ROADMAP_PLANNING_PROCESS.md
        ├── tdd/
        │     └── TDD_PROCESS.md
        └── (demais fases de delivery e feedback vivem em `process/delivery/…`)
```

> Este repositório guarda esses arquivos em `processes/forgeprocess/...`.
> Em um projeto alvo, ferramentas como `symforge init -p forgeprocess myproject` deverão
> copiar esse conteúdo para `process/` com o layout mostrado acima.

---

## 🔗 Relação com o PROCESS.md raiz

O `process/PROCESS.md` (documento raiz) enxerga:

- **MDD** como definição de valor de mercado.
- **BDD** como especificação verificável de comportamento.
- **Execution** (este processo) como o caminho técnico:
  - do comportamento especificado até o backlog técnico e o código testado,
  - servindo de base para a fase de **Delivery contínua**.
