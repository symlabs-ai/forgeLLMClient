# Sprint 3 - OpenAI Provider

## Objetivo
Implementar o OpenAI Provider real, substituindo o stub atual por uma integracao funcional com a API da OpenAI, suportando chat, streaming e tool calling.

## Escopo

### Entregaveis
1. **OpenAI Provider Completo**
   - Integracao real com API da OpenAI
   - Suporte a chat sincrono
   - Suporte a streaming
   - Suporte a tool calling
   - Tratamento de erros (AuthenticationError, RateLimitError)

2. **BDD**
   - Converter openai.feature PT -> EN
   - Implementar steps para cenarios de configuracao (ci-fast)
   - Cenarios @slow dependem de API real

3. **Testes Unitarios**
   - Testes com mocking da API OpenAI
   - Testes de error handling
   - Testes de conversao de formatos

### Criterios de Aceitacao
- [x] openai.feature convertido para ingles
- [x] Cenarios de configuracao passando (ci-fast)
- [x] OpenAIProvider funcional com openai SDK (Responses API)
- [x] Testes unitarios com mocking
- [x] Cobertura >= 80% (89.83%)
- [x] Lint sem erros

## Cenarios BDD

| Cenario | Tag | Descricao |
|---------|-----|-----------|
| 1 | ci-fast | Configurar provedor OpenAI com API key |
| 2 | ci-fast | Configurar OpenAI com modelo especifico |
| 3 | ci-fast | Configurar OpenAI com modelo GPT-3.5 |
| 4 | @slow | Enviar mensagem para GPT-4 |
| 5 | @slow @streaming | Streaming com OpenAI |
| 6 | @slow @tools | Tool calling com OpenAI |
| 7 | @error | Erro com API key invalida |

## Decisoes Tecnicas

### SDK vs HTTP Direto
- **Decisao:** Usar SDK oficial `openai`
- **Razao:** Mais estavel, type hints, retry automatico

### Estrutura de Testes
- Cenarios @slow requerem API key real
- Cenarios ci-fast usam mocks
- Testes unitarios mocam completamente a API

## Riscos
| Risco | Mitigacao |
|-------|-----------|
| API key exposta em testes | Usar env vars, nunca hardcoded |
| Rate limits | Usar @slow para testes de integracao |
| Mudancas na API OpenAI | Usar SDK oficial que abstrai versoes |

## Dependencias
- Sprint 2 completa (Tool Calling)
- Pacote `openai` instalado
- OPENAI_API_KEY configurada para testes @slow
