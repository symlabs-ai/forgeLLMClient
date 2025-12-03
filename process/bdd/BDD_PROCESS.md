# 🧩 Behavior Driven Development (BDD Process)

**O raciocínio que transforma valor validado em especificação executável.**

---

## 🌟 Visão Geral

O **BDD Process** é a ponte entre **mercado** e **código**. Ele transforma o aprendizado validado no ciclo MDD em uma especificação executável que guia o desenvolvimento com clareza e rastreabilidade.

```
MDD (Valor Validado) → BDD (Comportamento Especificado) → TDD (Código Testado)
        ↓                          ↓                              ↓
   visao.md                specs/bdd/*.feature              src/forge/*
   "PORQUÊ"                "O QUÊ fazer"                    "COMO implementar"
   (project/docs/)         (Gherkin PT-BR)                  (Python)
```

---

## 🎯 Propósito do BDD Process

**Não é** criar testes. **É** estabelecer um **contrato de comportamento** entre:
- Stakeholders (o que o sistema deve fazer)
- Produto (como validar que está correto)
- Desenvolvimento (o que implementar)
- QA (o que verificar)

**Todos falam a mesma língua: Gherkin.**

---

## 📖 As Seis Subetapas do BDD Process

```
┌─────────────────────────────────────────────────────────┐
│ 1. Mapeamento de Comportamentos                        │
│    "Derivar behaviors dos ValueTracks do MDD"           │
└────────────────┬────────────────────────────────────────┘
                 │ Tradução: Valor → Comportamento
                 ▼
┌─────────────────────────────────────────────────────────┐
│ 2. Escrita de Features Gherkin                         │
│    "Especificar comportamentos em linguagem natural"    │
└────────────────┬────────────────────────────────────────┘
                 │ Estruturação
                 ▼
┌─────────────────────────────────────────────────────────┐
│ 3. Organização e Tagging                               │
│    "Estruturar specs/bdd/ com tags de execução"        │
└────────────────┬────────────────────────────────────────┘
                 │ Rastreabilidade
                 ▼
┌─────────────────────────────────────────────────────────┐
│ 4. Criação de tracks.yml                               │
│    "Mapear features → ValueTracks + métricas"          │
└────────────────┬────────────────────────────────────────┘
                 │ Preparação para Automação
                 ▼
┌─────────────────────────────────────────────────────────┐
│ 5. Skeleton de Automação                               │
│    "Criar step definitions vazias (pytest-bdd)"         │
└────────────────┬────────────────────────────────────────┘
                 │ Entrega
                 ▼
┌─────────────────────────────────────────────────────────┐
│ 6. Handoff para TDD                                    │
│    "Documentar e entregar especificação para DEV"       │
└─────────────────────────────────────────────────────────┘
```

---

## 🗂️ Estrutura de Saída Esperada

> **Estrutura alvo em projetos ForgeProcess**
> Os caminhos abaixo descrevem **como um projeto que adota o ForgeProcess deve ser organizado**.
> Este repositório não contém essas pastas finais (`specs/`, `tests/` etc.); elas serão criadas em um
> projeto real (por exemplo, via `symforge init -p forgeprocess myproject`).

Ao final do BDD Process, um projeto típico terá:

```
specs/
 └── bdd/
      ├── 00_glossario.md                    ← Linguagem ubíqua
      ├── README.md                          ← Guia de uso
      ├── HANDOFF.md                         ← Instruções para DEV
      ├── tracks.yml                         ← Mapeamento Tracks
      ├── pull_request_template.md           ← Template de PR
      │
      ├── 10_forge_core/                     ← Núcleo do SDK
      │    ├── chat.feature
      │    ├── sessao.feature
      │    ├── config.feature
      │    └── streaming.feature
      │
      ├── 20_symclient_http/                 ← Servidor HTTP
      │    ├── chat_http.feature
      │    └── errors.feature
      │
      ├── 21_symclient_stdio/                ← Servidor STDIO
      │    ├── ping_chat.feature
      │    └── errors.feature
      │
      ├── 30_plugins_provedores/             ← Portabilidade
      │    └── tool_calling_fallback.feature
      │
      ├── 40_mcp_tecnospeed/                 ← Integrações VALUE
      │    └── marketplace.feature
      │
      ├── 41_llm_broker_tecnospeed/
      │    └── routing.feature
      │
      ├── 50_observabilidade/                ← Qualidade SUPPORT
      │    └── logs_metrics.feature
      │
      └── 60_seguranca/
           └── redaction.feature

tests/
 └── bdd/
      ├── conftest.py                        ← Fixtures pytest
      └── test_*_steps.py                    ← Step definitions (skeleton)
```

---

## 📋 Subetapas Detalhadas

### 🔹 Subetapa 1: Mapeamento de Comportamentos

**📥 Entrada:**
- `docs/visao.md` (A visão do produto)
- `docs/aprovacao_mvp.md` (Aprovação formal do MVP e aprendizados)

**📤 Saída:**
- `specs/bdd/drafts/behavior_mapping.md` (rascunho)

**🎯 Objetivo:**
Derivar comportamentos concretos dos ValueTracks definidos no MDD.

**Como fazer:**
1. Liste todos os ValueTracks do `visao.md`
2. Para cada Track, pergunte:
   - Quais **ações** o usuário executa?
   - Quais **resultados** ele espera ver?
   - Quais **erros** podem ocorrer?
3. Agrupe comportamentos por **domínio** (Forge SDK, SymClient HTTP, SymClient STDIO, etc.)

**Exemplo:**

| ValueTrack (MDD) | Comportamentos Derivados (BDD) |
|------------------|--------------------------------|
| "Chat básico com provedor único" | • Enviar mensagem e receber resposta<br>• Configurar provedor antes de usar<br>• Lidar com erro se provedor inválido |
| "Gestão de contexto por sessão" | • Criar sessão com session_id<br>• Preservar histórico na mesma sessão<br>• Isolar contextos entre sessões diferentes |

**📄 Template:** `process/bdd/templates/template_behavior_mapping.md`

---

### 🔹 Subetapa 2: Escrita de Features Gherkin

**📥 Entrada:**
- `process/bdd/docs/behavior_mapping.md`

**📤 Saída:**
- `specs/bdd/**/*.feature` (arquivos Gherkin)

**🎯 Objetivo:**
Escrever especificações em linguagem natural (Gherkin PT-BR) que todos entendam.

**Padrão Forge:**
```gherkin
@tag_dominio @tag_capacidade @tag_ci
FUNCIONALIDADE: Título descritivo
  PARA [benefício]
  COMO [ator]
  QUERO [ação]

  CONTEXTO:
    DADO [pré-condição comum]

  CENÁRIO: Caso de sucesso
    DADO [pré-condição específica]
    QUANDO [ação]
    ENTÃO [resultado esperado]
    E [efeito colateral observável]

  CENÁRIO: Caso de erro
    DADO [contexto de erro]
    QUANDO [ação que causa erro]
    ENTÃO [tratamento de erro esperado]
```

**Regras de ouro:**
- ✅ **UM comportamento por cenário** (não misture múltiplas validações)
- ✅ **Linguagem de negócio** (não detalhes técnicos como "chamar método X")
- ✅ **Observável** (resultado deve ser verificável externamente)
- ✅ **Curto** (máximo 5-7 steps por cenário)
- ❌ **Não inclua marketing** (nada de sites, CTAs, validações de mercado)

**📄 Template:** `process/bdd/templates/template_feature.md`

---

### 🔹 Subetapa 3: Organização e Tagging

**📥 Entrada:**
- `specs/bdd/**/*.feature` (recém-criadas)

**📤 Saída:**
- Features organizadas por pasta
- Tags aplicadas consistentemente
- `specs/bdd/README.md` atualizado

**🎯 Objetivo:**
Estruturar features para facilitar navegação, execução seletiva e CI.

**Convenções de pasta:**

| Prefixo | Domínio | Tipo | Exemplos |
|---------|---------|------|----------|
| `10_*` | Forge Core (SDK) | VALUE/SUPPORT | chat, sessao, streaming |
| `20_*` | SymClient HTTP | VALUE/SUPPORT | endpoints, errors |
| `21_*` | SymClient STDIO | VALUE/SUPPORT | json-rpc, ping |
| `30_*` | Plugins/Provedores | SUPPORT | fallbacks, capacidades |
| `40_*` | Integrações Externas | VALUE | MCP, Broker |
| `50_*` | Observabilidade | SUPPORT | logs, métricas |
| `60_*` | Segurança | SUPPORT | redaction, auth |

**Sistema de Tags:**

```gherkin
@sdk              # Forge SDK Python
@server           # SymClient (HTTP ou STDIO)
@http             # Protocolo HTTP
@stdio            # Protocolo STDIO/JSON-RPC

@contexto         # Gestão de sessão/contexto
@streaming        # Respostas em stream
@capability:*     # Capacidades específicas (tool_calling, etc)
@fallback         # Comportamentos de fallback

@mcp              # Integração MCP
@broker           # Roteamento via broker

@ci-fast          # CI rápido (mocks/stubs, sem deps externas)
@ci-int           # CI integração (provedores locais, deps internas)
@e2e              # E2E (ambiente controlado, deps externas)
```

**Exemplo de uso:**
```gherkin
@sdk @contexto @ci-fast
FUNCIONALIDADE: Preservar histórico por sessão
  ...
```

---

### 🔹 Subetapa 4: Criação de tracks.yml

**📥 Entrada:**
- `specs/bdd/**/*.feature` (organizadas)
- `project/docs/visao.md` (ValueTracks originais)

**📤 Saída:**
- `specs/bdd/tracks.yml`

**🎯 Objetivo:**
Estabelecer rastreabilidade entre:
- Features BDD ↔ ValueTracks do MDD
- Comportamentos ↔ Métricas de sucesso
- Cenários ↔ Unidades de valor de negócio

**Estrutura do tracks.yml:**

```yaml
tracks:
  - id: value_forge_baseline
    type: VALUE
    name: "Chat básico (Forge SDK)"
    owner: "Time de Produto"
    metrics:
      - adocao_dev           # nº de projetos usando
      - tempo_integracao     # tempo para primeiro chat funcionar
    features:
      - specs/bdd/10_forge_core/chat.feature
      - specs/bdd/10_forge_core/config.feature

  - id: support_context_session
    type: SUPPORT
    name: "Gestão de contexto e sessões"
    owner: "Time de Engenharia"
    metrics:
      - confiabilidade       # % de sessões preservadas corretamente
      - consistencia         # ausência de vazamento entre sessões
    features:
      - specs/bdd/10_forge_core/sessao.feature
```

**Rastreabilidade:**
- Cada **feature** deve estar mapeada em pelo menos **1 track**
- Cada **track** deve ter métricas claras
- PRs devem referenciar: `Track ID` + `Feature` + `Unidade de valor de negócio` (cenário implementado)

**📄 Template:** `process/bdd/templates/template_tracks.yml`

---

### 🔹 Subetapa 5: Skeleton de Automação

**📥 Entrada:**
- `specs/bdd/**/*.feature` (finalizadas)

**📤 Saída:**
- `tests/bdd/test_*_steps.py` (step definitions vazias)
- `tests/bdd/conftest.py` (fixtures pytest)
- `pytest.ini` (configuração de marcadores)

**🎯 Objetivo:**
Preparar infraestrutura de testes para que TDD possa começar imediatamente.

**Estrutura de um step file:**

```python
# tests/bdd/test_forge_chat_steps.py
import pytest
from pytest_bdd import scenarios, given, when, then, parsers

# Marcar como skip até implementação
pytestmark = pytest.mark.skip("BDD: Forge chat pendente de implementação")

# Vincular feature
scenarios("../../specs/bdd/10_forge_core/chat.feature")

# Step definitions (vazias por enquanto)
@given('que o Forge está configurado com o provedor "echo"', target_fixture="forge_client")
def forge_with_echo():
    # TODO: Implementar no TDD
    pytest.skip("Aguardando implementação")

@when(parsers.parse('envio a mensagem "{message}"'), target_fixture="response")
def send_message(forge_client, message):
    # TODO: Implementar no TDD
    pytest.skip("Aguardando implementação")

@then(parsers.parse('recebo uma resposta contendo "{text}"'))
def check_response(response, text):
    # TODO: Implementar no TDD
    pytest.skip("Aguardando implementação")
```

**Fixtures base (conftest.py):**

```python
# tests/bdd/conftest.py
import pytest

@pytest.fixture
def context():
    """Contexto compartilhado entre steps."""
    return {}

@pytest.fixture
def forge_config():
    """Configuração padrão do Forge para testes."""
    return {
        "provider": "echo",
        "timeout": 30
    }
```

**pytest.ini:**

```ini
[pytest]
markers =
    ci_fast: Testes rápidos (mocks, sem deps externas)
    ci_int: Testes de integração (provedores locais)
    e2e: Testes end-to-end (deps externas)
    sdk: Forge SDK
    server: SymClient
    http: HTTP protocol
    stdio: STDIO protocol
```

**📄 Template:** `process/bdd/templates/template_step_skeleton.py`

---

### 🔹 Subetapa 6: Handoff para Roadmap Planning

**📥 Entrada:**
- Todos os artefatos das subetapas anteriores (BDD completo)

**📤 Saída:**
- `specs/bdd/HANDOFF_BDD.md` (documento de handoff para o planejamento)

**🎯 Objetivo:**
Empacotar e documentar formalmente a especificação de comportamento completa, entregando-a como entrada para a fase de **Roadmap Planning**.

**Conteúdo do HANDOFF_BDD.md:**

1.  **O que foi especificado:**
    *   Lista de todas as features Gherkin (`.feature`) criadas.
    *   Referência ao `tracks.yml` para rastreabilidade com os objetivos de negócio (ValueTracks).
    *   Referência ao `00_glossario.md` para a linguagem ubíqua.
2.  **Visão Geral dos Comportamentos:**
    *   Resumo dos principais domínios de negócio cobertos (ex: Core SDK, SymClient HTTP, Integrações).
    *   Destaque para os comportamentos mais críticos ou complexos que podem exigir maior atenção no planejamento arquitetural.
3.  **Próximo Passo:**
    *   O conjunto de especificações BDD está pronto para ser consumido pelo **Roadmap Planning Process** para definição da arquitetura, stack, estimativas e criação do backlog de implementação.

---

## 🔄 Ciclo Completo: MDD → BDD → TDD

```
┌─────────────────────────────────────────────────────────┐
│ MDD: Market Driven Development                          │
├─────────────────────────────────────────────────────────┤
│ Saída: docs/visao.md                                    │
│        docs/aprovacao_mvp.md                            │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼ Handoff MDD → BDD
┌─────────────────────────────────────────────────────────┐
│ BDD: Behavior Driven Development                        │
├─────────────────────────────────────────────────────────┤
│ Saída: specs/bdd/*.feature                              │
│        specs/bdd/tracks.yml                             │
│        tests/bdd/test_*_steps.py (skeleton)             │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼ Handoff BDD → TDD
┌─────────────────────────────────────────────────────────┐
│ TDD: Test Driven Development                            │
├─────────────────────────────────────────────────────────┤
│ Ação: Implementar src/forge/* e src/symclient/*         │
│       guiado pelos cenários BDD                         │
│                                                         │
│ Red → Green → Refactor (ciclo contínuo)                │
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 Critérios de Qualidade (DoD do BDD Process)

✅ **Completude:**
- [ ] Todas as features Gherkin escritas em PT-BR
- [ ] Todos os ValueTracks do MDD têm features correspondentes
- [ ] Cobertura mínima: 2-3 cenários por área crítica

✅ **Rastreabilidade:**
- [ ] `tracks.yml` mapeia features → tracks
- [ ] Cada track tem métricas definidas
- [ ] Template de PR exige Track ID + evidência

✅ **Execução:**
- [ ] Tags de CI aplicadas (`@ci-fast`, `@ci-int`, `@e2e`)
- [ ] Step definitions skeleton criadas
- [ ] `pytest.ini` configurado

✅ **Documentação:**
- [ ] `HANDOFF.md` completo
- [ ] `README.md` atualizado
- [ ] `00_glossario.md` com linguagem ubíqua

✅ **Separação de Responsabilidades:**
- [ ] Nenhum conteúdo de marketing (sites, pitch, CTAs)
- [ ] Foco 100% em produto (Forge SDK + SymClient)

---

## 📚 Documentos Relacionados

- **process/mdd/MDD_process.md** - Processo que gera entrada para BDD
- **process/PROCESS.md** - Visão geral do ciclo completo
- **process/execution/roadmap_planning/ROADMAP_PLANNING_PROCESS.md** - Próxima fase do processo
- **specs/bdd/README.md** - Guia de uso das features
- **specs/bdd/HANDOFF_BDD.md** - Documento de Handoff para Roadmap Planning

---

## 💡 Citações

> *"BDD não é sobre testes. É sobre estabelecer um contrato de comportamento que todos — negócio, produto, dev e QA — entendem e validam juntos."*

> *"Uma feature Gherkin bem escrita é ao mesmo tempo: especificação, documentação e teste automatizado."*

> *"O BDD é a ponte entre o valor validado no mercado (MDD) e o código testado em produção (TDD)."*

---

**Author**: Forge Framework Team
**Version**: 1.0
**Date**: 2025-11-04
**Context**: Separação dos processos MDD e BDD em módulos independentes e coesos
