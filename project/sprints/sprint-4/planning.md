# Sprint 4 - Anthropic Provider

## Objetivo
Implementar o Anthropic Provider, integrando com a API da Anthropic (Claude) para suportar chat, streaming e tool calling.

## Escopo

### Entregaveis
1. **Anthropic Provider Completo**
   - Integracao real com API da Anthropic
   - Suporte a chat sincrono
   - Suporte a streaming
   - Suporte a tool calling
   - Tratamento de erros (AuthenticationError, RateLimitError)

2. **BDD**
   - Converter anthropic.feature PT -> EN
   - Implementar steps para cenarios de configuracao (ci-fast)
   - Cenarios @slow dependem de API real

3. **Testes Unitarios**
   - Testes com mocking da API Anthropic
   - Testes de error handling
   - Testes de conversao de formatos

### Criterios de Aceitacao
- [x] anthropic.feature convertido para ingles
- [x] Cenarios de configuracao passando (ci-fast)
- [x] AnthropicProvider funcional com anthropic SDK
- [x] Testes unitarios com mocking
- [x] Cobertura >= 80% (90.13%)
- [x] Lint sem erros
- [x] Testado com API real

## Cenarios BDD (anthropic.feature)

| Cenario | Tag | Descricao |
|---------|-----|-----------|
| 1 | ci-fast | Configurar provedor Anthropic com API key |
| 2 | ci-fast | Configurar Anthropic com modelo Claude 3 |
| 3 | ci-fast | Configurar Anthropic com modelo Claude 3.5 |
| 4 | @slow | Enviar mensagem para Claude |
| 5 | @slow @streaming | Streaming com Anthropic |
| 6 | @slow @tools | Tool calling com Anthropic |
| 7 | ci-fast | Resposta Anthropic segue formato unificado |
| 8 | @error | Erro com API key invalida |

## Decisoes Tecnicas

### SDK vs HTTP Direto
- **Decisao:** Usar SDK oficial `anthropic`
- **Razao:** Mais estavel, type hints, retry automatico

### API Anthropic
- Usar Messages API (padrao atual)
- Formato: `client.messages.create()`
- System message via parametro `system`

## Riscos
| Risco | Mitigacao |
|-------|-----------|
| API key exposta em testes | Usar env vars, nunca hardcoded |
| Rate limits | Usar @slow para testes de integracao |
| Mudancas na API Anthropic | Usar SDK oficial que abstrai versoes |

## Dependencias
- Sprint 3 completa (OpenAI Provider)
- Pacote `anthropic` instalado
- ANTHROPIC_API_KEY configurada para testes @slow
