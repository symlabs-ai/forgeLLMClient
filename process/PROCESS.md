# ForgeProcess: Ciclo de Raciocínio Completo

**O raciocínio que transforma intenção em execução e aprendizado.**

---

## 🚀 Getting Started

Após inicializar seu projeto com `symforge init -p forgeprocess <nome-projeto>`:

### Primeiro Passo: Registre sua Hipótese

O ForgeProcess começa com uma **hipótese de mercado**. Antes de qualquer código,
você precisa documentar a oportunidade que pretende explorar.

1. Abra o arquivo `docs/hipotese.md` (criado automaticamente a partir do template)
2. Preencha as seções seguindo o guia do template
3. Execute `symforge start` para iniciar o processo

### Comandos Essenciais

```bash
symforge start          # Inicia o processo
symforge status         # Mostra estado atual
symforge resume         # Retoma execução
symforge tui            # Interface interativa
symforge decide <opcao> # Registra decisão
```

### Fluxo do Processo

```
docs/hipotese.md → MDD (validação) → BDD (comportamentos) → Execution (código) → Delivery
```

### Documentação

- `process/PROCESS.md` — Este documento (especificação completa)
- `process/README.md` — Guia rápido
- `process/mdd/templates/` — Templates para cada etapa

---

## 🌟 O Renascimento do Desenvolvimento Baseado em Valor

### Do Tempo ao Valor: Uma Mudança de Paradigma

Durante anos, o desenvolvimento de software foi governado por metodologias que mediam esforço em **tempo** — horas, sprints, entregas. O **ForgeProcess** propõe uma inversão radical: **medir o valor, não o tempo**.

```
Tradicional:    "Quantos dias leva?"
                 ↓
ForgeProcess:   "Quanto valor entregamos?"
```

#### O Que São Unidades de Valor de Negócio?

**Unidade de Valor de Negócio** = Unidade de comportamento significativo que entrega resultado ao cliente

Exemplos:
- ❌ "Implementamos 5 classes" → Esforço técnico
- ✅ "Reduzimos abandono de carrinho em 20%" → **Unidade de Valor de Negócio**

- ❌ "Criamos 15 testes" → Atividade
- ✅ "Garantimos 0 erros em cálculo fiscal" → **Unidade de Valor de Negócio**

#### A Mudança de Foco

| Métrica Tradicional | ForgeProcess |
|---------------------|--------------|
| Velocidade de entrega | **Direção de valor** |
| "Entregamos em 2 semanas" | "Aumentamos conversão em 15%" |
| Sprint points | **Business value** |
| Features implementadas | **Behaviors validados** |

> *"Não importa o quão rápido o time progrida, se estiver indo para o lado errado."*

---

## 🎯 Visão Geral

O **ForgeProcess** é o sistema de raciocínio arquitetural do Forge Framework. Ele não é apenas uma metodologia, mas um **ciclo de raciocínio** que transforma:

```
Intenção (Valor) → Comportamento → Prova → Execução → Aprendizado → Mais Valor
```

O ForgeProcess opera em **fases integradas**, cada uma representando um nível de refinamento do pensamento.

> **Nota Importante sobre estrutura:**
> - Este repositório contém apenas a **documentação padrão** do ForgeProcess, em `processes/forgeprocess/...`.
> - Referências a `process/...`, `specs/...` e `project/...` descrevem a **estrutura alvo** de um projeto que adota o ForgeProcess (por exemplo, criada via `symforge init -p forgeprocess myproject`).
> - MDD e BDD são **processos independentes e detalhados**:
>   - **MDD Process**: `process/mdd/MDD_process.md` (6 etapas)
>   - **BDD Process**: `process/bdd/BDD_PROCESS.md` (6 subetapas)
> - Execution e Delivery são macro‑processos complementares:
>   - **Execution**: `process/execution/PROCESS.md` (Roadmap Planning + TDD)
>   - **Delivery**: `process/delivery/PROCESS.md` (Sprints + Review & Feedback)
> - A estrutura completa de pastas alvo está descrita em:
>   - **Project Layout**: `process/docs/layout/PROJECT_LAYOUT.md`

```
┌─────────────────────────────────────────────────────┐
│ 1. MDD — Market Driven Development                  │
│    "PORQUÊ existir?"                                │
│    Intenção de Valor                                │
│    📁 process/mdd/MDD_process.md                    │
└────────────────┬────────────────────────────────────┘
                 │
                 │ Tradução
                 │ (Valor → Comportamento)
                 ▼
┌─────────────────────────────────────────────────────┐
│ 2. BDD — Behavior Driven Development                │
│    "O QUÊ fazer?"                                   │
│    Comportamento Verificável                        │
│    📁 process/bdd/BDD_PROCESS.md                    │
└────────────────┬────────────────────────────────────┘
                 │
                 │ Planejamento Executivo
                 │ (Comportamento → Arquitetura e Backlog)
                 ▼
┌─────────────────────────────────────────────────────┐
│ 3. Execution                                        │
│    "COMO codar?"                                    │
│    Arquitetura, backlog técnico e código testado    │
│    📁 process/execution/PROCESS.md                  │
└────────────────┬────────────────────────────────────┘
                 │
                 │ Handoff para Delivery
                 ▼
┌─────────────────────────────────────────────────────┐
│ 4. Delivery                                         │
│    "COMO entregar continuamente e aprender?"        │
│    Sprints, reviews, deploy e métricas              │
│    📁 process/delivery/PROCESS.md                   │
└────────────────┬────────────────────────────────────┘
                 │
                 │ Loop de Aprendizado
                 └─────────────────────┐
                                       │
                  ┌────────────────────┘
                  ▼
              Volta para MDD
             (Ciclo se fecha)
```

---

## 📖 As Fases do ForgeProcess

### 1️⃣ MDD — Market Driven Development

**"PORQUÊ este sistema deve existir?"**

#### Propósito
Definir o **valor de mercado** que o sistema entrega. É a fase onde a **estratégia de negócio** se transforma em **intenção arquitetural**.

#### Artefatos Principais
- **`project/docs/visao.md`**: Documento de visão (PORQUÊ o sistema existe)
- **ValueTracks**: Fluxos que entregam valor direto ao usuário (o que o cliente vê)
- **SupportTracks**: Fluxos que suportam a entrega de valor (o alicerce invisível)
- **Value KPIs**: Métricas que comprovam entrega de valor

#### ValueTracks vs SupportTracks: A Simbiose do Valor

```
┌─────────────────────────────────────────────────────┐
│ VALUE TRACKS                                        │
│ "O que o cliente vê e experimenta"                  │
├─────────────────────────────────────────────────────┤
│ - Processar pedido em 1 clique                      │
│ - Reduzir abandono de carrinho em 20%              │
│ - Emitir nota fiscal sem erros                      │
│ - Rastreamento em tempo real                        │
│                                                     │
│ Medida: Impacto no negócio (KPIs)                  │
└─────────────────────────────────────────────────────┘
                       ▲
                       │ sustentado por
                       │
┌─────────────────────────────────────────────────────┐
│ SUPPORT TRACKS                                      │
│ "O que garante confiabilidade e qualidade"          │
├─────────────────────────────────────────────────────┤
│ - Testes automatizados BDD                          │
│ - CI/CD pipeline                                    │
│ - Monitoramento e observabilidade                   │
│ - Infraestrutura e escalabilidade                   │
│                                                     │
│ Medida: Confiabilidade técnica (Métricas)          │
└─────────────────────────────────────────────────────┘
```

**Fluxo Bidirecional**:
- **Value → Support**: "Precisamos de checkout 1-clique" gera necessidade de "Testes automatizados de pagamento"
- **Support → Value**: "Pipeline CI/CD robusto" permite "Entregas diárias sem medo"

**Exemplo Completo**:

| Tipo | Track | Unidade de Valor de Negócio | Medida |
|------|-------|----------------|--------|
| VALUE | "Checkout 1-clique" | Redução de abandono em 20% | Conversão aumentou de 60% → 80% |
| SUPPORT | "Testes BDD automatizados" | 0 bugs em produção | 100% scenarios passando |
| VALUE | "Nota fiscal automática" | 0 erros fiscais | Multas evitadas: R$ 0 |
| SUPPORT | "CI/CD com validação fiscal" | Deploy seguro | 95% dos commits auto-validados |

> *"Cada comportamento de negócio precisa de sustentação técnica — e cada automação técnica deve justificar sua existência pelo valor que possibilita."*

#### Exemplo: visao.md

```markdown
# Visão do Produto: OrderManagement

## Propósito
Permitir que lojistas gerenciem pedidos de forma ágil e segura

## Proposta de Valor
- Reduzir tempo de processamento de pedidos em 50%
- Eliminar erros manuais em emissão de notas
- Aumentar satisfação do cliente com rastreamento em tempo real

## ValueTracks

### ProcessOrder
**Descrição**: Processar pedido completo do início ao fim
**Métrica de Valor**: Tempo médio de processamento < 2 minutos
**Stakeholders**: Lojista, Cliente final

### IssueInvoice
**Descrição**: Emitir nota fiscal automaticamente
**Métrica de Valor**: 0 erros manuais em cálculo de impostos
**Stakeholders**: Lojista, Contador

## SupportTracks

### ManageInventory
**Descrição**: Controlar estoque de produtos
**Suporta**: ProcessOrder

### CalculateTaxes
**Descrição**: Calcular impostos corretamente
**Suporta**: IssueInvoice

## KPIs

| Métrica | Target | Atual |
|---------|--------|-------|
| Order Processing Time | < 2 minutos | 4.5 minutos |
| Invoice Error Rate | 0% | 3.2% |
```

#### Perguntas que o MDD Responde
- ✅ Qual problema estamos resolvendo?
- ✅ Para quem estamos resolvendo?
- ✅ Como medimos se estamos entregando valor?
- ✅ Qual o diferencial competitivo?

---

### 🔄 Transição Crítica: MDD → BDD

**O momento de tradução: Valor → Comportamento**

Esta é a transição mais importante do ForgeProcess. Aqui, conceitos abstratos de valor se transformam em ações concretas e verificáveis.

#### Mapeamento

| Do MDD | Para o BDD |
|--------|------------|
| **Propósito**: "O sistema ajuda o usuário a processar pedidos rapidamente" | **Cenário**: "Dado que há um pedido válido, quando eu processá-lo, então ele deve ser concluído em < 2 minutos" |
| **ValueTrack**: "IssueInvoice" | **Feature**: "Emissão automática de nota fiscal com cálculo de impostos" |
| **Value KPI**: "0 erros em cálculo" | **Critério de Aceitação**: "Todos os impostos devem ser calculados corretamente" |

#### Exemplo de Tradução

**MDD (Intenção em visao.md)**:
```markdown
### CreateUser
**Descrição**: Permitir cadastro rápido e seguro de usuários
**Métrica de Valor**: 95% dos cadastros completados em < 30 segundos
```

**BDD (Comportamento)**:
```gherkin
Feature: Cadastro rápido e seguro de usuários
  Para que usuários possam começar a usar o sistema rapidamente
  Como um visitante
  Eu quero me cadastrar de forma simples e segura

  Scenario: Cadastro bem-sucedido
    Given que eu estou na página de cadastro
    And eu preencho nome "Alice Silva"
    And eu preencho email "alice@example.com"
    And eu preencho senha válida
    When eu clico em "Criar conta"
    Then minha conta deve ser criada em menos de 30 segundos
    And eu devo receber um email de confirmação
    And o sistema deve validar que o email é único
```

#### Por que esta Transição é Crítica?

1. **Abstrato → Concreto**: Valor (abstrato) vira comportamento (concreto)
2. **Intenção → Ação**: Propósito vira cenário executável
3. **Métrica → Critério**: KPI vira critério de aceitação
4. **Estratégia → Tática**: Visão vira especificação

---

### 2️⃣ BDD — Behavior Driven Development

**"O QUÊ o sistema faz?"**

> **Nota:** O BDD é agora um **processo independente** com 6 subetapas detalhadas.
>
> **Documentação completa:** `process/bdd/BDD_PROCESS.md`

#### Propósito
O BDD é a **ponte entre valor validado (MDD) e código testado (TDD)**. Ele transforma comportamentos de negócio em especificações executáveis que servem simultaneamente como:
- Documentação viva
- Contrato entre stakeholders e dev
- Testes automatizados

#### Subetapas do BDD Process

```
1. Mapeamento de Comportamentos  → behavior_mapping.md
2. Escrita de Features Gherkin   → specs/bdd/**/*.feature
3. Organização e Tagging         → Estrutura + tags
4. Criação de tracks.yml         → Rastreabilidade
5. Skeleton de Automação         → tests/bdd/test_*_steps.py
6. Handoff para TDD              → HANDOFF.md
```

#### Artefatos Principais
- **Features Gherkin**: Arquivos `.feature` (PT-BR, tags, estrutura padrão Forge)
- **tracks.yml**: Mapeia features → ValueTracks → métricas
- **Step definitions**: Skeleton pytest-bdd (inicialmente com `@skip`)
- **HANDOFF.md**: Documentação de entrega para TDD

#### ⚠️ MVP Exception Policy (NEW - 2025-11-06)

**Standard Rule**: ALL features MUST have complete BDD scenarios before implementation.

**MVP Exception**: Under specific conditions, features may be delivered as MVP with reduced BDD coverage.

**When MVP is Acceptable**:
- ✅ Stakeholder explicitly approves MVP approach (documented)
- ✅ Value validated with interactive demo (ADR-010 compliance)
- ✅ Full Implementation planned in future sprint (tracked in BACKLOG.md)
- ✅ MVP status clearly documented ("incomplete" label)

**Full Guidelines**: See `process/docs/policies/MVP_GUIDELINES.md` para critérios completos, template de proposta e workflow.

**Why This Exists**: Sprint 1 (2025-11-06) validated that MVP strategy works for fast value delivery (F11_MVP, F12A_MVP) but needs formal policy to maintain process compliance (Jorge's recommendation 7.8/10).

#### Exemplo: Feature File (Padrão Forge)

```gherkin
# specs/bdd/10_forge_core/chat.feature

@sdk @ci-fast
FUNCIONALIDADE: Chat básico no Forge SDK
  PARA enviar mensagens e receber respostas de LLMs
  COMO um desenvolvedor Python
  QUERO usar uma interface consistente independente do provedor

  CONTEXTO:
    DADO que o Forge está instalado
    E o ambiente de teste está configurado

  CENÁRIO: Enviar mensagem simples e receber resposta
    DADO que o Forge está configurado com o provedor "echo"
    QUANDO envio a mensagem "Olá, mundo!"
    ENTÃO recebo uma resposta contendo "Olá, mundo!"
    E a resposta tem formato válido de ChatResponse
    E o log registra o evento com status "success"

  CENÁRIO: Erro ao usar provedor não configurado
    DADO que o Forge não está configurado com nenhum provedor
    QUANDO tento enviar uma mensagem
    ENTÃO recebo um erro do tipo ConfigurationError
    E a mensagem de erro contém "Provedor não configurado"
```

#### Como BDD se Conecta com o Código

Cada **CENÁRIO** Gherkin:
1. É vinculado a **step definitions** (pytest-bdd)
2. Guia a implementação via **TDD** (Red-Green-Refactor)
3. Serve como **documentação viva** e **teste automatizado**
4. É rastreável até **ValueTracks do MDD** via `tracks.yml`

#### Ferramentas e Estrutura
- **Framework**: pytest-bdd >= 6.1.1
- **Especificação**: `specs/bdd/**/*.feature`
- **Automação**: `tests/bdd/test_*_steps.py`
- **Rastreabilidade**: `specs/bdd/tracks.yml`

#### Documentação Completa do Processo BDD

Para detalhes sobre como executar todas as 6 subetapas do BDD Process:
- **Visão geral**: `process/bdd/BDD_PROCESS.md`
- **Subetapas 1-6**: `process/bdd/etapa_01_*.md` até `etapa_06_*.md`
- **Templates**: `process/bdd/templates/`

#### BDD como Linguagem Universal do Forge

**Por que BDD é o idioma natural do ForgeProcess?**

```
Stakeholder (Negócio)  ──┐
                         │
Product Owner (Produto) ──┼──> TODOS FALAM GHERKIN
                         │
  Developer (Código)      ──┤
                         │
  QA (Testes)             ──┘

Terminologia dos entregáveis (produto)
- forgeLLMClient: SDK Python (módulo) para integração multi‑provedor.
- SymClient: Servidor local com protocolos HTTP e STDIO/JSON‑RPC (language‑agnostic).

Provedores iniciais e capacidades v1
- Local: llama‑cpp (prioritário)
- Roteador: OpenRouter (interino)
- Capacidades alvo v1: tool calling, contexto/sessões, streaming (quando disponível), MCP (Marketplace), roteamento (Broker)
```

**Antes do BDD** (cada um fala um idioma):
- Negócio: "Precisamos aumentar vendas"
- Produto: "Vamos fazer checkout rápido"
- Dev: "Implementei um PaymentService com factory pattern"
- QA: "Testei 15 casos de teste do Jira"

❌ **Problema**: Ninguém garante que todos falam da mesma coisa!

**Com BDD** (todos falam a mesma língua):

```gherkin
FUNCIONALIDADE: Checkout em 1 clique
  PARA aumentar conversão em vendas          ← Negócio entende
  COMO um comprador recorrente               ← Produto entende
  QUERO finalizar compra com um clique       ← Todos entendem

  CENÁRIO: Compra rápida com cartão salvo
    DADO que tenho um cartão salvo           ← Dev implementa
    QUANDO clico em "Comprar agora"          ← QA testa
    ENTÃO vejo "Compra confirmada!"          ← Negócio valida
    E recebo email de confirmação            ← Todos verificam
```

✅ **Solução**: Uma única especificação que todos entendem, implementam e validam!

**Padrão Forge: Tags em MAIÚSCULO (Português)**

```gherkin
# ✅ CORRETO (padrão Forge)
FUNCIONALIDADE: Emissão de nota fiscal
  CENÁRIO: Cálculo de ICMS
    DADO pedido de R$ 1000 em SP
    QUANDO emitir nota
    ENTÃO ICMS deve ser R$ 180

# ❌ Evitar (inglês ou misturado)
Feature: Invoice issuance
  Scenario: ICMS calculation
    Given order of R$ 1000 in SP
    ...
```

**Por que maiúsculo e português?**
1. **Reduz ambiguidade**: DADO/QUANDO/ENTÃO são claramente tags estruturais
2. **Democratiza acesso**: Stakeholders brasileiros entendem sem barreira de idioma
3. **Documentação viva**: O código E a documentação são o mesmo artefato
4. **Rastreabilidade**: Cada linha de código rastreia até um behavior

**Ciclo de Vida de um Behavior**:

```
1. Stakeholder expressa valor
   "Quero reduzir abandono de carrinho"

2. PO escreve em Gherkin
   FUNCIONALIDADE: Checkout 1-clique
   CENÁRIO: Compra rápida

3. Dev implementa
   class QuickCheckoutUseCase(UseCaseBase):
       def execute(self, input):
           # Implementação baseada no CENÁRIO

4. QA valida automaticamente
   pytest features/checkout.feature
   ✅ CENÁRIO: Compra rápida.....PASSOU

5. Stakeholder confirma
   "Sim! Abandono caiu 20%"

6. Todos falam a mesma língua
   O behavior virou código virou teste virou valor
```

> *"BDD não é apenas testes. É a gramática que o Forge Process adota para que todos — produto, negócio, engenharia e QA — falem a mesma língua."*

---

### 3️⃣ Roadmap Planning — Concepção Técnica

**"QUANDO e COMO o sistema será construído?"**

> **Nota:** Esta é a fase de planejamento executivo que preenche a lacuna entre a especificação de comportamento e a implementação.
>
> **Documentação completa:** `process/execution/roadmap_planning/ROADMAP_PLANNING_PROCESS.md`

#### Propósito
Transformar as especificações BDD em um plano de ação técnico e executável. Esta fase garante que, antes de escrever o código, a equipe tenha um consenso sobre a arquitetura, as dependências e a ordem de implementação.

#### Artefatos Principais
- **`specs/roadmap/ADR.md`**: Registros de Decisões de Arquitetura (Architecture Decision Records).
- **`specs/roadmap/HLD.md` / `LLD.md`**: High-Level e Low-Level Design da solução técnica.
- **`specs/roadmap/ROADMAP.md`**: A visão executiva do plano, com fases e marcos.
- **`specs/roadmap/BACKLOG.md`**: O backlog detalhado e priorizado, pronto para ser consumido pelo time de desenvolvimento nos sprints.

---

### 4️⃣ TDD — Test Driven Development

**"COMO implementar? (com prova)"**

#### Propósito
Transformar comportamentos do BDD em **código testado**. Cada funcionalidade nasce com prova de que funciona.

#### Ciclo TDD (Red-Green-Refactor)

```
1. 🔴 RED: Escrever teste que falha
   ↓
2. 🟢 GREEN: Implementar código mínimo que passa
   ↓
3. 🔵 REFACTOR: Melhorar código mantendo testes verdes
   ↓
   Repetir
```

#### Exemplo: Do BDD ao TDD

**BDD Scenario**:
```gherkin
Scenario: Emissão bem-sucedida de nota fiscal
  Given um pedido válido no valor de R$ 1000,00
  When eu emitir a nota fiscal
  Then o ICMS deve ser R$ 180,00
```

**TDD Test (Red)**:
```python
# tests/unit/test_issue_invoice_usecase.py
import pytest
from forgebase.application.issue_invoice_usecase import IssueInvoiceUseCase

def test_should_calculate_icms_correctly():
    # Arrange
    usecase = IssueInvoiceUseCase()
    order = Order(value=1000.00, uf="SP")  # ICMS SP = 18%

    # Act
    invoice = usecase.execute(IssueInvoiceInput(order=order))

    # Assert
    assert invoice.icms == 180.00  # ❌ FALHA - código não existe ainda
```

**TDD Implementation (Green)**:
```python
# src/forgebase/application/issue_invoice_usecase.py
from forgebase.application.usecase_base import UseCaseBase

class IssueInvoiceUseCase(UseCaseBase[IssueInvoiceInput, IssueInvoiceOutput]):
    """Emitir nota fiscal com cálculo automático de impostos."""

    def execute(self, input_dto: IssueInvoiceInput) -> IssueInvoiceOutput:
        # Validar entrada
        input_dto.validate()

        # Calcular ICMS
        icms_rate = self._get_icms_rate(input_dto.order.uf)
        icms_value = input_dto.order.value * icms_rate

        # Gerar XML
        xml = self._generate_nfe_xml(input_dto.order, icms_value)

        # Registrar log
        self._log_emission(input_dto.order, xml)

        return IssueInvoiceOutput(
            xml=xml,
            icms=icms_value,
            success=True
        )

    def _get_icms_rate(self, uf: str) -> float:
        """Obter alíquota de ICMS por UF."""
        icms_table = {"SP": 0.18, "RJ": 0.20, "MG": 0.18}
        return icms_table.get(uf, 0.17)  # Default 17%
```

**Test passes ✅**

#### Tipos de Testes no Forge

1. **Unit Tests**: Testam UseCases isoladamente
2. **Integration Tests**: Testam UseCases com Repositories reais
3. **Property-Based Tests**: Testam propriedades gerais (Hypothesis)
4. **Contract Tests**: Validam interfaces (Ports)

---

### 5️⃣ CLI — Interface de Execução

**"Executar e observar"**

#### Propósito
Fornecer um **ambiente simbólico de teste** onde UseCases podem ser executados, observados e validados antes de uma interface gráfica.

O CLI não é apenas uma ferramenta de linha de comando, mas um **ambiente de teste** onde:
- Humanos podem testar manualmente
- IA pode explorar comportamentos
- Logs e métricas são coletados
- Debugging é facilitado

#### Exemplo: CLI do ForgeBase

```bash
# Executar UseCase via CLI
forgebase execute IssueInvoiceUseCase \
  --input '{"order_id": "12345", "value": 1000.00, "uf": "SP"}' \
  --output invoice.json \
  --verbose

# Output:
# ⏱️  Starting IssueInvoiceUseCase...
# 📊 Metrics enabled: true
# 🔍 Tracing enabled: true
#
# [DEBUG] Validating input...
# [INFO] Fetching order 12345...
# [INFO] Calculating ICMS for UF=SP (18%)...
# [INFO] ICMS calculated: R$ 180.00
# [INFO] Generating NF-e XML...
# [SUCCESS] Invoice issued successfully!
#
# 📈 Metrics:
#   - Duration: 1.2s
#   - ICMS: R$ 180.00
#   - XML size: 2.5KB
#
# ✅ Output saved to invoice.json
```

#### Capacidades do CLI

1. **Execução Manual**: Testar UseCases sem GUI
2. **Simulação**: Rodar cenários com dados fake
3. **Observação**: Ver logs, métricas, traces em tempo real
4. **Debugging**: Inspecionar estado e fluxo
5. **Automação**: Scripts e CI/CD
6. **Exploração**: IA pode usar CLI para aprender

#### CLI como Ponte entre Humanos e IA

```python
# IA explorando via CLI
from forgebase.dev.api import ComponentDiscovery, TestRunner

# 1. IA descobre componentes
discovery = ComponentDiscovery()
components = discovery.scan_project()
print(f"Found {len(components.usecases)} UseCases")

# 2. IA executa cada UseCase via CLI
for usecase in components.usecases:
    result = subprocess.run([
        "forgebase", "execute", usecase.name,
        "--input", "sample_input.json"
    ])

    # 3. IA analisa resultado
    if result.returncode == 0:
        print(f"✅ {usecase.name} works!")
    else:
        print(f"❌ {usecase.name} failed!")
```

---

### 6️⃣ Feedback — Reflexão

**"Aprender e ajustar"**

#### Propósito
Coletar dados de execução e usá-los para **melhorar o raciocínio** do sistema. Feedback fecha o ciclo cognitivo.

#### Dois Tipos de Feedback

##### 1. Feedback Operacional

**Origem**: Métricas, logs, exceções, performance
**Função**: Melhorar desempenho técnico

```python
# Coleta automática de métricas
@track_metrics
class IssueInvoiceUseCase(UseCaseBase):
    def execute(self, input_dto):
        # Métricas coletadas automaticamente:
        # - Tempo de execução
        # - Taxa de erro
        # - Throughput
        # - Latência de dependências
        ...

# Análise de métricas
metrics = MetricsCollector.get_metrics("IssueInvoiceUseCase")
print(f"Avg duration: {metrics.avg_duration}ms")
print(f"Error rate: {metrics.error_rate}%")
print(f"P95 latency: {metrics.p95_latency}ms")

# IA analisa e sugere melhorias
if metrics.error_rate > 0.05:
    print("⚠️ High error rate detected!")
    print("💡 Suggestion: Add retry logic for SEFAZ calls")
```

##### 2. Feedback de Valor

**Origem**: Stakeholders, usuários, KPIs
**Função**: Ajustar propósito e realinhar valor

```python
# Análise de Value KPIs
value_tracker = ValueKPITracker()

# KPI do MDD: "0 erros em cálculo de impostos"
kpi_result = value_tracker.measure_kpi(
    kpi="Invoice Error Rate",
    usecase="IssueInvoiceUseCase",
    period="last_30_days"
)

print(f"Target: 0%")
print(f"Current: {kpi_result.current_value}%")

if kpi_result.current_value > 0:
    print("❌ KPI não atingido!")

    # Feedback para o MDD: revisar ValueTrack
    feedback = FeedbackReport(
        kpi="Invoice Error Rate",
        target=0.0,
        actual=kpi_result.current_value,
        recommendation="Revisar regras de cálculo de ICMS para casos especiais"
    )

    # Exportar para ForgeProcess
    feedback_manager.export_to_forgeprocess(feedback)
```

#### Feedback Loop Completo

```python
# src/forgebase/observability/feedback_manager.py
class FeedbackManager:
    """Gerencia feedback loops entre ForgeBase e ForgeProcess."""

    def collect_comprehensive_feedback(
        self,
        usecase_name: str,
        time_window: str = "last_7_days"
    ) -> FeedbackReport:
        """Coleta feedback completo de um UseCase."""

        # 1. Métricas operacionais
        metrics = self.metrics_collector.get_metrics(usecase_name, time_window)

        # 2. Logs de erro
        errors = self.log_service.query_errors(usecase_name, time_window)

        # 3. Value KPIs
        kpis = self.value_tracker.measure_all_kpis(usecase_name, time_window)

        # 4. Intent tracking (coerência)
        coherence = self.intent_tracker.measure_coherence(usecase_name, time_window)

        # 5. Análise de IA
        insights = self.ai_analyzer.analyze(metrics, errors, kpis, coherence)

        return FeedbackReport(
            usecase=usecase_name,
            operational_metrics=metrics,
            errors=errors,
            value_kpis=kpis,
            coherence=coherence,
            ai_insights=insights,
            recommendations=self._generate_recommendations(insights)
        )

    def export_to_forgeprocess(self, report: FeedbackReport):
        """Exporta feedback para ForgeProcess aprender."""
        # Salvar em formato estruturado
        learning_data = {
            "usecase": report.usecase,
            "timestamp": datetime.now().isoformat(),
            "metrics": report.operational_metrics.to_dict(),
            "kpis": [kpi.to_dict() for kpi in report.value_kpis],
            "recommendations": report.recommendations
        }

        # Exportar para ForgeProcess
        with open(f"/var/learning/{report.usecase}_feedback.jsonl", "a") as f:
            f.write(json.dumps(learning_data) + "\n")

        # ForgeProcess pode ler e ajustar visao.md ou .feature files
```

---

## 🔄 O Ciclo Completo na Prática

### Exemplo Real: ValueTrack "IssueInvoice"

#### Fase 1: MDD

```markdown
# project/docs/visao.md

### IssueInvoice
**Descrição**: Emitir nota fiscal automaticamente
**Métrica de Valor**: 0 erros em cálculo de impostos
**Stakeholders**: Lojista, Contador
```

#### Fase 2: BDD

```gherkin
# features/issue_invoice.feature
Feature: Emissão de nota fiscal
  Scenario: Cálculo correto de ICMS
    Given um pedido de R$ 1000 em SP
    When emitir nota
    Then ICMS deve ser R$ 180
```

#### Fase 3: TDD

```python
# tests/test_issue_invoice.py
def test_icms_calculation():
    usecase = IssueInvoiceUseCase()
    result = usecase.execute(IssueInvoiceInput(order_value=1000, uf="SP"))
    assert result.icms == 180.00  # ✅
```

#### Fase 4: CLI

```bash
forgebase execute IssueInvoiceUseCase \
  --input '{"order_value": 1000, "uf": "SP"}' \
  --verbose

# ✅ ICMS: R$ 180.00
# ✅ XML generated
# ✅ Duration: 1.2s
```

#### Fase 5: Feedback

```python
# Análise após 30 dias
feedback = feedback_manager.collect_comprehensive_feedback("IssueInvoiceUseCase")

# KPI: 0 erros → ATUAL: 0.1% erros
# Recomendação: Adicionar validação para casos especiais de substituição tributária

# Feedback volta para MDD: Ajustar ValueTrack
# Feedback volta para BDD: Adicionar scenarios para ST
```

---

## 🎯 Benefícios do Ciclo de Raciocínio

### 1. Rastreabilidade Completa

```
Valor (MDD) → Comportamento (BDD) → Código (TDD) → Execução (CLI) → Aprendizado (Feedback)
```

Todo código pode ser rastreado até a intenção de valor original.

### 2. Documentação Viva

- **visao.md** documenta o porquê
- **.feature** documenta o quê
- **Testes** documentam o como
- **Logs** documentam o aconteceu
- **Feedback** documenta o aprendizado

### 3. Evolução Guiada por Valor

O sistema não evolui aleatoriamente, mas guiado por:
- Value KPIs (estamos entregando valor?)
- Operational Metrics (estamos funcionando bem?)
- Coherence Tracking (estamos cumprindo intenções?)

### 4. Ambiente de Execução para IA

IA pode:
- Ler **visao.md** e entender propósito
- Executar **.features** e validar comportamentos
- Analisar **métricas** e sugerir melhorias
- Usar **CLI** para explorar e testar
- Gerar **feedback** para auto-melhoria

---

## 📚 Próximos Passos

### Para Desenvolvedores

1. Leia o **project/docs/visao.md** do seu projeto
2. Entenda os **ValueTracks** (o que entrega valor?)
3. Escreva **.features** para cada ValueTrack
4. Implemente com **TDD** (testes primeiro)
5. Teste via **CLI** (observe e valide)
6. Analise **feedback** (aprenda e melhore)

### Para Agentes de IA

1. Parse **project/docs/visao.md** → Entenda propósito
2. Parse **.features** → Entenda comportamentos
3. Execute via **CLI** → Valide funcionamento
4. Colete **métricas** → Analise performance
5. Gere **feedback** → Sugira melhorias

### Para Product Owners

1. Defina **Value KPIs** claros
2. Acompanhe métricas de valor
3. Use feedback para ajustar roadmap
4. Valide que features entregam valor

---

## 🔗 Documentos Relacionados

### Processos Detalhados
- **process/mdd/MDD_process.md**: Market Driven Development (6 etapas)
- **process/bdd/BDD_PROCESS.md**: Behavior Driven Development (6 subetapas)
- **process/execution/PROCESS.md**: Execution (Roadmap Planning + TDD)
- **process/delivery/PROCESS.md**: Delivery (Sprints + Review & Feedback)

### Templates
- **process/mdd/templates/**: Templates para artefatos MDD (hipótese, visão, sumário, etc)
- **process/bdd/templates/**: Templates para artefatos BDD (features, tracks.yml, steps, etc)

### Especificações
- **specs/bdd/**: Features Gherkin (PT-BR) com estrutura padronizada
- **specs/bdd/tracks.yml**: Mapeamento features → ValueTracks → métricas
- **specs/bdd/HANDOFF.md**: Instruções de handoff BDD → TDD

### Outros Documentos
- **ADR-006**: ForgeProcess Integration (detalhes técnicos)

---

## 📂 Estrutura de Pastas do Processo

```
process/
├── PROCESS.md                    ← Visão geral do processo completo
│
├── mdd/                          ← Market Driven Development
│   ├── MDD_process.md            ← Processo completo (6 etapas)
│   ├── etapa_01.md               ← Concepção da Visão
│   ├── etapa_02.md               ← Síntese Executiva
│   ├── etapa_03.md               ← Pitch de Valor
│   ├── etapa_04.md               ← Validação Pública
│   ├── etapa_05.md               ← Avaliação Estratégica
│   └── templates/                ← Templates MDD
│       ├── template_hipotese.md
│       ├── template_visao.md
│       ├── template_sumario_executivo.md
│       ├── template_pitch_deck.md
│       ├── template_site.md
│       └── ... (outros templates MDD)
│
├── bdd/                          ← Behavior Driven Development
│   ├── BDD_PROCESS.md            ← Processo completo (6 subetapas)
│   ├── etapa_01_mapeamento_comportamentos.md
│   ├── etapa_02_escrita_features.md
│   ├── etapa_03_organizacao_tagging.md
│   ├── etapa_04_tracks_yml.md
│   ├── etapa_05_skeleton_automacao.md
│   ├── etapa_06_handoff_tdd.md
│   └── templates/                ← Templates BDD
│       ├── template_behavior_mapping.md
│       ├── template_feature.md
│       ├── template_tracks.yml
│       ├── template_step_skeleton.py
│       └── README.md
│
├── execution/                    ← Execução (arquitetura + TDD)
│   ├── PROCESS.md                ← Processo de Execution (macro)
│   ├── roadmap_planning/
│   │   └── ROADMAP_PLANNING_PROCESS.md
│   └── tdd/
│       └── TDD_PROCESS.md
│
└── delivery/                     ← Delivery (sprints + reviews)
    ├── PROCESS.md                ← Processo de Delivery (macro)
    ├── sprint/
    │   └── SPRINT_PROCESS.md
    └── review/
        └── REVIEW_PROCESS.md
```

### Artefatos Gerados

```
project/                          ← Artefatos do projeto
└── docs/
    ├── hipotese.md               ← MDD Etapa 1 (entrada)
    ├── visao.md                  ← MDD Etapa 1 (saída)
    ├── sumario_executivo.md      ← MDD Etapa 2
    ├── pitch_deck.md             ← MDD Etapa 3
    ├── sites/                    ← MDD Etapa 4
    └── aprovacao_mvp.md          ← MDD Etapa 5 (decisão)

specs/                            ← Especificações BDD
└── bdd/
    ├── 00_glossario.md           ← Linguagem ubíqua
    ├── tracks.yml                ← Rastreabilidade
    ├── HANDOFF.md                ← Handoff BDD → TDD
    ├── README.md                 ← Guia de uso
    ├── 10_forge_core/            ← Features do SDK
    ├── 20_symclient_http/        ← Features HTTP
    ├── 21_symclient_stdio/       ← Features STDIO
    ├── 30_plugins_provedores/    ← Features de portabilidade
    ├── 40_mcp_tecnospeed/        ← Features MCP
    ├── 41_llm_broker_tecnospeed/ ← Features Broker
    ├── 50_observabilidade/       ← Features observability
    └── 60_seguranca/             ← Features security

tests/                            ← Automação de testes
└── bdd/
    ├── conftest.py               ← Fixtures pytest
    └── test_*_steps.py           ← Step definitions
```

---

## 🌟 A Filosofia Forge: Valor de Negócio, Não Dias de Sprint

### O Que Estamos Realmente Medindo?

O ForgeProcess propõe algo mais profundo que velocidade: **clareza, coerência e confiança**.

```
Metodologia Tradicional           ForgeProcess
═══════════════════════           ════════════

"Entregamos 20 story points"      "Reduzimos abandono em 20%"
"Completamos 15 tasks"            "Garantimos 0 bugs fiscais"
"Sprint concluída em 2 semanas"   "Cliente economizou R$ 50k/mês"
"5 features implementadas"        "5 comportamentos validados"

Mede: ATIVIDADE                   Mede: IMPACTO
```

### Por Que "Unidades de Valor de Negócio"?

**Unidade de Valor de Negócio** = A menor unidade de comportamento que entrega resultado mensurável

Cada unidade de valor é:
1. **Rastreável**: Do visao.md até o código
2. **Verificável**: BDD scenarios automatizados
3. **Mensurável**: KPIs claros de impacto
4. **Valioso**: Cliente percebe diferença

### A Corrente de Valor Verificável

```
MDD (Intenção de Valor)
    ↓
BDD (Comportamento Verificável)
    ↓
TDD (Prova Automatizada)
    ↓
CLI (Observação em Tempo Real)
    ↓
Feedback (Medição de Impacto)
    ↓
Mais Valor (Ciclo Contínuo)
```

Cada elo dessa corrente é **verificável**:
- ✅ Valor definido? (visao.md)
- ✅ Comportamento especificado? (.feature)
- ✅ Código testado? (pytest)
- ✅ Funciona em produção? (CLI + métricas)
- ✅ KPI atingido? (feedback)

### A Simbiose Value ↔ Support

O ForgeProcess estabelece um contrato:

**VALUE TRACKS** entregam impacto
**SUPPORT TRACKS** garantem confiabilidade

```
       VALUE                        SUPPORT
   ┌──────────┐                ┌──────────┐
   │ Checkout │                │ Tests    │
   │ 1-clique │ ←──────────→  │ BDD auto │
   │          │   sustentação  │          │
   │ -20%     │                │ 100%     │
   │ abandono │                │ coverage │
   └──────────┘                └──────────┘
```

Sem VALUE TRACKS, o sistema não tem propósito.
Sem SUPPORT TRACKS, o valor não se sustenta.

### O Renascimento

**Num mundo saturado de entregas rápidas e resultados rasos**, o ForgeProcess propõe:

- 🔄 **Ciclo de raciocínio** em vez de workflow mecânico
- 🎯 **Direção de valor** em vez de velocidade cega
- 🗣️ **Linguagem universal** (BDD) em vez de silos técnicos
- 📊 **Unidades de valor de negócio** em vez de story points
- ✅ **Comportamentos validados** em vez de features "prontas"
- 🔗 **Rastreabilidade completa** do porquê até o código

### O Código se Reconciliando com o Propósito

```
Tradicional:                    ForgeProcess:
"Feature pronta!"              "Valor entregue!"
    ↓                              ↓
Mas funciona?                  Sim, está testado.
    ↓                              ↓
Mas entrega valor?             Sim, KPI mostra.
    ↓                              ↓
Como sabemos?                  Comportamento validado.
    ↓                              ↓
🤷 "Achamos que sim"            ✅ "Temos evidência"
```

---

## 💡 Citações

> *"O código do ForgeBase é o corpo de uma mente que pensa em software."*

> *"O ForgeProcess é o ciclo em que o pensamento se transforma em comportamento, o comportamento em prova, e a prova em aprendizado."*

> *"MDD → BDD: O momento em que estratégia vira função."*

> *"Não importa o quão rápido o time progrida, se estiver indo para o lado errado."*

> *"Cada comportamento de negócio precisa de sustentação técnica — e cada automação técnica deve justificar sua existência pelo valor que possibilita."*

> *"BDD é a gramática que todos — produto, negócio, engenharia e QA — usam para falar a mesma língua."*

> *"O progresso se mede em unidades de valor de negócio, não em dias de sprint."*

> *"É o código se reconciliando com o propósito."*

---

**Author**: ForgeBase Development Team
**Version**: 1.1
**Date**: 2025-11-04
**Updated**: 2025-11-04 - Adicionado conceitos de Tokens de Valor e ValueTracks vs SupportTracks
