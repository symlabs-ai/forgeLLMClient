# Sprint 6 - Testes de Integração Real

## Objetivo
Implementar testes de integração real com OpenAI e Anthropic APIs, validando comportamento end-to-end com API keys reais.

## Escopo

### Entregaveis
1. **Testes de Integração OpenAI**
   - Chat básico com API real
   - Streaming com API real
   - Tool calling com API real
   - Validação de tokens reais

2. **Testes de Integração Anthropic**
   - Chat básico com API real
   - Streaming com API real
   - Tool calling com API real
   - Validação de tokens reais

3. **Infraestrutura de Testes**
   - Marker @integration para testes com API real
   - Skip automático se API key não disponível
   - Configuração de pytest para separar ci-fast de integration

### Criterios de Aceitacao
- [ ] Testes de integração OpenAI passando (quando API key disponível)
- [ ] Testes de integração Anthropic passando (quando API key disponível)
- [ ] Marker @integration configurado
- [ ] Testes @integration skipped se API key não disponível
- [ ] Cobertura >= 80%
- [ ] Lint sem erros

## Cenarios de Teste

### OpenAI Integration
| Cenario | Tag | Descricao |
|---------|-----|-----------|
| 1 | @integration | Chat básico retorna resposta válida |
| 2 | @integration @streaming | Streaming retorna chunks válidos |
| 3 | @integration @tools | Tool calling funciona corretamente |
| 4 | @integration | Tokens são retornados corretamente |

### Anthropic Integration
| Cenario | Tag | Descricao |
|---------|-----|-----------|
| 1 | @integration | Chat básico retorna resposta válida |
| 2 | @integration @streaming | Streaming retorna chunks válidos |
| 3 | @integration @tools | Tool calling funciona corretamente |
| 4 | @integration | Tokens são retornados corretamente |

## Decisoes Tecnicas

### Estrutura de Testes
- Diretório: `tests/integration/`
- Marker: `@pytest.mark.integration`
- Skip: `pytest.mark.skipif(not has_api_key, reason="API key not available")`

### Configuração pytest
- `pytest.ini` ou `pyproject.toml`: definir marker integration
- Comando ci-fast: `pytest -m "not integration"`
- Comando integration: `pytest -m integration`

## Riscos
| Risco | Mitigacao |
|-------|-----------|
| API keys expostas em logs | Nunca logar API keys |
| Rate limits | Usar poucos testes, respostas curtas |
| Custos de API | Usar modelos mais baratos (gpt-4o-mini, claude-haiku) |
| Testes flaky | Retry logic, timeouts adequados |

## Dependencias
- Sprint 5 completa
- .env com OPENAI_API_KEY e ANTHROPIC_API_KEY
