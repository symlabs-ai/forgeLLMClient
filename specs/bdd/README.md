# Especificacoes BDD — ForgeLLMClient

Este diretorio contem as especificacoes de comportamento do ForgeLLMClient em formato Gherkin (PT-BR).

## Estrutura

```
specs/bdd/
├── README.md                    # Este arquivo
├── 00_glossario.md              # Linguagem ubiqua
├── tracks.yml                   # Mapeamento features → ValueTracks
├── HANDOFF.md                   # Instrucoes para DEV
│
├── drafts/                      # Rascunhos e mapeamentos
│   └── behavior_mapping.md      # Mapeamento de comportamentos
│
├── 10_forge_core/               # Nucleo do SDK
│   ├── chat.feature             # Chat basico (sync/streaming)
│   ├── config.feature           # Configuracao de provedor
│   ├── tools.feature            # Tool Calling unificado
│   ├── tokens.feature           # Contagem de tokens
│   └── response.feature         # Formato de resposta
│
└── 30_providers/                # Provedores especificos
    ├── openai.feature           # Integracao OpenAI
    └── anthropic.feature        # Integracao Anthropic
```

## Convencoes

### Idioma
- Features em **Portugues (PT-BR)**
- Tags Gherkin em **MAIUSCULO**: `FUNCIONALIDADE`, `CENARIO`, `DADO`, `QUANDO`, `ENTAO`

### Tags de Dominio
```gherkin
@sdk              # Forge SDK Python
@chat             # Funcionalidades de chat
@config           # Configuracao
@tools            # Tool Calling
@tokens           # Contagem de tokens
@response         # Formato de resposta
@provider         # Provedores especificos
@openai           # Provedor OpenAI
@anthropic        # Provedor Anthropic
```

### Tags de CI
```gherkin
@ci-fast          # Testes rapidos (mocks, sem deps externas)
@ci-int           # Testes de integracao (provedores reais)
@slow             # Testes que podem demorar
@error            # Cenarios de erro
@streaming        # Cenarios com streaming
```

## Executando Testes

```bash
# Todos os testes rapidos
pytest tests/bdd/ -m "ci_fast"

# Testes de integracao (requer API keys)
pytest tests/bdd/ -m "ci_int"

# Feature especifica
pytest tests/bdd/ -k "chat"

# Com verbose
pytest tests/bdd/ -v
```

## Metricas de Cobertura

| Dominio | Features | Cenarios | Status |
|---------|----------|----------|--------|
| 10_forge_core | 5 | 23 | MVP |
| 30_providers | 2 | 14 | MVP |
| **Total** | **7** | **37** | - |

## Relacionamento com MDD

Estas especificacoes derivam dos ValueTracks definidos em:
- `docs/visao.md` — Visao do produto
- `docs/aprovacao_mvp.md` — Escopo do MVP

O mapeamento completo esta em `tracks.yml`.

---

*Ultima atualizacao: 2025-12-03*
