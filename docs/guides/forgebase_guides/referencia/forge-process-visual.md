# ForgeProcess: Guia Visual Completo

**Aprenda o ciclo cognitivo através de diagramas, exemplos e visualizações práticas.**

---

## 🎨 Índice Visual

1. [O Ciclo Completo (Diagrama Macro)](#ciclo-completo)
2. [Fase 1: MDD (Market Driven)](#fase-1-mdd)
3. [Transição Crítica: MDD → BDD](#transição-mdd-bdd)
4. [Fase 2: BDD (Behavior Driven)](#fase-2-bdd)
5. [Fase 3: TDD (Test Driven)](#fase-3-tdd)
6. [Fase 4: CLI (Interface Cognitiva)](#fase-4-cli)
7. [Fase 5: Feedback (Reflexão)](#fase-5-feedback)
8. [Exemplo Completo: Do Valor ao Feedback](#exemplo-completo)

---

<a name="ciclo-completo"></a>
## 🔄 O Ciclo Completo (Diagrama Macro)

```
                          FORGE PROCESS
                     ═══════════════════════

┌─────────────────────────────────────────────────────┐
│                                                     │
│  Fase 1: MDD (Market Driven Development)           │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━         │
│  PERGUNTA: "PORQUÊ este sistema deve existir?"     │
│                                                     │
│  Artefato: forge.yaml                               │
│  Output: ValueTracks, Value KPIs                    │
│                                                     │
│  Exemplo:                                           │
│    ValueTrack: "ProcessOrder"                       │
│    KPI: "< 2 minutos por pedido"                    │
│                                                     │
└──────────────────────┬──────────────────────────────┘
                       │
                       │ TRADUÇÃO COGNITIVA
                       │ (Valor → Comportamento)
                       ▼
┌─────────────────────────────────────────────────────┐
│                                                     │
│  Fase 2: BDD (Behavior Driven Development)         │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━         │
│  PERGUNTA: "O QUÊ o sistema faz?"                   │
│                                                     │
│  Artefato: process_order.feature                    │
│  Output: Scenarios (Given/When/Then)                │
│                                                     │
│  Exemplo:                                           │
│    Given um pedido válido                           │
│    When eu processar                                │
│    Then deve concluir em < 2 min                    │
│                                                     │
└──────────────────────┬──────────────────────────────┘
                       │
                       │ ESPECIFICAÇÃO TÉCNICA
                       ▼
┌─────────────────────────────────────────────────────┐
│                                                     │
│  Fase 3: TDD (Test Driven Development)             │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━         │
│  PERGUNTA: "COMO implementar? (com prova)"         │
│                                                     │
│  Artefato: test_process_order.py                    │
│  Output: Código testado                             │
│                                                     │
│  Exemplo:                                           │
│    def test_should_process_in_2_minutes():          │
│        # Red → Green → Refactor                     │
│                                                     │
└──────────────────────┬──────────────────────────────┘
                       │
                       │ MANIFESTAÇÃO EXECUTÁVEL
                       ▼
┌─────────────────────────────────────────────────────┐
│                                                     │
│  Fase 4: CLI (Interface Cognitiva)                 │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━         │
│  PERGUNTA: "Executar e observar?"                   │
│                                                     │
│  Artefato: forgebase CLI                            │
│  Output: Logs, Métricas, Traces                     │
│                                                     │
│  Exemplo:                                           │
│    $ forgebase execute ProcessOrder                 │
│    ⏱️  Duration: 1.8 minutes ✅                      │
│                                                     │
└──────────────────────┬──────────────────────────────┘
                       │
                       │ COLETA DE EVIDÊNCIAS
                       ▼
┌─────────────────────────────────────────────────────┐
│                                                     │
│  Fase 5: Feedback (Reflexão)                       │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━         │
│  PERGUNTA: "Aprender e ajustar?"                    │
│                                                     │
│  Artefato: feedback_report.jsonl                    │
│  Output: Insights, Recommendations                  │
│                                                     │
│  Exemplo:                                           │
│    KPI Target: < 2 min                              │
│    Actual: 1.8 min (✅ Cumprido!)                   │
│    Recommendation: Manter estratégia                │
│                                                     │
└──────────────────────┬──────────────────────────────┘
                       │
                       │ LOOP DE APRENDIZADO
                       └──────────────────┐
                                          │
                  ┌───────────────────────┘
                  ▼
         Volta para MDD
       (Ajusta forge.yaml)
```

---

<a name="fase-1-mdd"></a>
## 📊 Fase 1: MDD (Market Driven Development)

### Diagrama de Artefatos

```
forge.yaml
├── project
│   ├── name
│   ├── vision
│   └── value_proposition
│
├── value_tracks                  ← Fluxos que entregam valor
│   ├── ProcessOrder
│   │   ├── description
│   │   ├── value_metric
│   │   └── stakeholders
│   │
│   └── IssueInvoice
│       ├── description
│       ├── value_metric
│       └── stakeholders
│
├── support_tracks                ← Fluxos de suporte
│   ├── ManageInventory
│   └── CalculateTaxes
│
└── kpis                          ← Métricas de valor
    ├── Order Processing Time
    └── Invoice Error Rate
```

### Exemplo Completo: forge.yaml

```yaml
# forge.yaml
project:
  name: "EcommerceSystem"
  vision: "Facilitar vendas online com agilidade e segurança"
  value_proposition:
    - "Processar pedidos 50% mais rápido"
    - "Zero erros em notas fiscais"
    - "Rastreamento em tempo real"

value_tracks:
  - name: "ProcessOrder"
    description: "Processar pedido do início ao fim"
    value_metric: "Tempo médio < 2 minutos"
    stakeholders:
      - "Vendedor"
      - "Cliente"
    business_value: "Aumenta conversão e satisfação"

  - name: "IssueInvoice"
    description: "Emitir nota fiscal automaticamente"
    value_metric: "0% de erros em cálculo"
    stakeholders:
      - "Vendedor"
      - "Contador"
    business_value: "Evita multas fiscais"

support_tracks:
  - name: "ManageInventory"
    description: "Controlar estoque"
    supports: ["ProcessOrder"]

  - name: "CalculateTaxes"
    description: "Calcular impostos"
    supports: ["IssueInvoice"]

kpis:
  - metric: "Order Processing Time"
    target: "< 2 minutes"
    current: "4.5 minutes"
    priority: "critical"

  - metric: "Invoice Error Rate"
    target: "0%"
    current: "3.2%"
    priority: "high"
```

### Visualização: ValueTracks vs SupportTracks

```
VALUE TRACKS                SUPPORT TRACKS
(Entregam valor direto)     (Suportam value tracks)

┌─────────────────┐         ┌─────────────────┐
│  ProcessOrder   │◄────────│ ManageInventory │
│  (VALUE)        │         │  (SUPPORT)      │
└─────────────────┘         └─────────────────┘
        │
        │ usa
        ▼
┌─────────────────┐         ┌─────────────────┐
│  IssueInvoice   │◄────────│  CalculateTaxes │
│  (VALUE)        │         │  (SUPPORT)      │
└─────────────────┘         └─────────────────┘
```

---

<a name="transição-mdd-bdd"></a>
## 🔀 Transição Crítica: MDD → BDD

**O momento onde pensamento abstrato vira ação concreta.**

### Visualização da Tradução

```
MDD (Abstrato)                    BDD (Concreto)
══════════════                    ══════════════

ValueTrack:                       Feature:
"ProcessOrder"        ─────────>  "Processar pedido completo"
                     tradução
                                  Scenario:
Value Metric:                     "Dado pedido válido"
"< 2 minutos"         ─────────>  "When processar"
                     especifica   "Then concluir < 2 min"

Stakeholder:                      Actor:
"Vendedor"            ─────────>  "Como um vendedor"
                     personifica

Business Value:                   Acceptance Criteria:
"Aumenta conversão"   ─────────>  "Pedido processado com sucesso"
                     verifica     "Tempo registrado em métrica"
```

### Exemplo Lado a Lado

#### MDD (forge.yaml)
```yaml
value_tracks:
  - name: "CreateUser"
    description: "Cadastro rápido e seguro"
    value_metric: "95% completam em < 30s"
    stakeholders: ["Novo usuário"]
```

#### BDD (.feature)
```gherkin
Feature: Cadastro rápido e seguro de usuários
  Para que novos usuários comecem rápido
  Como um visitante
  Eu quero me cadastrar facilmente

  Scenario: Cadastro bem-sucedido
    Given que estou na página de cadastro
    And preencho dados válidos
    When clico em "Criar conta"
    Then minha conta deve ser criada
    And o processo deve durar < 30 segundos
    And devo receber email de confirmação
```

#### Mapeamento Completo

| MDD | → | BDD |
|-----|---|-----|
| ValueTrack name | → | Feature title |
| description | → | Feature description |
| value_metric | → | Acceptance criteria (Then steps) |
| stakeholders | → | Actors (Como um...) |
| business_value | → | Para que... (benefit) |

---

<a name="fase-2-bdd"></a>
## 🎭 Fase 2: BDD (Behavior Driven Development)

### Anatomia de um Feature File

```
┌────────────────────────────────────────────────────┐
│ Feature: [Título do comportamento]                 │  ← O QUÊ
│   [Narrativa em 3 linhas]                          │
│   Para que [benefício]                             │  ← PORQUÊ
│   Como um [ator]                                   │  ← QUEM
│   Eu quero [ação]                                  │  ← O QUÊ
├────────────────────────────────────────────────────┤
│ Background:                                        │  ← Contexto comum
│   Given [pré-condição comum]                       │
├────────────────────────────────────────────────────┤
│ Scenario: [Caso específico]                        │  ← Exemplo concreto
│   Given [contexto]                                 │  ← Estado inicial
│   And [mais contexto]                              │
│   When [ação]                                      │  ← Ação do usuário
│   Then [resultado esperado]                        │  ← Comportamento
│   And [verificação adicional]                      │  ← Mais verificações
├────────────────────────────────────────────────────┤
│ Business Rules:                                    │  ← Regras documentadas
│   - [Regra 1]                                      │
│   - [Regra 2]                                      │
└────────────────────────────────────────────────────┘
```

### Exemplo Visual: IssueInvoice

```gherkin
┌─────────────────────────────────────────────────────┐
│ Feature: Emissão de nota fiscal                     │
│   Para que lojistas possam faturar vendas           │
│   Como um sistema de gestão                         │
│   Eu devo emitir notas automaticamente              │
├─────────────────────────────────────────────────────┤
│ Background:                                         │
│   Given sistema configurado para NF-e              │
│   And credenciais SEFAZ válidas                     │
├─────────────────────────────────────────────────────┤
│ Scenario: Emissão bem-sucedida                      │
│                                                     │
│   ┌─────────────────────────────────────┐          │
│   │ GIVEN (Estado inicial)              │          │
│   │  - Pedido válido R$ 1000            │          │
│   │  - Cliente com CPF                  │          │
│   │  - Produto tributável               │          │
│   └─────────────────────────────────────┘          │
│                ↓                                    │
│   ┌─────────────────────────────────────┐          │
│   │ WHEN (Ação)                         │          │
│   │  - Emitir nota fiscal               │          │
│   └─────────────────────────────────────┘          │
│                ↓                                    │
│   ┌─────────────────────────────────────┐          │
│   │ THEN (Resultado esperado)           │          │
│   │  ✅ ICMS = R$ 180 (18%)             │          │
│   │  ✅ XML gerado                      │          │
│   │  ✅ Log registrado                  │          │
│   │  ✅ Enviado para SEFAZ              │          │
│   │  ✅ DANFE enviado por email         │          │
│   └─────────────────────────────────────┘          │
├─────────────────────────────────────────────────────┤
│ Business Rules:                                     │
│   1. Produtos devem ter NCM válido                  │
│   2. ICMS conforme tabela da UF                     │
│   3. Numeração sequencial obrigatória               │
│   4. Retry automático em falhas (3x)                │
└─────────────────────────────────────────────────────┘
```

---

<a name="fase-3-tdd"></a>
## 🧪 Fase 3: TDD (Test Driven Development)

### Ciclo Red-Green-Refactor

```
Fase RED (Teste falha)
┌────────────────────────────────┐
│ def test_icms_calculation():   │
│     usecase = IssueInvoice()   │
│     result = usecase.execute(  │
│         order_value=1000,      │
│         uf="SP"                │
│     )                          │
│     assert result.icms == 180  │  ← ❌ FALHA
│                                │     (código não existe)
└────────────────────────────────┘
            ↓
Fase GREEN (Código mínimo)
┌────────────────────────────────┐
│ class IssueInvoiceUseCase:     │
│     def execute(self, input):  │
│         icms = input.value *   │
│                0.18            │
│         return Output(         │
│             icms=icms          │
│         )                      │  ← ✅ PASSA
└────────────────────────────────┘
            ↓
Fase REFACTOR (Melhoria)
┌────────────────────────────────┐
│ class IssueInvoiceUseCase:     │
│     ICMS_TABLE = {             │
│         "SP": 0.18,            │
│         "RJ": 0.20             │
│     }                          │
│                                │
│     def execute(self, input):  │
│         rate = self.ICMS_TABLE │
│                 [input.uf]     │
│         icms = input.value *   │
│                rate            │
│         return Output(         │
│             icms=icms          │
│         )                      │  ← ✅ PASSA (melhorado)
└────────────────────────────────┘
```

### Mapeamento BDD → TDD

```
BDD Scenario                          TDD Test
════════════════                      ═════════

Given um pedido de R$ 1000            order = Order(value=1000, uf="SP")
When emitir nota                      result = usecase.execute(order)
Then ICMS deve ser R$ 180             assert result.icms == 180.00


BDD Scenario                          TDD Test
════════════════                      ═════════

Given produto sem NCM                 product = Product(ncm=None)
When tentar emitir nota               with pytest.raises(ValidationError):
Then deve rejeitar                        usecase.execute(product)
```

### Pirâmide de Testes ForgeBase

```
                    ▲
                   ╱ ╲
                  ╱   ╲
                 ╱  E2E ╲           ← 10% (poucos, lentos)
                ╱ (CLI)  ╲
               ╱───────────╲
              ╱             ╲
             ╱  Integration  ╲      ← 20% (médios)
            ╱  (Repositories) ╲
           ╱───────────────────╲
          ╱                     ╲
         ╱      Unit Tests       ╲  ← 70% (muitos, rápidos)
        ╱     (UseCases)          ╲
       ╱───────────────────────────╲
```

---

<a name="fase-4-cli"></a>
## 💻 Fase 4: CLI (Interface Cognitiva)

### Fluxo de Execução via CLI

```
Terminal                  CLI               ForgeBase
════════                  ═══               ═════════

$ forgebase execute  ─────>  Parse command
  IssueInvoiceUseCase         │
  --input data.json           │
  --verbose                   ▼
                          Load UseCase
                              │
                              ▼
                          Inject dependencies
                              │
                              ▼
                          Enable metrics  ────> MetricsCollector
                              │
                              ▼
                          Enable tracing  ────> TracingService
                              │
                              ▼
                          Execute  ──────────> UseCase.execute()
                              │                      │
                              │                      ▼
                          Collect output        Business logic
                              │                      │
                              ◄──────────────────────┘
                              │
                              ▼
                          Format output
                              │
                              ▼
◄─────────────────────  Display results
📊 Metrics:
   Duration: 1.2s
   ICMS: R$ 180
✅ Success
```

### Exemplo de Output CLI

```bash
$ forgebase execute IssueInvoiceUseCase \
    --input '{"order_value": 1000, "uf": "SP"}' \
    --verbose

╔═══════════════════════════════════════════════════╗
║  ForgeBase CLI - UseCase Execution                ║
╚═══════════════════════════════════════════════════╝

⏱️  Starting IssueInvoiceUseCase...
📊 Observability enabled
🔍 Tracing ID: exec-abc123

┌─────────────────────────────────────────────────┐
│ PHASE 1: Validation                             │
└─────────────────────────────────────────────────┘
  [DEBUG] Validating input DTO...
  [INFO]  Input valid ✅

┌─────────────────────────────────────────────────┐
│ PHASE 2: Business Logic                         │
└─────────────────────────────────────────────────┘
  [INFO]  Fetching ICMS rate for UF=SP...
  [INFO]  ICMS rate: 18%
  [INFO]  Calculating ICMS...
  [INFO]  ICMS: R$ 180.00 ✅

┌─────────────────────────────────────────────────┐
│ PHASE 3: Side Effects                           │
└─────────────────────────────────────────────────┘
  [INFO]  Generating NF-e XML...
  [INFO]  XML size: 2.5KB ✅
  [INFO]  Logging emission...
  [INFO]  Log saved ✅

┌─────────────────────────────────────────────────┐
│ RESULT                                          │
└─────────────────────────────────────────────────┘
  {
    "success": true,
    "invoice_id": "nfe-12345",
    "icms": 180.00,
    "xml_size_kb": 2.5,
    "duration_ms": 1247
  }

📈 METRICS
  Duration: 1.247s
  Success: true
  ICMS calculated: R$ 180.00

✅ Execution completed successfully!
```

---

<a name="fase-5-feedback"></a>
## 📈 Fase 5: Feedback (Reflexão)

### Dois Tipos de Feedback

```
┌────────────────────────────────────────────────────┐
│ FEEDBACK OPERACIONAL                               │
│ (Métricas técnicas)                                │
├────────────────────────────────────────────────────┤
│                                                    │
│  Fonte: Logs, Métricas, Traces                     │
│                                                    │
│  Exemplo:                                          │
│  - Duration: 1.2s (target: < 2s) ✅               │
│  - Error rate: 0.1% (target: 0%) ⚠️               │
│  - Throughput: 100 req/s                           │
│  - P95 latency: 1.8s                               │
│                                                    │
│  Ação:                                             │
│  → Adicionar retry logic                           │
│  → Otimizar cálculo de ICMS                        │
│                                                    │
└────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────┐
│ FEEDBACK DE VALOR                                  │
│ (Validação de negócio)                             │
├────────────────────────────────────────────────────┤
│                                                    │
│  Fonte: Stakeholders, KPIs, Usuários               │
│                                                    │
│  Exemplo:                                          │
│  - KPI Target: 0% erros                            │
│  - KPI Actual: 0.1% erros ⚠️                       │
│  - User feedback: "Cálculo demora muito"           │
│                                                    │
│  Ação:                                             │
│  → Revisar regras de cálculo                       │
│  → Ajustar ValueTrack no MDD                       │
│  → Adicionar scenario no BDD                       │
│                                                    │
└────────────────────────────────────────────────────┘
```

### Fluxo de Feedback Completo

```
Execução (CLI)
      ↓
┌─────────────────┐
│ Collect Metrics │
│  - Duration     │
│  - Errors       │
│  - Success rate │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Analyze KPIs   │
│  - Target met?  │
│  - Trends       │
│  - Anomalies    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Generate Report │
│  - Operational  │
│  - Business     │
│  - Recommendations │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Export Learning │
│  Data (JSONL)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  ForgeProcess   │
│  - Read feedback │
│  - Adjust MDD   │
│  - Refine BDD   │
└─────────────────┘
```

---

<a name="exemplo-completo"></a>
## 🎬 Exemplo Completo: Do Valor ao Feedback

### Visualização End-to-End

```
SEMANA 1: MDD
─────────────
📝 forge.yaml criado
   ValueTrack: "IssueInvoice"
   KPI: "0% erros em cálculo"
   ↓
─────────────────────────────────────

SEMANA 2: BDD
─────────────
📄 issue_invoice.feature criado
   Scenario: Cálculo correto de ICMS
   Given pedido R$ 1000 em SP
   Then ICMS deve ser R$ 180
   ↓
─────────────────────────────────────

SEMANA 3: TDD
─────────────
🧪 test_issue_invoice.py criado
   ❌ RED: Teste falha
   ✅ GREEN: Código passa
   🔵 REFACTOR: Código melhorado
   ↓
─────────────────────────────────────

SEMANA 4: CLI
─────────────
💻 Teste manual via CLI
   $ forgebase execute IssueInvoice
   ✅ ICMS: R$ 180 (correto!)
   ⏱️  Duration: 1.2s
   ↓
─────────────────────────────────────

SEMANA 5-8: PRODUÇÃO
────────────────────
🚀 Sistema em produção
   1000 notas emitidas
   3 erros encontrados (0.3%)
   ↓
─────────────────────────────────────

SEMANA 9: FEEDBACK
──────────────────
📊 Análise de feedback
   KPI Target: 0% erros
   KPI Actual: 0.3% erros ⚠️

   Causa: Casos especiais de
          substituição tributária

   Recomendação:
   - Adicionar regra no MDD
   - Adicionar scenario no BDD
   - Implementar com TDD
   ↓
─────────────────────────────────────

SEMANA 10: AJUSTE
─────────────────
🔄 Ciclo reinicia
   forge.yaml atualizado
   Nova feature adicionada
   Testes expandidos
   ↓
─────────────────────────────────────

RESULTADO: MELHORIA CONTÍNUA
────────────────────────────
✅ Sistema aprende com erros
✅ Documentação sempre atualizada
✅ Qualidade aumenta continuamente
```

### Timeline Visual

```
Tempo │
═════════════════════════════════════════════════════
      │
S1-2  │ ███ MDD + BDD (Especificação)
      │
S3    │     ███ TDD (Implementação)
      │
S4    │         ██ CLI (Validação)
      │
S5-8  │            ████████████ Produção
      │
S9    │                        ███ Feedback
      │
S10+  │                           ████ Ciclo 2
      │                               (MDD → BDD → ...)
      │
      └────────────────────────────────────────────>
```

---

## 🎯 Checklist: Como Saber Se Você Está Usando ForgeProcess Corretamente

### ✅ MDD
- [ ] Tem forge.yaml com ValueTracks definidos?
- [ ] Cada ValueTrack tem um Value KPI mensurável?
- [ ] Stakeholders estão identificados?
- [ ] Você sabe explicar PORQUÊ o sistema existe?

### ✅ BDD
- [ ] Cada ValueTrack tem um .feature file?
- [ ] Scenarios usam Given/When/Then?
- [ ] Business rules estão documentadas?
- [ ] Qualquer stakeholder pode ler e entender?

### ✅ TDD
- [ ] Cada Scenario tem testes automatizados?
- [ ] Você escreve teste ANTES do código?
- [ ] Ciclo Red-Green-Refactor é seguido?
- [ ] Cobertura > 90%?

### ✅ CLI
- [ ] UseCases podem ser executados via CLI?
- [ ] Logs e métricas são coletados?
- [ ] IA pode explorar behaviors via CLI?
- [ ] Debugging é fácil?

### ✅ Feedback
- [ ] Métricas operacionais são coletadas?
- [ ] Value KPIs são medidos regularmente?
- [ ] Feedback volta para MDD e BDD?
- [ ] Sistema melhora continuamente?

---

## 📚 Próximos Passos

1. **Leia o documento completo**: [docs/FORGE_PROCESS.md](FORGE_PROCESS.md)
2. **Veja a integração técnica**: [docs/adr/006-forgeprocess-integration.md](adr/006-forgeprocess-integration.md)
3. **Experimente**: Crie seu primeiro forge.yaml
4. **Pratique**: Escreva uma .feature para um ValueTrack
5. **Implemente**: Use TDD para desenvolver
6. **Observe**: Execute via CLI e colete feedback

---

**Autor**: ForgeBase Development Team
**Data**: 2025-11-04
**Versão**: 1.0

> *"Um diagrama vale mais que mil palavras. Mil execuções valem mais que um diagrama."*
