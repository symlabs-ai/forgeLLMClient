# Sprint 10 - OpenRouter Integration

**Data Inicio**: 2025-12-04
**Status**: Em Andamento

---

## 1. Objetivo

Implementar provider para OpenRouter, permitindo acesso a 400+ modelos LLM atraves de uma API unificada OpenAI-compatible.

---

## 2. Escopo

### Incluido
- OpenRouterProvider com Chat Completions API
- Suporte a streaming
- Suporte a tool calling
- Suporte a imagens (Vision)
- Headers opcionais (HTTP-Referer, X-Title)
- Testes unitarios e BDD
- Registro no provider registry

### Excluido
- Provider routing avancado
- Fallback automatico entre providers
- Cache de respostas

---

## 3. Design Tecnico

### 3.1 Arquitetura

```
Client --> ProviderRegistry --> OpenRouterProvider
                                     |
                                     v
                              AsyncOpenAI (SDK)
                                     |
                                     v
                            OpenRouter API (v1)
                                     |
                                     v
                              400+ LLM Models
```

### 3.2 Decisao de Implementacao

**Abordagem**: Usar OpenAI SDK com `base_url` customizada

**Justificativa**:
1. OpenRouter e 100% OpenAI Chat Completions compatible
2. SDK ja tem tratamento de erros, retries, streaming
3. Menos codigo para manter
4. Testado e estavel

### 3.3 Diferenca de API

| Aspecto | OpenAI Provider (atual) | OpenRouter Provider |
|---------|------------------------|---------------------|
| API | Responses API | Chat Completions API |
| System | `instructions` param | Message com role="system" |
| Tools | `function_call` | `tools` array |
| Endpoint | `/responses` | `/chat/completions` |

### 3.4 Configuracao

```python
AsyncOpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1",
    default_headers={
        "HTTP-Referer": site_url,  # opcional
        "X-Title": site_name,      # opcional
    }
)
```

---

## 4. Tarefas

### 4.1 Implementacao
- [ ] `openrouter_provider.py` - Provider principal
- [ ] Registrar no `registry.py`
- [ ] Export no `__init__.py`

### 4.2 Testes
- [ ] `openrouter.feature` - BDD scenarios
- [ ] `test_openrouter_steps.py` - BDD steps
- [ ] `test_openrouter_provider.py` - Unit tests
- [ ] `test_openrouter_integration.py` - Integration tests

### 4.3 Documentacao
- [ ] planning.md (este documento)
- [ ] progress.md
- [ ] retrospective.md

---

## 5. Metricas de Entrada

| Metrica | Valor |
|---------|-------|
| Testes | 307 |
| Cobertura | 94.32% |
| BDD Scenarios | 54 |

---

## 6. Criterios de Aceite

1. Provider registrado e funcional
2. Chat basico funcionando
3. Streaming funcionando
4. Tool calling funcionando
5. Imagens (Vision) funcionando
6. Testes passando (>90% cobertura)
7. BDD scenarios passando

---

## 7. Riscos

| Risco | Mitigacao |
|-------|-----------|
| API key de teste | Usar modelo free tier |
| Rate limiting | Testes de integracao com skip |
| Formato de resposta diferente | Testes unitarios com mocks |

---

## 8. Referencias

- [OpenRouter Quickstart](https://openrouter.ai/docs/quickstart)
- [OpenRouter API Parameters](https://openrouter.ai/docs/api/reference/parameters)
- [Guia de Providers](../../docs/guides/creating-providers.md)
