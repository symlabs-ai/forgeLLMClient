# 🔹 BDD Subetapa 1: Mapeamento de Comportamentos

## 🎯 Propósito

Transformar **ValueTracks validados no MDD** em **comportamentos concretos e verificáveis** que serão especificados em Gherkin.

Esta é a **tradução** mais importante do BDD: passar de "valor de negócio" para "ação observável".

---

## ⚙️ Entradas e Saídas

| Tipo | Artefato | Descrição |
|------|----------|-----------|
| **Entrada** | `project/docs/visao.md` | ValueTracks e proposta de valor |
| **Entrada** | `project/docs/sumario_executivo.md` | Contexto estratégico e diferencial |
| **Entrada** | `project/docs/aprovacao_mvp.md` | Decisão de avanço (se houver) |
| **Saída** | `process/bdd/docs/behavior_mapping.md` | Mapeamento Track → Behaviors |

---

## 🧭 Como Fazer o Mapeamento

### Passo 1: Extrair ValueTracks do MDD

Liste todos os ValueTracks definidos em `visao.md`:

**Exemplo:**
```yaml
ValueTracks do forgeLLMClient:
  1. Chat básico multi-provedor
  2. Gestão de contexto por sessão
  3. Portabilidade com fallback
  4. Integração MCP Tecnospeed
  5. Roteamento via LLM Broker
```

---

### Passo 2: Para Cada Track, Perguntar

Para cada ValueTrack, faça as **5 perguntas de comportamento:**

| Pergunta | Objetivo | Exemplo |
|----------|----------|---------|
| **O QUÊ o usuário faz?** | Ação principal | "Enviar mensagem", "Criar sessão" |
| **O QUÊ ele espera ver?** | Resultado de sucesso | "Receber resposta", "Contexto preservado" |
| **O QUE pode dar errado?** | Cenários de erro | "Provedor inválido", "Sessão não existe" |
| **COMO saber que funcionou?** | Critério observável | "Resposta contém texto", "Log registra evento" |
| **QUAL o comportamento em edge cases?** | Limites e exceções | "Timeout", "Rate limit", "Resposta vazia" |

---

### Passo 3: Agrupar por Domínio Técnico

Organize comportamentos por **módulo do produto**:

```
Domínios:
├─ 10_forge_core/        → Forge SDK (Python)
├─ 20_symclient_http/    → Servidor HTTP
├─ 21_symclient_stdio/   → Servidor STDIO/JSON-RPC
├─ 30_plugins/           → Arquitetura de plugins
├─ 40_mcp/               → Integração MCP
├─ 41_broker/            → Roteamento LLM
├─ 50_observabilidade/   → Logs, métricas
└─ 60_seguranca/         → Redação PII, auth
```

---

## 📋 Exemplo Completo de Mapeamento

### ValueTrack: "Chat básico multi-provedor"

| Pergunta | Resposta | Comportamento Derivado |
|----------|----------|------------------------|
| O QUÊ o usuário faz? | Configura provedor e envia mensagem | CENÁRIO: Configurar e usar provedor |
| O QUÊ ele espera? | Resposta do LLM | ENTÃO: Recebo resposta contendo texto |
| O QUE pode dar errado? | Provedor não existe | CENÁRIO: Erro ao configurar provedor inválido |
| COMO saber que funcionou? | Resposta não vazia e válida | ENTÃO: Resposta tem formato esperado |
| Edge cases? | Provedor offline, timeout | CENÁRIO: Tratamento de timeout |

**Mapeamento final:**

```
ValueTrack: "Chat básico multi-provedor" (VALUE)
├─ Domínio: 10_forge_core/
└─ Comportamentos:
    ├─ CENÁRIO: Enviar mensagem e receber resposta (happy path)
    ├─ CENÁRIO: Erro ao usar provedor não configurado
    ├─ CENÁRIO: Erro ao usar provedor inválido
    └─ CENÁRIO: Timeout ao aguardar resposta
```

---

### ValueTrack: "Gestão de contexto por sessão"

| Pergunta | Resposta | Comportamento Derivado |
|----------|----------|------------------------|
| O QUÊ o usuário faz? | Cria sessão e envia múltiplas mensagens | CENÁRIO: Preservar histórico na sessão |
| O QUÊ ele espera? | Mensagens subsequentes têm contexto anterior | ENTÃO: Resposta considera mensagens anteriores |
| O QUE pode dar errado? | Vazamento de contexto entre sessões | CENÁRIO: Isolar contextos entre sessões |
| COMO saber que funcionou? | Session_id identifica conversas distintas | ENTÃO: Sessão A não vê mensagens da sessão B |
| Edge cases? | Sessão expira, limite de histórico | CENÁRIO: Expiração de sessão inativa |

**Mapeamento final:**

```
ValueTrack: "Gestão de contexto por sessão" (SUPPORT)
├─ Domínio: 10_forge_core/
└─ Comportamentos:
    ├─ CENÁRIO: Criar sessão com session_id
    ├─ CENÁRIO: Preservar histórico de mensagens
    ├─ CENÁRIO: Isolar contextos entre sessões diferentes
    └─ CENÁRIO: Tratar expiração de sessão
```

---

## 🗂️ Template de Mapeamento

Use o template `process/bdd/templates/template_behavior_mapping.md`:

```markdown
# Mapeamento de Comportamentos — [Nome do Projeto]

## ValueTrack: [Nome do Track]

**Tipo:** VALUE | SUPPORT
**Domínio:** [10_forge_core, 20_symclient_http, etc]

### Comportamentos Identificados

1. **[Nome do Comportamento]**
   - Ação: [O que o usuário faz]
   - Resultado esperado: [O que ele vê]
   - Critério: [Como validar]
   - Cenário BDD: [Nome do cenário futuro]

2. **[Outro Comportamento]**
   ...

### Casos de Erro

1. **[Nome do Erro]**
   - Condição: [Quando ocorre]
   - Tratamento esperado: [Como o sistema reage]
   - Cenário BDD: [Nome do cenário futuro]

---

## ValueTrack: [Próximo Track]
...
```

---

## 🚨 Armadilhas Comuns

❌ **Pensar em implementação técnica**
- Errado: "Chamar método `chat()` da classe `ForgeClient`"
- Certo: "Enviar mensagem e receber resposta"

❌ **Misturar múltiplos comportamentos**
- Errado: "Enviar mensagem, preservar contexto E logar evento"
- Certo: Dividir em 3 cenários distintos

❌ **Incluir detalhes de UI/marketing**
- Errado: "Clicar no botão azul de enviar"
- Certo: "Enviar mensagem" (agnóstico de interface)

❌ **Esquecer casos de erro**
- Errado: Só mapear happy paths
- Certo: Para cada sucesso, mapear 2-3 erros prováveis

---

## ✅ Critérios de Qualidade (DoD)

- [ ] Todos os ValueTracks do MDD foram analisados
- [ ] Cada Track tem pelo menos 2 comportamentos (1 sucesso + 1 erro)
- [ ] Comportamentos estão agrupados por domínio técnico
- [ ] Linguagem é de negócio (não implementação)
- [ ] Mapeamento revisado com stakeholder/PO

---

## 🔄 Próximo Passo

Com o `behavior_mapping.md` pronto, avance para:

**Subetapa 2: Escrita de Features Gherkin** (`etapa_02_escrita_features.md`)

---

**Author**: Forge Framework Team
**Version**: 1.0
**Date**: 2025-11-04
