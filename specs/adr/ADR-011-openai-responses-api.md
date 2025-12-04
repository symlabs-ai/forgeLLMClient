# ADR-011: Usar OpenAI Responses API ao inves de Chat Completions

**Status**: ACCEPTED
**Date**: 2025-12-03
**Sprint**: 3
**Decision Makers**: Stakeholder, Team

---

## Context

O OpenAI Provider precisa integrar com a API da OpenAI para fornecer funcionalidades de chat, streaming e tool calling. A OpenAI oferece duas APIs principais:

1. **Chat Completions API** (`client.chat.completions.create()`)
   - API tradicional, amplamente documentada
   - Formato: `messages: [{"role": "user", "content": "..."}]`

2. **Responses API** (`client.responses.create()`)
   - Nova API lancada em Marco 2025
   - Projetada para agentes e aplicacoes complexas
   - Gerenciamento de estado no servidor
   - Formato: `input: [{"type": "message", "role": "user", "content": "..."}]`

O stakeholder requisitou explicitamente que a implementacao usasse a Responses API.

---

## Decision

**Usar a OpenAI Responses API** para todas as interacoes com a OpenAI no ForgeLLMClient.

### Implementacao

```python
# Responses API (o que usamos)
response = await self._client.responses.create(
    model="gpt-4o-mini",
    input=[{"type": "message", "role": "user", "content": "Hello"}],
    instructions="You are a helpful assistant",
    temperature=0.7,
)

# Chat Completions API (o que NAO usamos)
# response = await self._client.chat.completions.create(
#     model="gpt-4o-mini",
#     messages=[{"role": "user", "content": "Hello"}],
#     temperature=0.7,
# )
```

### Diferencas de Formato

| Aspecto | Responses API | Chat Completions API |
|---------|---------------|----------------------|
| Metodo | `responses.create()` | `chat.completions.create()` |
| Input format | `input: [{"type": "message", ...}]` | `messages: [{"role": ..., ...}]` |
| System message | `instructions` parameter | Message com role "system" |
| Max tokens | `max_output_tokens` | `max_tokens` |
| Tool results | `function_call_output` | Message com role "tool" |

---

## Consequences

### Positivas

1. **Melhor suporte para agentes**: A Responses API foi projetada especificamente para aplicacoes de agentes
2. **Gerenciamento de estado**: O servidor gerencia o estado da conversa, simplificando aplicacoes complexas
3. **API mais moderna**: Incorpora aprendizados da Chat Completions API
4. **Alinhamento com stakeholder**: Atende ao requisito explicito do stakeholder

### Negativas

1. **Menos documentacao**: Por ser nova, ha menos exemplos e documentacao disponivel
2. **Formato diferente**: Requer conversao de mensagens para formato especifico
3. **Compatibilidade futura**: API ainda pode evoluir

### Mitigacoes

1. **Testes especificos**: 2 testes unitarios verificam que a Responses API esta sendo usada
2. **Conversao encapsulada**: Metodos privados isolam a logica de conversao de formato
3. **SDK oficial**: Uso do SDK `openai` abstrai mudancas de versao

---

## Alternatives Considered

### Alternativa 1: Chat Completions API

**Pros**:
- Amplamente documentada
- Estavel e bem testada
- Mais exemplos disponiveis

**Cons**:
- Gerenciamento de estado manual
- Nao otimizada para agentes
- Rejeitada pelo stakeholder

**Decisao**: REJEITADA - Stakeholder requisitou explicitamente Responses API

### Alternativa 2: Suportar ambas as APIs

**Pros**:
- Flexibilidade para usuarios
- Compatibilidade retroativa

**Cons**:
- Complexidade de manutencao
- Duplicacao de codigo
- Testes mais complexos

**Decisao**: REJEITADA - Complexidade desnecessaria para o MVP

---

## Verification

A decisao foi verificada atraves de:

1. **Testes unitarios especificos**:
   - `test_openai_provider_uses_responses_api_not_chat_completions`
   - `test_openai_provider_stream_uses_responses_api`

2. **Assercoes de mock**:
   ```python
   # Verifica que responses.create foi chamado
   mock_client.responses.create.assert_called_once()

   # Verifica que chat.completions.create NAO foi chamado
   mock_client.chat.completions.create.assert_not_called()
   ```

---

## References

- [OpenAI Responses API Documentation](https://platform.openai.com/docs/api-reference/responses)
- Sprint 3 Planning: `project/sprints/sprint-3/planning.md`
- Sprint 3 Progress: `project/sprints/sprint-3/progress.md`

---

**Approved by**: Stakeholder
**Implementation**: `src/forge_llm/providers/openai_provider.py`
