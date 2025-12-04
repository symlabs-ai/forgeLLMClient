# Sprint 5 - Token Counting & Response Format

## Objetivo
Implementar contagem de tokens e validar formato unificado de resposta para todos os providers.

## Escopo

### Entregaveis
1. **Token Counting**
   - Converter tokens.feature PT -> EN
   - Implementar BDD steps para tokens
   - Garantir que ChatResponse.tokens funciona em todos os providers
   - MockProvider retorna tokens simulados

2. **Response Format**
   - Converter response.feature PT -> EN
   - Implementar BDD steps para response
   - Validar formato unificado entre providers
   - Validar ChatResponseChunk para streaming

3. **Validacao Cross-Provider**
   - Testar que OpenAI e Anthropic retornam formato identico
   - Validar consistencia de tokens

### Criterios de Aceitacao
- [x] tokens.feature convertido para ingles
- [x] response.feature convertido para ingles
- [x] Cenarios BDD de tokens passando (4/4)
- [x] Cenarios BDD de response passando (4/4)
- [x] Cobertura >= 80% (89.14%)
- [x] Lint sem erros

## Cenarios BDD

### tokens.feature (4 cenarios)
| Cenario | Tag | Descricao |
|---------|-----|-----------|
| 1 | @sync | Receber contagem de tokens na resposta sincrona |
| 2 | @streaming | Receber contagem de tokens apos streaming |
| 3 | ci-fast | Tokens zerados quando provedor nao informa |
| 4 | ci-fast | Tokens consistentes entre chamadas |

### response.feature (4 cenarios)
| Cenario | Tag | Descricao |
|---------|-----|-----------|
| 1 | ci-fast | Resposta tem formato ChatResponse unificado |
| 2 | ci-fast | Metadados do provedor na resposta |
| 3 | ci-fast | Formato identico entre provedores diferentes |
| 4 | @streaming | Chunks de streaming tem formato padronizado |

## Decisoes Tecnicas

### Token Counting
- OpenAI: `usage.prompt_tokens`, `usage.completion_tokens`
- Anthropic: `usage.input_tokens`, `usage.output_tokens`
- Mock: Retorna valores simulados

### Response Format
- ChatResponse: content, role, provider, model, tokens, tool_calls
- ChatResponseChunk: delta, index, finish_reason

## Riscos
| Risco | Mitigacao |
|-------|-----------|
| Providers retornam tokens diferentes | Normalizar para formato unico |
| Streaming nao retorna tokens | Retornar None/0 quando nao disponivel |

## Dependencias
- Sprint 4 completa (OpenAI + Anthropic providers)
- MockProvider com suporte a tokens
