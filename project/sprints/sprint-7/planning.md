# Sprint 7 - Error Handling & Retry

## Objetivo
Implementar tratamento robusto de erros e retry com backoff exponencial para chamadas de API.

## Escopo

### Funcionalidades
1. **Retry com Backoff Exponencial**
   - Configuracao de max_retries (default: 3)
   - Backoff exponencial com jitter
   - Retry apenas para erros transientes (rate limit, timeout, server errors)

2. **Tratamento de Erros de API**
   - Rate Limit (429) - retry com backoff
   - Timeout - retry com backoff
   - Authentication (401/403) - falha imediata, sem retry
   - Server Errors (5xx) - retry com backoff
   - Client Errors (4xx exceto 429) - falha imediata

3. **Exceptions Customizadas**
   - `RateLimitError` - quando rate limit excedido apos retries
   - `AuthenticationError` - credenciais invalidas
   - `APITimeoutError` - timeout apos retries
   - `APIError` - erro generico de API

4. **Configuracao no Client**
   - `max_retries` - numero maximo de tentativas
   - `timeout` - timeout por request
   - `retry_delay` - delay inicial entre retries

## Criterios de Aceite
- [ ] Retry automatico para erros 429 e 5xx
- [ ] Backoff exponencial com jitter
- [ ] Exceptions especificas para cada tipo de erro
- [ ] Configuracao via Client
- [ ] Testes unitarios para retry logic
- [ ] Testes BDD para cenarios de erro
- [ ] Cobertura >= 80%

## Arquivos a Criar/Modificar
- `src/forge_llm/domain/exceptions.py` - novas exceptions
- `src/forge_llm/infrastructure/retry.py` - retry logic
- `src/forge_llm/client.py` - adicionar configuracao de retry
- `src/forge_llm/providers/*.py` - integrar retry nos providers
- `specs/bdd/10_forge_core/error_handling.feature` - cenarios BDD
- `tests/bdd/test_error_handling_steps.py` - steps BDD
- `tests/unit/infrastructure/test_retry.py` - testes unitarios

## Dependencias
- Nenhuma nova dependencia externa (usar asyncio nativo)
