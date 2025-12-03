# Project Layout – ForgeProcess

**Contrato de estrutura de pastas para projetos inicializados com `symforge init -p forgeprocess myproject`.**

> **Comentário**
> Este layout não é “engessado”: ele define a base mínima para que o ForgeProcess,
> o `symforge` e os symbiotas funcionem. Times podem **estender** essa estrutura
> (por exemplo, adicionando pastas ou arquivos específicos do domínio) desde que
> mantenham compatibilidade com os caminhos principais documentados aqui.

> Este arquivo descreve a **estrutura alvo** que será criada em um projeto que adota o ForgeProcess.
> Nem todas as pastas são obrigatórias desde o primeiro dia; algumas são pontos de extensão.

Legenda:
- `[CORE]` – deve existir em todo projeto ForgeProcess.
- `[OPTIONAL]` – criado conforme necessidade.
- `[EXTENSION]` – ponto explícito de customização do time.

---

## 1. Estrutura Geral do Projeto

```text
<project_root>/
├── .symforge/                    # [CORE] Configurações locais do Symforge (ex.: config.yml)
├── process/                       # [CORE] Documentação de processo e symbiotas
├── specs/                         # [CORE] Especificações (BDD, roadmap, ADRs)
├── project/                       # [CORE] Artefatos de execução (sprints, reviews, MDD)
├── src/                           # [CORE] Código da aplicação/biblioteca
├── tests/                         # [CORE] Testes automatizados
├── docs/                          # [OPTIONAL] Documentação de produto/negócio
└── examples/                      # [OPTIONAL] Exemplos, demos, scripts de uso
```

---

## 2. Estrutura de `process/` (ForgeProcess)

```text
process/
├── PROCESS.md                     # [CORE] Visão geral do ForgeProcess
├── README.md                      # [CORE] Índice de processos
│
├── mdd/                           # [CORE] Market-Driven Development
│   ├── MDD_process.md
│   ├── etapa_01-05.md
│   └── templates/
│
├── bdd/                           # [CORE] Behavior-Driven Development
│   ├── BDD_PROCESS.md
│   ├── etapa_01-06.md
│   └── templates/
│
├── execution/                     # [CORE] Execução (arquitetura + TDD)
│   ├── PROCESS.md
│   ├── roadmap_planning/
│   │   └── ROADMAP_PLANNING_PROCESS.md
│   └── tdd/
│       └── TDD_PROCESS.md
│
├── delivery/                      # [CORE] Delivery (sprints + reviews)
│   ├── PROCESS.md
│   ├── sprint/
│   │   └── SPRINT_PROCESS.md
│   └── review/
│       └── REVIEW_PROCESS.md
│
├── docs/                          # [CORE] Documentação complementar de processo
│   ├── diagrams/                  # [CORE] Diagramas Mermaid
│   │   └── forgeprocess/
│   │       ├── macro_forgeprocess_flow.md
│   │       ├── mdd_process_flow.md
│   │       ├── bdd_process_flow.md
│   │       ├── roadmap_planning_process_flow.md
│   │       └── feedback_flow.md
│   └── policies/                  # [CORE] Políticas de processo
│       └── forgeprocess/
│           └── MVP_GUIDELINES.md
│
└── symbiotes/                     # [CORE] Symbiotas (agentes) que aplicam o processo
    ├── mdd_coach/
    │   └── prompt.md
    ├── mdd_publisher/
    │   └── prompt.md
    ├── bill_review/
    │   └── prompt.md
    └── jorge_forge/
        └── prompt.md
```

> `[EXTENSION]` – é permitido (e esperado) que times adicionem **novos symbiotas** em
> `process/symbiotes/` e **novas policies** em `process/docs/policies/` seguindo o
> mesmo formato dos exemplos fornecidos.

---

## 3. Estrutura de `specs/` (Especificações)

```text
specs/
├── bdd/                           # [CORE] Especificações BDD
│   ├── 00_glossario.md
│   ├── README.md
│   ├── HANDOFF_BDD.md
│   ├── tracks.yml
│   └── 10_forge_core/            # Exemplos de domínios
│       └── *.feature
│
├── roadmap/                       # [CORE] Roadmap & Arquitetura
│   ├── TECH_STACK.md
│   ├── ADR.md
│   ├── adr/
│   │   └── ADR-XXX-*.md
│   ├── HLD.md
│   ├── LLD.md
│   ├── ROADMAP.md
│   ├── BACKLOG.md
│   ├── dependency_graph.md
│   └── estimates.yml
│
└── adr/                           # [OPTIONAL] ADRs adicionais (separados por convenção local)
    └── ADR-XXX-*.md
```

---

## 4. Estrutura de `project/` (Execução)

```text
project/
├── mdd-artifacts/                 # [CORE] Artefatos de negócio do MDD
│   ├── hipotese.md
│   ├── visao.md
│   ├── sumario_executivo.md
│   ├── pitch_deck.md
│   ├── resultados_validacao.md
│   ├── revisao_estrategica.md
│   ├── aprovacao_mvp.md
│   └── rejeicao_projeto.md
│
├── sprints/                       # [CORE] Artefatos por sprint
│   └── sprint-N/
│       ├── planning.md
│       ├── progress.md
│       ├── review.md
│       ├── jorge-process-review.md
│       └── retrospective.md
│
└── reviews/                       # [OPTIONAL] Reviews técnicos adicionais
    └── review-FXX.md
```

---

## 5. Estrutura de `src/` e `tests/`

```text
src/                               # [CORE] Código do sistema
└── ...                            # Definido pelo projeto (ex.: forgellmclient/)

tests/                             # [CORE] Testes automatizados
├── unit/                          # [OPTIONAL] Testes unitários
├── integration/                   # [OPTIONAL] Testes de integração
└── bdd/                           # [CORE] Steps BDD
    ├── conftest.py
    └── test_*_steps.py
```

---

## 6. Pontos de Customização

Principais pontos previstos para customização do time/projeto:

- `process/docs/policies/` – adicionar novas políticas de processo (ex.: segurança, qualidade, compliance).
- `process/symbiotes/` – adicionar novos symbiotas especializados (ex.: security_auditor, ux_reviewer).
- `specs/bdd/` e `specs/roadmap/` – adaptar a organização por domínios conforme o contexto do projeto.
- `project/sprints/` – criar convenções próprias de nome de arquivos adicionais (`decisions.md`, `notes.md`, etc.).

> A recomendação é manter a estrutura **compatível com o que está documentado aqui**,
> para que ferramentas (como `symforge` e symbiotas) possam operar de forma previsível.
