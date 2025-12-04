# Sprint 2 - Tool Calling

## Objetivo
Implementar suporte a Tool Calling unificado, permitindo registro de ferramentas e processamento de tool_calls de forma padronizada independente do provider.

## Escopo

### Entregaveis
1. **Domain Layer**
   - ToolCallNotFoundError exception

2. **Providers**
   - MockToolsProvider (mock que simula tool calls)

3. **Client Extensions**
   - register_tool() - registrar ferramentas
   - submit_tool_result() - enviar resultado de tool call
   - tools property - listar ferramentas registradas

4. **BDD**
   - Converter tools.feature PT -> EN
   - Implementar todos os steps (6 cenarios)

### Criterios de Aceitacao
- [ ] tools.feature convertido para ingles
- [ ] 6 cenarios BDD implementados e passando
- [ ] MockToolsProvider funcional
- [ ] Testes unitarios para novas funcionalidades
- [ ] Cobertura >= 80%
- [ ] Lint sem erros

## Cenarios BDD

| Cenario | Descricao |
|---------|-----------|
| 1 | Registrar ferramentas para o LLM |
| 2 | Receber solicitacao de tool call |
| 3 | Enviar resultado de tool call |
| 4 | Multiplos tool calls em uma resposta |
| 5 | Erro ao registrar ferramenta sem nome |
| 6 | Erro ao enviar resultado para tool_call inexistente |

## Riscos
| Risco | Mitigacao |
|-------|-----------|
| Complexidade de tool call flow | Usar MockToolsProvider simples |
| Estado de tool calls pendentes | Gerenciar no Client |

## Dependencias
- Sprint 1 completa (Domain, Client, MockProvider)
