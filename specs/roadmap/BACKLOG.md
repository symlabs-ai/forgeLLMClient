# Backlog — ForgeLLMClient

> **Versao:** 1.0
> **Data:** 2025-12-03
> **Status:** Priorizado

---

## Visao Geral

Este documento contem o backlog priorizado de tarefas para implementacao do ForgeLLMClient, seguindo a metodologia TDD.

---

## Legenda

| Tag | Significado |
|-----|-------------|
| `[P0]` | Prioridade critica |
| `[P1]` | Prioridade alta |
| `[P2]` | Prioridade media |
| `[TDD]` | Requer teste antes |
| `[BDD]` | Vinculado a feature BDD |
| `[SETUP]` | Configuracao/infra |

---

## Sprint 1: Fundacao (P0)

### 1.1 Setup do Projeto [SETUP]

- [ ] **TASK-001**: Criar estrutura de diretorios src/forge_llm
  - Criar pacotes: domain, application, infrastructure, adapters, providers
  - Criar __init__.py em cada pacote
  - Criar py.typed para type hints

- [ ] **TASK-002**: Configurar pyproject.toml
  - Copiar configuracao de TECH_STACK.md
  - Ajustar dependencias
  - Configurar pytest markers

- [ ] **TASK-003**: Configurar ferramentas de qualidade
  - ruff (lint + format)
  - mypy (type check)
  - import-linter (boundaries)
  - pre-commit hooks

### 1.2 Domain Layer [P0] [TDD]

- [ ] **TASK-004**: Implementar Value Objects base
  - [ ] Teste: test_value_objects.py
  - [ ] Codigo: TokenUsage, ToolCall, ToolDefinition
  - Usar ValueObjectBase do ForgeBase

- [ ] **TASK-005**: Implementar Entidades
  - [ ] Teste: test_entities.py
  - [ ] Codigo: Message, ChatResponse, ProviderConfig
  - Usar EntityBase do ForgeBase

- [ ] **TASK-006**: Implementar Exceptions
  - [ ] Teste: test_exceptions.py
  - [ ] Codigo: ForgeLLMError, ProviderError, ConfigError, etc.
  - Usar ExceptionBase do ForgeBase

### 1.3 Application Layer [P0] [TDD]

- [ ] **TASK-007**: Implementar Ports (ABCs)
  - [ ] Teste: test_ports.py
  - [ ] Codigo: ProviderPort, ConfigPort
  - Usar PortBase do ForgeBase

- [ ] **TASK-008**: Implementar DTOs
  - [ ] Teste: test_dtos.py
  - [ ] Codigo: ChatRequest, ChatResult, StreamChunk

### 1.4 config.feature [P0] [BDD]

- [ ] **TASK-009**: Implementar steps para config.feature
  - [ ] Criar tests/bdd/test_config_steps.py
  - [ ] Remover @skip dos cenarios
  - [ ] Implementar ProviderConfig

- [ ] **TASK-010**: Implementar ConfigService
  - [ ] Teste: test_config_service.py
  - [ ] Codigo: Validacao, env vars, fallbacks

### 1.5 chat.feature [P0] [BDD]

- [ ] **TASK-011**: Implementar steps para chat.feature (sync)
  - [ ] Criar tests/bdd/test_chat_steps.py
  - [ ] Cenarios sync passando

- [ ] **TASK-012**: Implementar steps para chat.feature (streaming)
  - [ ] Cenarios streaming passando
  - [ ] AsyncIterator funcional

---

## Sprint 2: MockProvider + Features (P0)

### 2.1 MockProvider [P0] [TDD]

- [ ] **TASK-013**: Implementar MockProvider
  - [ ] Teste: test_mock_provider.py
  - [ ] Codigo: MockProvider com respostas configuraveis
  - Suportar: chat, streaming, tools

### 2.2 response.feature [P0] [BDD]

- [ ] **TASK-014**: Implementar steps para response.feature
  - [ ] Criar tests/bdd/test_response_steps.py
  - [ ] Validar estrutura ChatResponse
  - [ ] Validar campos obrigatorios

### 2.3 tokens.feature [P0] [BDD]

- [ ] **TASK-015**: Implementar steps para tokens.feature
  - [ ] Criar tests/bdd/test_tokens_steps.py
  - [ ] Contagem de tokens funcional
  - [ ] TokenUsage correto

### 2.4 tools.feature [P0] [BDD]

- [ ] **TASK-016**: Implementar steps para tools.feature
  - [ ] Criar tests/bdd/test_tools_steps.py
  - [ ] ToolDefinition funcional
  - [ ] ToolCall na resposta

- [ ] **TASK-017**: Implementar ToolRegistry
  - [ ] Teste: test_tool_registry.py
  - [ ] Registro e validacao de tools

---

## Sprint 3: OpenAI Provider (P1)

### 3.1 openai.feature [P1] [BDD]

- [ ] **TASK-018**: Implementar OpenAIProvider
  - [ ] Teste: test_openai_provider.py (mock)
  - [ ] Codigo: OpenAIProvider usando Responses API
  - **CRITICO**: Usar APENAS Responses API, NUNCA ChatCompletions

- [ ] **TASK-019**: Implementar steps para openai.feature
  - [ ] Criar tests/bdd/test_openai_steps.py
  - [ ] Testes com mock

- [ ] **TASK-020**: Testes de integracao OpenAI
  - [ ] Criar tests/integration/test_openai_real.py
  - [ ] Marker @ci_int
  - [ ] Testar com API real

### 3.2 OpenAI Responses API [P1] [TDD]

- [ ] **TASK-021**: Implementar mapeamento Responses API
  - [ ] Teste: test_openai_mapping.py
  - [ ] Request → Responses API format
  - [ ] Response → ChatResponse

- [ ] **TASK-022**: Implementar streaming OpenAI
  - [ ] Teste: test_openai_streaming.py
  - [ ] SSE parsing
  - [ ] AsyncIterator

---

## Sprint 4: Anthropic Provider (P1)

### 4.1 anthropic.feature [P1] [BDD]

- [ ] **TASK-023**: Implementar AnthropicProvider
  - [ ] Teste: test_anthropic_provider.py (mock)
  - [ ] Codigo: AnthropicProvider

- [ ] **TASK-024**: Implementar steps para anthropic.feature
  - [ ] Criar tests/bdd/test_anthropic_steps.py
  - [ ] Testes com mock

- [ ] **TASK-025**: Testes de integracao Anthropic
  - [ ] Criar tests/integration/test_anthropic_real.py
  - [ ] Marker @ci_int
  - [ ] Testar com API real

### 4.2 Anthropic Messages API [P1] [TDD]

- [ ] **TASK-026**: Implementar mapeamento Messages API
  - [ ] Teste: test_anthropic_mapping.py
  - [ ] Request → Messages API format
  - [ ] Response → ChatResponse

- [ ] **TASK-027**: Implementar streaming Anthropic
  - [ ] Teste: test_anthropic_streaming.py
  - [ ] SSE parsing
  - [ ] AsyncIterator

---

## Sprint 5: Recursos Avancados (P2)

### 5.1 AutoFallbackProvider [P2] [TDD]

- [ ] **TASK-028**: Implementar AutoFallbackProvider
  - [ ] Teste: test_autofallback.py
  - [ ] Chain de providers
  - [ ] Fallback em erro

### 5.2 MCP Client [P2] [TDD]

- [ ] **TASK-029**: Implementar MCP Client base
  - [ ] Teste: test_mcp_client.py
  - [ ] Protocolo MCP
  - [ ] Tool discovery

- [ ] **TASK-030**: Integrar MCP com providers
  - [ ] Teste: test_mcp_integration.py
  - [ ] Tools do MCP disponiveis para providers

### 5.3 Documentacao [P2]

- [ ] **TASK-031**: Criar documentacao de uso
  - [ ] README.md atualizado
  - [ ] Exemplos de uso
  - [ ] API reference

---

## Criterios de Aceitacao por Task

### Padrao TDD

Cada task [TDD] deve seguir:

1. **Teste escrito primeiro** - antes de qualquer codigo
2. **Teste deve falhar** - RED
3. **Implementar minimo** - GREEN
4. **Refatorar** - REFACTOR
5. **Cobertura** - >= 80% para a task

### Padrao BDD

Cada task [BDD] deve seguir:

1. **Feature ja existe** em specs/bdd/
2. **Remover @skip** do cenario
3. **Rodar teste** - deve falhar
4. **Implementar steps**
5. **Implementar codigo**
6. **Teste deve passar**

---

## Ordem de Execucao

```
TASK-001 → TASK-002 → TASK-003 (Setup paralelo)
    ↓
TASK-004 → TASK-005 → TASK-006 (Domain sequencial)
    ↓
TASK-007 → TASK-008 (Application sequencial)
    ↓
TASK-009 → TASK-010 (config.feature)
    ↓
TASK-011 → TASK-012 (chat.feature)
    ↓
TASK-013 (MockProvider)
    ↓
TASK-014, TASK-015, TASK-016, TASK-017 (Features paralelas)
    ↓
TASK-018 → TASK-019 → TASK-020 → TASK-021 → TASK-022 (OpenAI)
    ↓
TASK-023 → TASK-024 → TASK-025 → TASK-026 → TASK-027 (Anthropic)
    ↓
TASK-028 → TASK-029 → TASK-030 → TASK-031 (Avancados)
```

---

## Metricas de Qualidade

| Metrica | Minimo | Alvo |
|---------|--------|------|
| Cobertura total | 80% | 90% |
| Domain coverage | 95% | 100% |
| Application coverage | 90% | 95% |
| Testes BDD passando | 100% | 100% |
| Lint errors | 0 | 0 |
| Type errors | 0 | 0 |

---

## Referencias

- `specs/roadmap/ROADMAP.md` - Visao executiva
- `specs/roadmap/dependency_graph.md` - Dependencias entre features
- `specs/bdd/*.feature` - Especificacoes BDD
- `specs/roadmap/LLD.md` - Design detalhado

---

*Documento gerado pelo Roadmap Planning Process*
