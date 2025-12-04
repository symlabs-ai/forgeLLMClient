# Sprint 11 - Planning

**Data**: 2025-12-04
**Objetivo**: Melhorias Tecnicas - Aumentar cobertura e qualidade de codigo

---

## 1. Objetivo

Melhorar a qualidade tecnica do ForgeLLMClient:
- Aumentar cobertura de testes de 94.06% para 95%+
- Adicionar validacao de formato de modelo no OpenRouter
- Usar modelos gratuitos nos testes de integracao
- Extrair constantes e melhorar organizacao do codigo

---

## 2. Metricas Iniciais

| Metrica | Valor |
|---------|-------|
| Testes | 345 |
| Cobertura | 94.06% |
| BDD Scenarios | 60 |
| Providers | 7 |

---

## 3. Entregas Planejadas

### 3.1 Aumentar Cobertura de Testes

**Arquivos com gaps identificados (Bill Review Sprint 10):**

| Arquivo | Cobertura | Linhas nao cobertas |
|---------|-----------|---------------------|
| openrouter_provider.py | 92% | 146->143, 194-195, 330, 333, 354-361 |

**Acoes:**
- [ ] Adicionar testes para branches de erro
- [ ] Testar cenarios de falha de API
- [ ] Testar timeout e connection errors

### 3.2 Validacao de Formato de Modelo no OpenRouter

Modelos OpenRouter usam formato `provider/model` (ex: "openai/gpt-4o-mini").

**Implementacao:**
```python
def _validate_model(self, model: str) -> None:
    """Validar formato do modelo OpenRouter."""
    if "/" not in model:
        import warnings
        warnings.warn(
            f"Modelo '{model}' nao segue formato OpenRouter (provider/model)",
            UserWarning
        )
```

### 3.3 Extrair Constantes

Conforme sugerido pelo Bill:
```python
# Constantes no OpenRouterProvider
DEFAULT_MODEL = "openai/gpt-4o-mini"
BASE_URL = "https://openrouter.ai/api/v1"
```

### 3.4 Testes com Modelos Gratuitos

Usar modelos gratuitos do OpenRouter para testes de integracao:
- `meta-llama/llama-3.1-8b-instruct:free`
- `google/gemini-2.0-flash-exp:free`
- `qwen/qwen-2-7b-instruct:free`

---

## 4. Criterios de Aceite

- [ ] Cobertura >= 95%
- [ ] Todos os testes passando
- [ ] Validacao de modelo OpenRouter implementada
- [ ] Constantes extraidas
- [ ] Testes de integracao com modelo gratuito
- [ ] Documentacao atualizada

---

## 5. Arquivos a Modificar

### Modificar
- `src/forge_llm/providers/openrouter_provider.py`
- `tests/unit/providers/test_openrouter_provider.py`
- `tests/integration/test_openrouter_integration.py`

### Criar
- `project/sprints/sprint-11/planning.md` (este arquivo)
- `project/sprints/sprint-11/progress.md`

---

## 6. Riscos

| Risco | Mitigacao |
|-------|-----------|
| Modelo gratuito pode estar indisponivel | Usar skip se falhar por disponibilidade |
| Branches de erro dificeis de testar | Usar mocks detalhados |

---

## 7. Estimativa de Trabalho

| Item | Complexidade |
|------|-------------|
| Testes de cobertura | Media |
| Validacao de modelo | Baixa |
| Constantes | Baixa |
| Modelo gratuito | Baixa |

---

**Criado por**: Team
**Data**: 2025-12-04
