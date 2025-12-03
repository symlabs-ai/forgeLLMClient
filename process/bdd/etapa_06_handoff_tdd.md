# 🔹 BDD Subetapa 6: Handoff para TDD

## 🎯 Propósito

Entregar o **pacote BDD completo** para o time de desenvolvimento com:
- Documentação clara de como usar
- Priorização de features
- Políticas de PR e rastreabilidade
- Guia de início rápido para TDD

Esta é a **ponte** entre especificação (BDD) e implementação (TDD).

---

## ⚙️ Entradas e Saídas

| Tipo | Artefato | Descrição |
|------|----------|-----------|
| **Entrada** | Todas as saídas das etapas 1-5 | BDD completo |
| **Saída** | `specs/bdd/HANDOFF.md` | Documento de handoff |
| **Saída** | `specs/bdd/README.md` | Guia de uso atualizado |
| **Saída** | `specs/bdd/pull_request_template.md` | Template de PR |
| **Saída** | `specs/bdd/QUICKSTART.md` | Guia de início rápido (opcional) |

---

## 📄 Conteúdo do HANDOFF.md

### Estrutura Recomendada

```markdown
# Handoff BDD → TDD — [Nome do Projeto]

> **Status:** Especificação BDD completa. Pronto para implementação TDD.
>
> **Data:** [AAAA-MM-DD]
>
> **Revisão:** [PO/Stakeholder]

---

## 1. O Que Foi Entregue

### Especificação BDD

- **13 features Gherkin** (PT-BR) organizadas em 8 domínios
- **6 tracks** mapeados (2 VALUE, 4 SUPPORT)
- **tracks.yml** vinculando features → tracks → métricas
- **Step definitions skeleton** (pytest-bdd) marcados como skip

### Estrutura de Pastas

```
specs/bdd/
├── 10_forge_core/         → 4 features (chat, sessao, config, streaming)
├── 20_symclient_http/     → 2 features (chat_http, errors)
├── 21_symclient_stdio/    → 2 features (ping_chat, errors)
├── 30_plugins_provedores/ → 1 feature (tool_calling_fallback)
├── 40_mcp_tecnospeed/     → 1 feature (marketplace)
├── 41_llm_broker_tecnospeed/ → 1 feature (routing)
├── 50_observabilidade/    → 1 feature (logs_metrics)
└── 60_seguranca/          → 1 feature (redaction)
```

### Rastreabilidade

- `tracks.yml`: Mapeia features → ValueTracks do MDD
- `00_glossario.md`: Linguagem ubíqua do domínio
- `pull_request_template.md`: Template de PR com Track ID

---

## 2. Priorização de Implementação

### Fase 1: Baseline VALUE (Sprint 1-2)

**Objetivo:** Entregar funcionalidade mínima viável.

| Prioridade | Track ID | Features | Critério de Sucesso |
|------------|----------|----------|---------------------|
| 🔴 P0 | `value_forge_symclient_baseline` | `chat.feature`, `chat_http.feature` | Chat básico funcional com echo provider |

**DoD Fase 1:**
- [ ] `pytest -m "ci_fast and sdk"` → todos passando
- [ ] `pytest -m "ci_fast and http"` → todos passando
- [ ] Tempo de integração < 10 minutos (meta: adocao_dev)

---

### Fase 2: Contexto SUPPORT (Sprint 3)

**Objetivo:** Habilitar conversas multi-turn.

| Prioridade | Track ID | Features | Critério de Sucesso |
|------------|----------|----------|---------------------|
| 🟠 P1 | `support_context_session` | `sessao.feature` | Histórico preservado por session_id |

**DoD Fase 2:**
- [ ] Cenários de sessão passando
- [ ] Isolamento entre sessões validado
- [ ] Métrica: confiabilidade > 99%

---

### Fase 3: Portabilidade SUPPORT (Sprint 4)

**Objetivo:** Garantir paridade de capacidades.

| Prioridade | Track ID | Features | Critério de Sucesso |
|------------|----------|----------|---------------------|
| 🟡 P2 | `support_capabilities_parity` | `tool_calling_fallback.feature`, `streaming.feature` | Fallback funcional em provedores sem tool calling |

**DoD Fase 3:**
- [ ] Tool calling funciona em 3 provedores (incluindo fallback)
- [ ] Streaming funciona onde disponível
- [ ] Métrica: portabilidade > 90%

---

### Fase 4: Observabilidade & Segurança SUPPORT (Sprint 5)

| Prioridade | Track ID | Features |
|------------|----------|----------|
| 🟢 P3 | `support_observability_security` | `logs_metrics.feature`, `redaction.feature` |
| 🟢 P3 | `support_protocols_errors` | `errors.feature` (HTTP/STDIO) |

---

### Fase 5: Ecossistema VALUE (Sprint 6)

**Objetivo:** Integração Tecnospeed (diferencial competitivo).

| Prioridade | Track ID | Features |
|------------|----------|----------|
| 🔵 P4 | `value_ecosystem_tecnospeed` | `marketplace.feature`, `routing.feature` |

---

## 3. Como Executar Localmente

### Setup Inicial

```bash
# 1. Clonar repositório
git clone [repo-url]
cd forgeLLMClient

# 2. Criar ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# 3. Instalar dependências
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 4. Validar setup
pytest --collect-only tests/bdd/
# Deve listar todos os cenários BDD
```

### Executar Testes BDD

```bash
# Todos os testes (skipped por enquanto)
pytest tests/bdd/ -v

# Apenas CI fast (quando implementados)
pytest -m ci_fast tests/bdd/

# Apenas SDK
pytest -m sdk tests/bdd/

# Feature específica
pytest tests/bdd/test_forge_chat_steps.py -v

# Com relatório HTML
pytest -m ci_fast --html=report.html --self-contained-html
```

---

## 4. Como Implementar (Ciclo TDD)

### 🔴 RED: Escrever teste que falha

1. Escolher uma feature (ex: `chat.feature`)
2. Abrir step file: `tests/bdd/test_forge_chat_steps.py`
3. **Remover** `pytestmark = pytest.mark.skip(...)`
4. Rodar teste:
   ```bash
   pytest tests/bdd/test_forge_chat_steps.py -v
   ```
5. Resultado esperado: **FAIL** (código não existe)

---

### 🟢 GREEN: Implementar código mínimo

1. Criar estrutura de código:
   ```
   src/forge/
   ├── __init__.py
   ├── client.py          ← ForgeClient
   ├── providers/
   │   ├── __init__.py
   │   ├── base.py        ← AbstractProvider
   │   └── echo.py        ← EchoProvider (mock)
   └── models/
       └── chat.py        ← ChatRequest/Response
   ```

2. Implementar código mínimo que passa:
   ```python
   # src/forge/client.py
   class ForgeClient:
       def __init__(self, provider: str):
           self.provider = provider

       def chat(self, message: str):
           return ChatResponse(content=f"Echo: {message}")
   ```

3. Implementar steps:
   ```python
   # tests/bdd/test_forge_chat_steps.py

   @given('que o Forge está configurado com o provedor "echo"')
   def forge_with_echo():
       from forge import ForgeClient
       return ForgeClient(provider="echo")

   @when('envio a mensagem "{message}"')
   def send_message(forge_client, message):
       return forge_client.chat(message)

   @then('recebo uma resposta contendo "{text}"')
   def check_response(response, text):
       assert text in response.content
   ```

4. Rodar teste novamente:
   ```bash
   pytest tests/bdd/test_forge_chat_steps.py -v
   ```
5. Resultado esperado: **PASS** ✅

---

### 🔵 REFACTOR: Melhorar mantendo verde

1. Adicionar type hints
2. Extrair interfaces (Ports)
3. Aplicar padrões (Factory, Repository, etc)
4. Adicionar logging
5. Rodar testes a cada mudança (devem continuar passando)

---

## 5. Políticas de PR

### Template de PR

Use `specs/bdd/pull_request_template.md`:

```markdown
## Track e Feature

- **Track ID**: `value_forge_symclient_baseline`
- **Track Type**: VALUE
- **Feature**: `specs/bdd/10_forge_core/chat.feature`
- **Cenário(s) implementado(s)**:
  - [ ] "Enviar mensagem simples e receber resposta"
  - [ ] "Erro ao usar provedor não configurado"

## Unidade de Valor de Negócio Entregue

**Comportamento:** Chat básico funcional com provedor echo

**Impacto esperado:** Reduz tempo de primeira integração para < 10min

## Evidências

- [ ] Cenários BDD verde: `pytest -k test_forge_chat -v`
- [ ] Relatório CI: [link]
- [ ] Cobertura de código: X%
- [ ] Métrica baseline registrada: tempo_primeiro_chat = Ymin

## Checklist

- [ ] Step definitions implementadas (não vazias)
- [ ] Código segue padrões do projeto
- [ ] Documentação atualizada (docstrings, README)
- [ ] Nenhum TODO deixado sem justificativa
```

### Regras de Merge

- ✅ Todos os cenários BDD do PR devem estar **PASS**
- ✅ Cobertura de código > 80% das linhas modificadas
- ✅ CI passando (linting, type checking, testes)
- ✅ Revisão de pelo menos 1 desenvolvedor
- ✅ Track ID referenciado no PR
- ✅ Evidência de teste anexada

---

## 6. Dúvidas Frequentes

### P: Posso implementar múltiplas features no mesmo PR?

**R:** Prefira PRs pequenos (1 feature ou 1-2 cenários). Se houver dependência forte, documente claramente.

---

### P: E se o código precisar ser muito diferente da spec BDD?

**R:** Primeiro questionar: a spec está errada ou o código?
- Se spec está errada: Voltar ao processo BDD, revisar com PO
- Se código precisa ser complexo: OK, mas comportamento externo deve bater

---

### P: Como lidar com cenários que dependem de APIs externas (MCP, Broker)?

**R:** Use tags:
- `@ci-fast`: Mock a API (sempre verde)
- `@e2e`: API real (rodar sob demanda)

Ambos os cenários devem existir e ser mantidos.

---

### P: Posso mudar a feature Gherkin durante implementação?

**R:** Apenas com aprovação do PO. Features são contrato, não sugestão. Se precisar mudar, documentar razão no PR.

---

## 7. Contatos e Suporte

- **PO/Product**: [Nome/Email]
- **Tech Lead**: [Nome/Email]
- **Canal Slack**: #forge-dev
- **Documentação**: `specs/bdd/README.md`
- **Issues**: [Link do projeto]

---

## 8. Próximos Passos Imediatos

1. **Time de DEV**: Review deste handoff, esclarecer dúvidas
2. **Sprint Planning**: Priorizar Fase 1 (Baseline VALUE)
3. **Setup**: Cada dev roda `pytest --collect-only` localmente
4. **Kick-off TDD**: Escolher primeira feature e começar Red-Green-Refactor

---

**Entrega oficial:** [Data]
**Assinatura PO:** [Nome]
**Próxima revisão:** [Data]
```

---

## 📋 Checklist de Entrega

### Artefatos Obrigatórios

- [ ] `specs/bdd/HANDOFF.md` completo
- [ ] `specs/bdd/README.md` atualizado com instruções de execução
- [ ] `specs/bdd/pull_request_template.md` criado
- [ ] `specs/bdd/tracks.yml` validado
- [ ] `specs/bdd/00_glossario.md` finalizado
- [ ] Todas as features com tags corretas
- [ ] Step definitions skeleton criadas
- [ ] `pytest.ini` e `requirements-dev.txt` configurados

### Validações Técnicas

- [ ] `pytest --collect-only tests/bdd/` → sem erros
- [ ] `pytest tests/bdd/ -v` → todos skipped (ainda não implementados)
- [ ] `yq eval specs/bdd/tracks.yml` → YAML válido
- [ ] Estrutura de pastas segue convenção (prefixos numéricos)

### Validações de Negócio

- [ ] PO revisou e aprovou todas as features
- [ ] Priorização alinhada com roadmap do MDD
- [ ] Métricas de cada track são mensuráveis
- [ ] Stakeholders cientes do handoff

---

## ✅ Critérios de Qualidade (DoD do Processo BDD)

- [ ] Todas as 6 subetapas executadas
- [ ] Documentação completa e revisada
- [ ] Time de DEV capacitado (sessão de onboarding realizada)
- [ ] Primeiro PR de exemplo criado (pode ser spike/demo)
- [ ] Processo BDD oficialmente encerrado
- [ ] **Processo TDD oficialmente iniciado**

---

## 🎉 Cerimônia de Handoff (Sugerida)

1. **Demo das Features** (30min)
   - PO apresenta features Gherkin
   - Mostra rastreabilidade com MDD

2. **Walkthrough Técnico** (30min)
   - Tech Lead mostra estrutura de código
   - Executa exemplo de Red-Green-Refactor ao vivo

3. **Q&A** (20min)
   - Time esclarece dúvidas
   - Alinha expectativas

4. **Sprint Planning** (40min)
   - Prioriza primeira onda de features
   - Define DoD e métricas de sprint

---

## 🔄 Próximo Processo

Com o BDD entregue, inicia-se:

**TDD Process** (Test Driven Development)
- Ciclo: Red → Green → Refactor
- Implementação de `src/forge/` e `src/symclient/`
- Validação contínua com cenários BDD

---

**Author**: Forge Framework Team
**Version**: 1.0
**Date**: 2025-11-04
