# Sprint 1 - Foundation

## Objetivo
Estabelecer a fundacao do ForgeLLMClient SDK com arquitetura limpa, domain layer completo e infraestrutura de testes.

## Escopo

### Entregaveis
1. **Domain Layer**
   - Entities: ChatResponse, ToolCall
   - Value Objects: Message, TokenUsage, ToolDefinition
   - Exceptions: ForgeError, ValidationError, ProviderError, AuthenticationError, RateLimitError, ConfigurationError, ToolNotFoundError

2. **Application Layer**
   - ProviderPort (interface ABC para providers)

3. **Providers**
   - MockProvider (para testes)
   - OpenAIProvider (stub inicial)
   - ProviderRegistry (gerenciamento de providers)

4. **Client**
   - Client facade com chat() e chat_stream()
   - Validacao de mensagens vazias
   - Suporte a configuracao dinamica

5. **Testes**
   - Unit tests TDD (76 testes)
   - BDD steps para config.feature (6 cenarios)
   - BDD steps para chat.feature (6 cenarios)

### Criterios de Aceitacao
- [ ] Todos os testes passando
- [ ] Cobertura >= 80%
- [ ] Lint sem erros (ruff)
- [ ] BDD config.feature implementado
- [ ] BDD chat.feature implementado

## Riscos Identificados
| Risco | Mitigacao |
|-------|-----------|
| pytest-bdd nao suporta PT | Converter features para EN |
| Complexidade de async | Usar run_async helper nos BDD steps |

## Dependencias
- Python 3.12+
- pytest, pytest-bdd, pytest-asyncio, pytest-cov
- ruff (linting)
- httpx (futuro - chamadas HTTP)

## Timeline
- Inicio: Sprint 1
- Fim: Sprint 1 (concluida)
