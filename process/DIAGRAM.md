# Resumo do Processo

**ID:** `forgeprocess`
**Versão:** 2.0.0
**Título:** ForgeProcess
**Tipo:** Processo Principal

**Descrição:**
> Ciclo de raciocínio que transforma intenção de valor em comportamentos verificáveis, código testado, execução observável e aprendizado contínuo, medindo progresso em unidades de valor de negócio em vez de tempo, tarefas ou story points.


## Subprocessos

| ID | Descrição | Retornos Esperados |
|----|-----------|-------------------|
| `mdd` | Market Driven Development - validação de mercado e definição de valor | approved, rejected |
| `bdd` | Behavior Driven Development - especificação de comportamentos em Gherkin | complete, needs_mdd_revision |
| `execution` | Execution - Roadmap Planning + TDD | complete, needs_bdd_revision |
| `delivery` | Delivery - Sprint Management + Review | deployed, needs_revision |

## Fases

| Fase | Nome | Passos | Subprocesso |
|------|------|--------|-------------|
| `mdd` | MDD — Market Driven Development | 0 | mdd/PROCESS.yml |
| `bdd` | BDD — Behavior Driven Development | 0 | bdd/PROCESS.yml |
| `execution` | Execution — Roadmap + TDD | 0 | execution/PROCESS.yml |
| `delivery` | Delivery — Sprint + Review | 0 | delivery/PROCESS.yml |
| `feedback` | Feedback — Reflexão | 2 | - |

## Fluxo

**Total de nós:** 11

| Tipo | Quantidade |
|------|------------|
| 📦 Chamada | 4 |
| 🔀 Decisão | 2 |
| ⏹ Fim | 2 |
| ▶ Início | 1 |
| 📋 Passo | 2 |

**Decisões:**
- 👤 HIL (humanas): 2


---

## Hierarquia de Processos

```mermaid
flowchart TB
    forgeprocess["ForgeProcess"]

    mdd["Market Driven Development -..."]
    forgeprocess --> mdd
    bdd["Behavior Driven Development..."]
    forgeprocess --> bdd
    execution["Execution - Roadmap Plannin..."]
    forgeprocess --> execution
    delivery["Delivery - Sprint Managemen..."]
    forgeprocess --> delivery

    classDef main fill:#4CAF50,stroke:#333,stroke-width:2px,color:#fff
    classDef sub fill:#2196F3,stroke:#333,stroke-width:1px,color:#fff
    class forgeprocess main
    class mdd,bdd,execution,delivery sub
```

---

## Diagrama de Fluxo

```mermaid
flowchart TD
    start(["▶ Início"])
    call_mdd[["📦 Market Driven Development -..."]]
    call_bdd[["📦 Behavior Driven Development..."]]
    call_execution[["📦 Execution - Roadmap Plannin..."]]
    call_delivery[["📦 Delivery - Sprint Managemen..."]]
    feedback_collect["Coletar métricas operacionais e ..."]
    feedback_analyze["Analisar feedback e gerar recome..."]
    decisao_mudar_visao{"👤 A visão ou hipótese de valor pre..."}
    decisao_continuar_ciclo{"👤 O produto está completo ou há ma..."}
    end_ciclo_completo(["⏹ Ciclo ForgeProcess concluíd..."])
    end_projeto_rejeitado(["⏹ Projeto rejeitado na fase MDD"])

    start --> call_mdd
    call_mdd -->|"approved"| call_bdd
    call_mdd -->|"rejected"| end_projeto_rejeitado
    call_bdd -->|"complete"| call_execution
    call_bdd -->|"needs_mdd_revision"| call_mdd
    call_execution -->|"complete"| call_delivery
    call_execution -->|"needs_bdd_revision"| call_bdd
    call_delivery -->|"deployed"| feedback_collect
    call_delivery -->|"needs_revision"| call_execution
    feedback_collect --> feedback_analyze
    feedback_analyze --> decisao_mudar_visao
    decisao_mudar_visao -->|"yes"| call_mdd
    decisao_mudar_visao -->|"no"| decisao_continuar_ciclo
    decisao_continuar_ciclo -->|"continuar"| call_bdd
    decisao_continuar_ciclo -->|"completo"| end_ciclo_completo

    %% Estilos
    classDef startEnd fill:#d4edda,stroke:#28a745,stroke-width:2px
    classDef stepNode fill:#e1f5ff,stroke:#333,stroke-width:1px
    classDef decisionNode fill:#fff4e6,stroke:#ff9800,stroke-width:2px
    classDef subprocessCall fill:#e8daef,stroke:#8e44ad,stroke-width:2px
    classDef returnNode fill:#fadbd8,stroke:#e74c3c,stroke-width:2px
    class start,end_ciclo_completo,end_projeto_rejeitado startEnd
    class feedback_collect,feedback_analyze stepNode
    class decisao_mudar_visao,decisao_continuar_ciclo decisionNode
    class call_mdd,call_bdd,call_execution,call_delivery subprocessCall
```

---

## Diagrama de Estados

```mermaid
stateDiagram-v2
    [*] --> start
    start --> call_mdd
    call_mdd --> call_bdd: approved
    call_mdd --> end_projeto_rejeitado: rejected
    call_bdd --> call_execution: complete
    call_bdd --> call_mdd: needs_mdd_revision
    call_execution --> call_delivery: complete
    call_execution --> call_bdd: needs_bdd_revision
    call_delivery --> feedback_collect: deployed
    call_delivery --> call_execution: needs_revision
    feedback_collect --> feedback_analyze
    feedback_analyze --> decisao_mudar_visao
    decisao_mudar_visao --> call_mdd: yes
    decisao_mudar_visao --> decisao_continuar_ciclo: no
    decisao_continuar_ciclo --> call_bdd: continuar
    decisao_continuar_ciclo --> end_ciclo_completo: completo
```
