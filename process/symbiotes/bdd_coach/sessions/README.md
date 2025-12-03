# Sessões do BDD Coach

Este diretório armazena os **registros internos de raciocínio** do agente BDD Coach.

## Propósito

Cada arquivo aqui representa uma sessão de análise e especificação conduzida pelo Coach durante o processo BDD. Estes são registros **internos e privados** do agente, diferentemente das sessões formais do projeto.

## Formato

Arquivos devem seguir o padrão:
```
coach_YYYY-MM-DD_<descrição>.md
```

Exemplo:
- `coach_2025-11-25_mapeamento-behaviors-chat.md`
- `coach_2025-11-25_derivacao-support-tracks.md`
- `coach_2025-11-25_escrita-features-value.md`

## Diferença entre Sessions

| Local | Tipo | Público |
|-------|------|---------|
| `symbiotas/bdd_coach/sessions/` | Interno | Agente |
| `project/docs/sessions/bdd_coach/` | Formal/Oficial | Stakeholders e Time |

As sessões internas (aqui) contêm:
- Raciocínio sobre derivação de behaviors
- Análise de dependências VALUE ↔ SUPPORT
- Decisões sobre priorização de SupportTracks
- Rascunhos e iterações de features

As sessões formais (no projeto) contêm:
- Diálogos com stakeholders
- Validações de features
- Aprovações de handoffs
- Registros de decisões formais

Consulte o README.md principal para mais detalhes sobre a arquitetura BDD.
