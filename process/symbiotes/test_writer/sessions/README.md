# Sessões do Test Writer

Este diretório armazena os **registros internos de execução** do agente Test Writer.

## Propósito

Cada arquivo aqui representa uma sessão de implementação TDD conduzida pelo Test Writer. Estes são registros **internos e privados** do agente, diferentemente das sessões formais do projeto.

## Formato

Arquivos devem seguir o padrão:
```
test_writer_YYYY-MM-DD_<descrição>.md
```

Exemplo:
- `test_writer_2025-11-25_chat-feature-red-green-refactor.md`
- `test_writer_2025-11-25_retry-after-bill-review-feedback.md`
- `test_writer_2025-11-25_escalation-to-human.md`

## Conteúdo das Sessões

Cada sessão cognitiva registra:

### 1. Contexto
- Feature sendo implementada
- Iteração atual (1/3, 2/3, 3/3)
- Resultado da última validação (se houver)

### 2. Ciclo TDD
- **RED Phase**: Quais testes foram escritos, por quê, como falharam
- **GREEN Phase**: Implementação realizada, decisões de design
- **REFACTOR Phase**: Melhorias aplicadas, justificativas

### 3. Auto-Check
- Resultado de cada verificação interna
- Valores encontrados (hardcoded, coverage, etc.)
- Ações tomadas se falhou

### 4. Bill Review
- Score recebido
- Feedback detalhado
- Issues identificados
- Plano de correção (se rejeitado)

### 5. Decisão Final
- Aprovado: dados do commit
- Rejeitado: feedback incorporado
- Escalado: contexto para humano

## Diferença entre Sessions

| Local | Tipo | Público |
|-------|------|---------|
| `symbiotes/test_writer/sessions/` | Interno | Agente |
| `project/docs/sessions/test_writer/` | Formal/Oficial | Stakeholders e Time |

As sessões internas (aqui) contêm:
- Raciocínio detalhado sobre implementação
- Decisões de design e trade-offs
- Análise de falhas e correções
- Loop de feedback com bill_review
- Tentativas de melhoria iterativa

As sessões formais (no projeto) contêm:
- Resumo executivo das implementações
- Features completadas
- Commits realizados
- Métricas de qualidade finais

## Exemplo de Sessão Interna

```markdown
# Test Writer Session - Chat Feature

**Data**: 2025-11-25
**Feature**: specs/bdd/10_forge_core/chat.feature
**Iteração**: 1/3

## Contexto
- 2 cenários BDD identificados
- Skeleton criado pelo bdd_coach
- Primeira tentativa de implementação

## RED Phase
Implementei 7 step definitions:
- `forge_with_echo()`: Configurar ForgeClient com echo
- `send_message()`: Enviar mensagem
- `check_response()`: Validar resposta
- ...

Testes executados: 7 FAILED ✅
Motivo: ImportError (módulo forge.client não existe)

## GREEN Phase
Implementação:
1. Criado `src/forge/client.py`
2. Implementado `ForgeClient` básico
3. Implementado `EchoProvider`

Testes executados: 7 PASSED ✅

## REFACTOR Phase
Melhorias:
1. Extraído `ProviderRegistry`
2. Criada interface `Provider`
3. Simplificado `ForgeClient.__init__()`

Testes executados: 7 PASSED ✅ (após refactor)

## Auto-Check
✅ Diversidade: 7 testes
✅ Lógica genérica: 0 hardcoded
✅ Cobertura BDD: 2/2 cenários
✅ Cobertura código: 92.3%
✅ Testes: Todos passam

## Bill Review
Score: 9/10 ✅
Feedback: "Código limpo, testes robustos"

## Decisão
✅ APROVADO - Feature implementada com sucesso
Commit: abc1234 "feat: Implement chat.feature scenarios"
```

Consulte o README.md principal para mais detalhes sobre a arquitetura TDD.
