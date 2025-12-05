# ForgeLLM Client - Plano de Sprints

## Status Geral
- **Última atualização**: 2025-12-05
- **Testes passando**: 718
- **Sprint atual**: 21

## Sprints Completados

### Sprint 15: Observability & Metrics ✅
- [x] Events dataclasses (ChatStartEvent, ChatCompleteEvent, etc.)
- [x] ObserverPort interface
- [x] ObservabilityManager
- [x] LoggingObserver
- [x] MetricsObserver
- [x] CallbackObserver
- [x] Integração no Client
- [x] Testes unitários
- [x] BDD feature e steps

### Sprint 16: Documentation ✅
- [x] Guias de uso
- [x] Documentação de API

### Sprint 17: Integration Tests ✅
- [x] Testes de integração com APIs reais

### Sprint 18: Structured Output / JSON Mode ✅
- [x] ResponseFormat value object
- [x] ResponseFormat.text(), .json(), .json_with_schema()
- [x] ResponseFormat.from_pydantic() com additionalProperties:false
- [x] OpenAI provider: text.format parameter
- [x] Anthropic provider: prompt engineering + tool workaround
- [x] Client: response_format parameter
- [x] Testes unitários (17 testes)
- [x] Testes de integração (5 testes)

---

## Sprints Pendentes

### Sprint 19: BDD Feature para JSON Mode ✅
**Objetivo**: Criar specs BDD para documentar comportamento de structured output

**Arquivos criados**:
- [x] `specs/bdd/10_forge_core/json_mode.feature` (24 cenários)
- [x] `tests/bdd/test_json_mode_steps.py`

**Cenários BDD**:
- [x] Formato texto padrão
- [x] JSON object mode retorna JSON válido
- [x] JSON schema mode valida contra schema
- [x] Pydantic model cria schema correto
- [x] Strict mode adiciona additionalProperties
- [x] Provider Anthropic usa workaround

---

### Sprint 20: OpenRouter Provider ✅
**Objetivo**: Adicionar suporte ao OpenRouter para acesso a múltiplos modelos

**Arquivos modificados/criados**:
- [x] `src/forge_llm/providers/openrouter_provider.py` (response_format suporte)
- [x] `tests/unit/providers/test_openrouter_provider.py` (42 testes)
- [x] `tests/integration/test_openrouter_integration.py`

**Funcionalidades**:
- [x] Chat com modelos via OpenRouter
- [x] Streaming support
- [x] Tool calling (quando suportado pelo modelo)
- [x] Response format (json_object e json_schema)
- [x] Headers específicos (HTTP-Referer, X-Title)

**BDD**:
- [x] `specs/bdd/10_forge_core/openrouter.feature` (8 cenários)
- [x] `tests/bdd/test_openrouter_steps.py`

---

### Sprint 21: Auto-Fallback Provider 🔄 IN PROGRESS
**Objetivo**: Provider que faz fallback automático entre providers

**Arquivos a criar**:
- [ ] `src/forge_llm/providers/auto_fallback_provider.py`
- [ ] `tests/unit/providers/test_auto_fallback_provider.py`

**Funcionalidades**:
- [ ] Configuração de lista de providers ordenada por prioridade
- [ ] Fallback automático em caso de erro
- [ ] Fallback em caso de rate limit
- [ ] Métricas de fallback (qual provider foi usado)
- [ ] Configuração de retry antes de fallback
- [ ] Healthcheck de providers

**BDD**:
- [ ] `specs/bdd/30_providers/auto_fallback.feature`
- [ ] `tests/bdd/test_auto_fallback_steps.py`

---

### Sprint 22: Streaming Melhorado
**Objetivo**: Melhorar suporte a streaming com eventos tipados

**Arquivos a modificar**:
- [ ] `src/forge_llm/domain/entities.py` - StreamEvent types
- [ ] `src/forge_llm/providers/openai_provider.py`
- [ ] `src/forge_llm/providers/anthropic_provider.py`
- [ ] `src/forge_llm/client.py`

**Funcionalidades**:
- [ ] StreamEvent dataclass (content, tool_call_start, tool_call_delta, done)
- [ ] Parsing de tool calls em stream
- [ ] Agregação de chunks
- [ ] Callback para cada tipo de evento
- [ ] Timeout configurável por chunk

**Arquivos a criar**:
- [ ] `src/forge_llm/domain/stream_events.py`
- [ ] `tests/unit/domain/test_stream_events.py`

**BDD**:
- [ ] `specs/bdd/10_forge_core/streaming.feature`
- [ ] `tests/bdd/test_streaming_steps.py`

---

### Sprint 23: MCP Integration (Model Context Protocol)
**Objetivo**: Integração com MCP para tools e resources externos

**Arquivos a criar**:
- [ ] `src/forge_llm/mcp/` (diretório)
- [ ] `src/forge_llm/mcp/__init__.py`
- [ ] `src/forge_llm/mcp/client.py`
- [ ] `src/forge_llm/mcp/types.py`
- [ ] `src/forge_llm/mcp/tool_adapter.py`
- [ ] `tests/unit/mcp/test_mcp_client.py`
- [ ] `tests/unit/mcp/test_tool_adapter.py`

**Funcionalidades**:
- [ ] Conexão com MCP servers
- [ ] Descoberta de tools
- [ ] Conversão de MCP tools para formato interno
- [ ] Execução de tools via MCP
- [ ] Suporte a resources
- [ ] Suporte a prompts

**BDD**:
- [ ] `specs/bdd/20_integrations/mcp.feature`
- [ ] `tests/bdd/test_mcp_steps.py`

---

### Sprint 24: Conversation Management
**Objetivo**: Gerenciamento avançado de conversas

**Arquivos a criar/modificar**:
- [ ] `src/forge_llm/domain/conversation.py`
- [ ] `src/forge_llm/utils/conversation_memory.py` (melhorar se existir)
- [ ] `src/forge_llm/persistence/` (diretório)
- [ ] `src/forge_llm/persistence/conversation_store.py`
- [ ] `src/forge_llm/persistence/json_store.py`
- [ ] `src/forge_llm/persistence/sqlite_store.py`

**Funcionalidades**:
- [ ] Conversation entity com ID único
- [ ] Persistência em JSON
- [ ] Persistência em SQLite
- [ ] Busca por conversas
- [ ] Resumo automático de conversas longas
- [ ] Fork de conversas
- [ ] Branching (múltiplas respostas)

**BDD**:
- [ ] `specs/bdd/10_forge_core/conversation.feature` (atualizar se existir)
- [ ] `tests/bdd/test_conversation_steps.py` (atualizar se existir)

---

## Checklist de Qualidade (por Sprint)

Para cada sprint, verificar:
- [ ] Testes unitários passando
- [ ] Testes BDD passando
- [ ] `ruff check` sem erros
- [ ] `mypy` sem erros
- [ ] Cobertura > 80%
- [ ] Exports em `__init__.py`
- [ ] Documentação atualizada

---

## Comandos Úteis

```bash
# Rodar todos os testes
.venv/bin/pytest tests/ -q --tb=no

# Rodar testes específicos
.venv/bin/pytest tests/unit/domain/ -v

# Verificar lint
.venv/bin/ruff check src/

# Verificar tipos
.venv/bin/mypy src/forge_llm/

# Cobertura
.venv/bin/pytest --cov=src --cov-report=term-missing
```

---

## Notas de Continuidade

Se a sessão cair, continuar do sprint marcado como "IN PROGRESS".
Verificar o status atual com:
1. `git status` - ver arquivos modificados
2. `pytest tests/ -q --tb=no | tail -5` - ver se testes passam
3. Ler este arquivo para ver o progresso
