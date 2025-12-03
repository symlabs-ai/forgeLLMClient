# 🔹 BDD Subetapa 3: Organização e Tagging

## 🎯 Propósito

Estruturar as features Gherkin de forma que facilitem:
- **Navegação** (encontrar features rapidamente)
- **Execução seletiva** (rodar apenas subconjuntos)
- **CI/CD** (integrar testes em pipelines)
- **Rastreabilidade** (vincular features a tracks)

---

## ⚙️ Entradas e Saídas

| Tipo | Artefato | Descrição |
|------|----------|-----------|
| **Entrada** | `specs/bdd/**/*.feature` | Features recém-escritas |
| **Saída** | `specs/bdd/` (estruturada) | Pastas organizadas por domínio |
| **Saída** | `specs/bdd/README.md` | Guia de navegação e execução |
| **Saída** | Features com tags consistentes | Tagueamento completo |

---

## 🗂️ Estrutura de Pastas (Convenção Forge)

### Princípio: Prefixo Numérico + Domínio

```
specs/bdd/
├── 00_glossario.md                  ← Linguagem ubíqua
├── README.md                        ← Guia de uso
├── HANDOFF.md                       ← Instruções para DEV
├── tracks.yml                       ← Mapeamento (próxima etapa)
├── pull_request_template.md         ← Template de PR
│
├── 10_forge_core/                   ← Núcleo do SDK
│   ├── chat.feature
│   ├── sessao.feature
│   ├── config.feature
│   └── streaming.feature
│
├── 20_symclient_http/               ← Servidor HTTP
│   ├── health.feature
│   ├── chat_http.feature
│   └── errors.feature
│
├── 21_symclient_stdio/              ← Servidor STDIO
│   ├── ping.feature
│   ├── chat_stdio.feature
│   └── errors.feature
│
├── 30_plugins_provedores/           ← Portabilidade
│   ├── capabilities.feature
│   └── tool_calling_fallback.feature
│
├── 40_mcp_tecnospeed/               ← Integrações VALUE
│   ├── marketplace.feature
│   └── discovery.feature
│
├── 41_llm_broker_tecnospeed/
│   └── routing.feature
│
├── 50_observabilidade/              ← Qualidade SUPPORT
│   ├── logs.feature
│   └── metrics.feature
│
└── 60_seguranca/
    ├── redaction.feature
    └── auth.feature
```

### Convenção de Prefixos

| Prefixo | Domínio | Tipo Track | Descrição |
|---------|---------|------------|-----------|
| `10_*` | Forge Core | VALUE/SUPPORT | SDK Python, funcionalidades centrais |
| `20_*` | SymClient HTTP | VALUE | Servidor com protocolo HTTP |
| `21_*` | SymClient STDIO | VALUE | Servidor com protocolo STDIO/JSON-RPC |
| `30_*` | Plugins/Provedores | SUPPORT | Arquitetura de extensão |
| `40_*` | MCP | VALUE | Integrações de mercado (Tecnospeed) |
| `41_*` | Broker | VALUE | Roteamento e agregação LLM |
| `50_*` | Observabilidade | SUPPORT | Logs, métricas, traces |
| `60_*` | Segurança | SUPPORT | Auth, redaction, rate limit |

**Regra:** Prefixos 40+ são para integrações externas (VALUE). 50+ são para qualidades cross-cutting (SUPPORT).

---

## 🏷️ Sistema de Tags Completo

### Tags Obrigatórias (toda feature deve ter pelo menos 2)

#### 1. **Tag de Domínio** (obrigatória)

```gherkin
@sdk          # Forge SDK Python
@server       # SymClient (HTTP ou STDIO)
@http         # Protocolo HTTP específico
@stdio        # Protocolo STDIO/JSON-RPC específico
```

**Uso:**
```gherkin
@sdk
FUNCIONALIDADE: Chat básico no Forge SDK
  ...

@server @http
FUNCIONALIDADE: Endpoint /chat do SymClient HTTP
  ...
```

---

#### 2. **Tag de CI** (obrigatória)

```gherkin
@ci-fast      # Rápido: mocks/stubs, sem deps externas
@ci-int       # Integração: provedores locais, deps internas
@e2e          # End-to-end: ambiente controlado, deps externas
```

**Regras:**
- **@ci-fast**: Deve rodar em < 5 segundos por feature, em qualquer ambiente
- **@ci-int**: Pode exigir Docker, serviços locais (Redis, PostgreSQL)
- **@e2e**: Exige credenciais, APIs externas (MCP Tecnospeed, OpenRouter)

**Exemplo:**
```gherkin
@sdk @ci-fast
FUNCIONALIDADE: Chat com provedor mock "echo"
  ...

@server @http @ci-int
FUNCIONALIDADE: SymClient HTTP rodando localmente
  ...

@mcp @e2e
FUNCIONALIDADE: Integração MCP Tecnospeed (ambiente staging)
  ...
```

---

### Tags Opcionais (Capacidades e Categorias)

#### 3. **Tags de Capacidade**

```gherkin
@contexto                   # Gestão de sessão/histórico
@streaming                  # Respostas em stream (SSE, WebSocket)
@capability:tool_calling    # Tool calling / function calling
@capability:vision          # Processamento de imagem
@capability:audio           # Processamento de áudio
@fallback                   # Estratégias de fallback
```

#### 4. **Tags de Integração**

```gherkin
@mcp           # Model Context Protocol
@broker        # Roteamento via LLM Broker
@tecnospeed    # Ecossistema Tecnospeed específico
```

#### 5. **Tags de Categoria**

```gherkin
@observabilidade   # Logs, métricas, traces
@seguranca         # Auth, PII redaction, rate limit
@erro              # Cenários de tratamento de erro
@performance       # Testes de latência, throughput
```

---

## 📋 Exemplo Completo de Tagueamento

```gherkin
# specs/bdd/10_forge_core/chat.feature

@sdk @ci-fast
FUNCIONALIDADE: Chat básico no Forge SDK
  PARA enviar mensagens e receber respostas
  COMO um desenvolvedor
  QUERO usar interface consistente

  CENÁRIO: Enviar mensagem simples
    ...
```

```gherkin
# specs/bdd/30_plugins_provedores/tool_calling_fallback.feature

@sdk @capability:tool_calling @fallback @ci-fast
FUNCIONALIDADE: Tool calling com fallback automático
  PARA garantir portabilidade
  COMO um desenvolvedor
  QUERO que tool calling funcione mesmo em provedores sem suporte nativo

  ESQUEMA DO CENÁRIO: Executar tool em diferentes provedores
    ...
```

```gherkin
# specs/bdd/40_mcp_tecnospeed/marketplace.feature

@mcp @tecnospeed @e2e
FUNCIONALIDADE: Integração MCP Tecnospeed Marketplace
  PARA publicar/consumir serviços
  COMO um desenvolvedor de ERP
  QUERO conectar ao marketplace via SymClient

  CENÁRIO: Registrar serviço no marketplace
    ...
```

---

## 📖 Criar README.md do BDD

O `specs/bdd/README.md` serve como **índice navegável** e **guia de execução**.

### Template Sugerido

```markdown
# Especificação BDD — Forge SDK e SymClient

Este diretório contém as **features Gherkin** que especificam o comportamento do:
- **Forge**: SDK Python para integração multi-provedor LLM
- **SymClient**: Servidor HTTP/STDIO para integração language-agnostic

---

## 📁 Estrutura de Pastas

| Pasta | Domínio | Tipo Track | Descrição |
|-------|---------|------------|-----------|
| `10_forge_core/` | Forge SDK | VALUE/SUPPORT | Chat, sessão, config, streaming |
| `20_symclient_http/` | SymClient HTTP | VALUE | Endpoints /health, /chat |
| `21_symclient_stdio/` | SymClient STDIO | VALUE | JSON-RPC ping, chat |
| `30_plugins_provedores/` | Plugins | SUPPORT | Capacidades, fallbacks |
| `40_mcp_tecnospeed/` | MCP | VALUE | Marketplace Tecnospeed |
| `41_llm_broker_tecnospeed/` | Broker | VALUE | Roteamento LLM |
| `50_observabilidade/` | Observability | SUPPORT | Logs, métricas |
| `60_seguranca/` | Security | SUPPORT | Redaction, auth |

---

## 🏷️ Sistema de Tags

### Execução por Ambiente

```bash
# Testes rápidos (mocks, sem deps)
pytest -m ci_fast tests/bdd/

# Testes de integração (provedores locais)
pytest -m ci_int tests/bdd/

# Testes end-to-end (deps externas)
pytest -m e2e tests/bdd/
```

### Execução por Domínio

```bash
# Apenas Forge SDK
pytest -m sdk tests/bdd/

# Apenas SymClient
pytest -m server tests/bdd/

# Apenas HTTP
pytest -m "server and http" tests/bdd/
```

### Execução por Capacidade

```bash
# Tool calling
pytest -m capability_tool_calling tests/bdd/

# Streaming
pytest -m streaming tests/bdd/
```

---

## 🔗 Rastreabilidade

- Mapeamento **features → tracks**: Ver `tracks.yml`
- Template de PR: Ver `pull_request_template.md`
- Handoff para DEV: Ver `HANDOFF.md`

---

## 🧪 Executar Localmente

```bash
# Instalar dependências
pip install -r requirements-dev.txt

# Rodar todos os testes fast
pytest -m ci_fast -v

# Rodar com relatório HTML
pytest -m ci_fast --html=report.html --self-contained-html
```
```

---

## ✅ Critérios de Qualidade (DoD)

- [ ] Features organizadas em pastas por domínio com prefixos numéricos
- [ ] Todas as features têm pelo menos 2 tags (domínio + CI)
- [ ] Tags aplicadas consistentemente em todo o projeto
- [ ] `README.md` criado com guia de execução
- [ ] Estrutura revisada com time de desenvolvimento

---

## 🔄 Próximo Passo

Com a estrutura organizada e tagueada, avance para:

**Subetapa 4: Criação de tracks.yml** (`etapa_04_tracks_yml.md`)

---

**Author**: Forge Framework Team
**Version**: 1.0
**Date**: 2025-11-04
