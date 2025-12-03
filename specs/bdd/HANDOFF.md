# Handoff BDD → Execution — ForgeLLMClient

> **Data:** 2025-12-03
> **Status:** Pronto para Roadmap Planning e TDD
> **Versao:** 1.0

---

## 1. O Que Foi Especificado

### Features Gherkin Criadas

| Dominio | Feature | Cenarios | Tags |
|---------|---------|----------|------|
| 10_forge_core | chat.feature | 6 | @sdk @chat @ci-fast |
| 10_forge_core | config.feature | 6 | @sdk @config @ci-fast |
| 10_forge_core | tools.feature | 6 | @sdk @tools @ci-fast |
| 10_forge_core | tokens.feature | 4 | @sdk @tokens @ci-fast |
| 10_forge_core | response.feature | 4 | @sdk @response @ci-fast |
| 30_providers | openai.feature | 7 | @sdk @provider @openai @ci-int |
| 30_providers | anthropic.feature | 7 | @sdk @provider @anthropic @ci-int |
| **Total** | **7 features** | **40 cenarios** | - |

### Documentos de Referencia

- **Mapeamento de Comportamentos:** `specs/bdd/drafts/behavior_mapping.md`
- **Rastreabilidade:** `specs/bdd/tracks.yml`
- **Linguagem Ubiqua:** `specs/bdd/00_glossario.md`
- **Guia de Uso:** `specs/bdd/README.md`

---

## 2. Visao Geral dos Comportamentos

### Dominio: Forge Core SDK

O nucleo do SDK que todo desenvolvedor usara:

| Capacidade | Descricao | Prioridade |
|------------|-----------|------------|
| **Chat Sync** | Enviar mensagem e receber resposta completa | Alta |
| **Chat Streaming** | Receber resposta em chunks progressivos | Alta |
| **Configuracao** | Configurar provedor, modelo, API key | Alta |
| **Tool Calling** | Registrar tools, receber/responder tool calls | Alta |
| **Tokens** | Informar consumo de tokens | Alta |
| **Normalizacao** | Formato de resposta unificado | Alta |

### Dominio: Provedores

Integracoes com provedores especificos:

| Provedor | Modelos | Features |
|----------|---------|----------|
| **OpenAI** | gpt-4, gpt-3.5-turbo | chat, streaming, tools |
| **Anthropic** | claude-3-sonnet, claude-3-5-sonnet | chat, streaming, tools |

---

## 3. Comportamentos Criticos

### Alta Complexidade Tecnica

1. **Tool Calling Normalizado**
   - Converter formato OpenAI → interno
   - Converter formato Anthropic → interno
   - Manter consistencia de IDs

2. **Streaming Unificado**
   - Normalizar chunks de diferentes provedores
   - Garantir informacao de tokens ao final

3. **Tratamento de Erros**
   - Normalizar erros de diferentes provedores
   - Manter informacoes uteis (rate limit, auth, etc)

### Decisoes Arquiteturais Necessarias

- [ ] Estrutura de tipos (ChatResponse, ChatResponseChunk, etc)
- [ ] Interface de Provider (protocolo/ABC)
- [ ] Sistema de registro de tools
- [ ] Gerenciamento de configuracao

---

## 4. Skeleton de Automacao

### Estrutura Criada

```
tests/bdd/
├── conftest.py          # Fixtures pytest
├── test_chat_steps.py   # Steps para chat.feature
└── test_tools_steps.py  # Steps para tools.feature

pytest.ini               # Configuracao pytest + markers
```

### Como Executar (apos implementacao)

```bash
# Testes rapidos (mocks)
pytest tests/bdd/ -m "ci_fast"

# Testes de integracao
pytest tests/bdd/ -m "ci_int"

# Feature especifica
pytest tests/bdd/ -k "chat"
```

---

## 5. Proximo Passo: Execution Phase

Este handoff autoriza o inicio da fase de **Execution**, que inclui:

### 5.1 Roadmap Planning

1. **Definir Tech Stack** — Python, dependencias, estrutura
2. **Criar ADRs** — Decisoes arquiteturais
3. **HLD/LLD** — Design de alto e baixo nivel
4. **Backlog** — Lista priorizada de tarefas

### 5.2 TDD

1. **Implementar Core** — Tipos, interfaces, cliente
2. **Implementar Provedores** — OpenAI, Anthropic
3. **Remover @skip** — Habilitar testes conforme implementa
4. **Cobertura >= 80%** — Garantir qualidade

---

## 6. Metricas de Sucesso do BDD

| Criterio | Status |
|----------|--------|
| Todos ValueTracks do MVP tem features | OK |
| Cada feature tem cenarios de sucesso e erro | OK |
| Tags de CI aplicadas | OK |
| Rastreabilidade em tracks.yml | OK |
| Glossario de linguagem ubiqua | OK |
| Skeleton de automacao criado | OK |

---

## 7. Contato

Para duvidas sobre as especificacoes:
- Consultar `specs/bdd/00_glossario.md` para termos
- Consultar `specs/bdd/README.md` para estrutura
- Consultar `docs/visao.md` para contexto de negocio

---

*Documento gerado pelo BDD Coach*
*Handoff autorizado em: 2025-12-03*
