# 🔹 BDD Subetapa 4: Criação de tracks.yml

## 🎯 Propósito

Estabelecer **rastreabilidade completa** entre:
- Features Gherkin ↔ ValueTracks do MDD
- Comportamentos implementados ↔ Métricas de sucesso
- Cenários BDD ↔ Unidades de valor de negócio entregues

O `tracks.yml` é o **mapa de navegação** entre valor de negócio e código testado.

---

## ⚙️ Entradas e Saídas

| Tipo | Artefato | Descrição |
|------|----------|-----------|
| **Entrada** | `specs/bdd/**/*.feature` | Features organizadas |
| **Entrada** | `project/docs/visao.md` | ValueTracks originais |
| **Saída** | `specs/bdd/tracks.yml` | Mapeamento tracks ↔ features |

---

## 📖 Estrutura do tracks.yml

```yaml
tracks:
  - id: [identificador_unico]
    type: VALUE | SUPPORT
    name: "[Nome descritivo do track]"
    owner: "[Time ou pessoa responsável]"
    metrics:
      - [metrica_1]
      - [metrica_2]
    features:
      - specs/bdd/[caminho]/[feature1].feature
      - specs/bdd/[caminho]/[feature2].feature
    notes: "[Contexto ou justificativa opcional]"
```

---

## 🎯 Campos Obrigatórios

### **id** (string)
Identificador único em snake_case.

**Convenção:**
- VALUE tracks: `value_[dominio]_[capacidade]`
- SUPPORT tracks: `support_[categoria]_[capacidade]`

**Exemplos:**
- `value_forge_chat_baseline`
- `value_symclient_http_api`
- `support_context_session`
- `support_observability_logs`

---

### **type** (VALUE | SUPPORT)

| Tipo | Quando Usar |
|------|-------------|
| **VALUE** | Comportamento entrega impacto direto ao usuário final |
| **SUPPORT** | Comportamento garante qualidade, confiabilidade ou habilitação técnica |

**Exemplos:**
- VALUE: Chat básico, integração MCP, roteamento broker
- SUPPORT: Logs, métricas, fallback, tratamento de erros

---

### **name** (string)
Título legível para humanos.

**Boas práticas:**
- Máximo 50 caracteres
- Descreve o que é entregue, não como
- Evita jargão técnico excessivo

**Exemplos:**
✅ "Chat básico multi-provedor (Forge SDK)"
✅ "Integração MCP Tecnospeed (Marketplace)"
✅ "Observabilidade: Logs estruturados"

❌ "ForgeClient.chat() implementation"
❌ "MCP stuff"

---

### **owner** (string)
Responsável pelo track (pessoa, time ou área).

**Exemplos:**
- "Time de Produto"
- "Jake, The Stake"
- "Engenharia de Plataforma"

---

### **metrics** (array de strings)
Métricas que comprovam sucesso do track.

**Para VALUE tracks:**
- Impacto de negócio: adoção, conversão, retenção
- Experiência: tempo de integração, facilidade de uso

**Para SUPPORT tracks:**
- Qualidade: confiabilidade, cobertura, disponibilidade
- Performance: latência, throughput

**Exemplos:**
```yaml
# VALUE track
metrics:
  - adocao_dev                # nº de projetos usando
  - tempo_primeira_integracao # tempo até primeiro chat funcionar
  - nps_sdk                   # satisfação dos desenvolvedores

# SUPPORT track
metrics:
  - confiabilidade_sessao     # % sessões preservadas corretamente
  - taxa_fallback_controlada  # fallbacks < 5% dos casos
  - cobertura_logs            # 100% eventos críticos logados
```

---

### **features** (array de caminhos)
Lista de features Gherkin que implementam o track.

**Formato:** Caminho relativo a partir de `specs/bdd/`

```yaml
features:
  - specs/bdd/10_forge_core/chat.feature
  - specs/bdd/10_forge_core/config.feature
```

---

### **notes** (string, opcional)
Contexto adicional, justificativa ou links.

```yaml
notes: "Baseline mínimo para qualquer uso do Forge. Prioridade P0."
```

---

## 📋 Exemplo Completo: tracks.yml do forgeLLMClient

```yaml
# Mapeamento de Tracks (Value/Support) e unidades de valor de negócio por feature
# Vincula comportamentos BDD aos ValueTracks do MDD

tracks:
  # ===========================
  # VALUE TRACKS
  # ===========================

  - id: value_forge_symclient_baseline
    type: VALUE
    name: "Baseline de uso (Forge SDK + SymClient)"
    owner: "Time de Produto"
    metrics:
      - adocao_dev                # nº de desenvolvedores usando
      - integracao_stack          # facilidade de integração (NPS)
      - tempo_primeiro_chat       # tempo até primeiro chat funcionar
    features:
      - specs/bdd/10_forge_core/chat.feature
      - specs/bdd/10_forge_core/config.feature
      - specs/bdd/20_symclient_http/chat_http.feature
      - specs/bdd/21_symclient_stdio/ping_chat.feature
    notes: "Funcionalidade mínima viável. Sem isso, o produto não existe."

  - id: value_ecosystem_tecnospeed
    type: VALUE
    name: "Integração ecossistema Tecnospeed"
    owner: "Time de Parcerias"
    metrics:
      - servicos_mcp_operacionais  # nº de serviços MCP funcionando
      - roteamento_broker_ok       # taxa de sucesso no roteamento
      - adocao_erps                # nº de ERPs conectados
    features:
      - specs/bdd/40_mcp_tecnospeed/marketplace.feature
      - specs/bdd/41_llm_broker_tecnospeed/routing.feature
    notes: "Diferencial competitivo. Integração estratégica com Casa do Desenvolvedor."

  # ===========================
  # SUPPORT TRACKS
  # ===========================

  - id: support_context_session
    type: SUPPORT
    name: "Sessões e contexto conversacional"
    owner: "Time de Engenharia"
    metrics:
      - confiabilidade            # % sessões preservadas corretamente
      - consistencia_contexto     # ausência de vazamento entre sessões
      - tempo_resposta_contexto   # latência ao buscar histórico
    features:
      - specs/bdd/10_forge_core/sessao.feature
    notes: "Habilita chat multi-turn. Crítico para VALUE tracks avançados."

  - id: support_capabilities_parity
    type: SUPPORT
    name: "Paridade de capacidades e fallbacks"
    owner: "Time de Engenharia"
    metrics:
      - portabilidade             # % features funcionam em todos provedores
      - taxa_fallback_controlada  # fallbacks < 5% dos casos
      - cobertura_capacidades     # % provedores com tool calling
    features:
      - specs/bdd/30_plugins_provedores/tool_calling_fallback.feature
      - specs/bdd/10_forge_core/streaming.feature
    notes: "Garante que trocar provedor não perde funcionalidades. Promessa central do produto."

  - id: support_protocols_errors
    type: SUPPORT
    name: "Protocolos e tratamento de erros"
    owner: "Time de Plataforma"
    metrics:
      - previsibilidade           # clareza de mensagens de erro
      - dx_api                    # facilidade de debugging (developer experience)
      - cobertura_erro            # % erros esperados tratados
    features:
      - specs/bdd/20_symclient_http/errors.feature
      - specs/bdd/21_symclient_stdio/errors.feature
    notes: "Reduz fricção e acelera desenvolvimento. Afeta diretamente NPS."

  - id: support_observability_security
    type: SUPPORT
    name: "Observabilidade e segurança"
    owner: "Time de Plataforma"
    metrics:
      - auditabilidade            # 100% eventos críticos logados
      - privacidade               # 0 vazamentos de PII em logs
      - tempo_debug               # redução de 50% em tempo de investigação
    features:
      - specs/bdd/50_observabilidade/logs_metrics.feature
      - specs/bdd/60_seguranca/redaction.feature
    notes: "Requisito não-funcional crítico para adoção enterprise."
```

---

## 🔗 Rastreabilidade: Como Usar o tracks.yml

### **1. Durante Desenvolvimento (Devs)**

Ao implementar uma feature BDD:

```bash
# Identificar o track
$ cat specs/bdd/tracks.yml | grep "10_forge_core/chat.feature"
# Resultado: value_forge_symclient_baseline

# Entender métricas de sucesso
$ yq '.tracks[] | select(.id == "value_forge_symclient_baseline") | .metrics' specs/bdd/tracks.yml
# - adocao_dev
# - integracao_stack
# - tempo_primeiro_chat
```

### **2. Durante PRs**

Template de PR deve incluir:

```markdown
## Track e Feature

- **Track ID**: `value_forge_symclient_baseline`
- **Feature**: `specs/bdd/10_forge_core/chat.feature`
- **Cenário implementado**: "Enviar mensagem simples e receber resposta"

## Unidade de Valor de Negócio Entregue

✅ Comportamento: Chat básico funcional com provedor echo

## Evidência

- [ ] Cenário BDD verde: `pytest -k test_enviar_mensagem_simples`
- [ ] Relatório: [link para CI]
- [ ] Métrica baseline: Tempo de integração = 5min (meta: < 10min)
```

### **3. Durante Retrospectivas**

Analisar entrega de valor por track:

```bash
# Quais tracks têm 100% features implementadas?
# Quais tracks estão bloqueados?
# Quais métricas melhoraram?
```

---

## ✅ Critérios de Qualidade (DoD)

- [ ] Todos os ValueTracks do MDD estão mapeados
- [ ] Cada track tem pelo menos 1 feature vinculada
- [ ] Cada track tem métricas claras e mensuráveis
- [ ] Owner definido para cada track
- [ ] Separação clara entre VALUE e SUPPORT
- [ ] Arquivo validado (YAML válido)
- [ ] Revisão com PO/Stakeholder

---

## 🧪 Validação do tracks.yml

```bash
# Validar sintaxe YAML
yq eval specs/bdd/tracks.yml

# Validar estrutura (campos obrigatórios)
python -m scripts.validate_tracks specs/bdd/tracks.yml
```

---

## 🔄 Próximo Passo

Com o `tracks.yml` pronto, avance para:

**Subetapa 5: Skeleton de Automação** (`etapa_05_skeleton_automacao.md`)

---

**Author**: Forge Framework Team
**Version**: 1.0
**Date**: 2025-11-04
