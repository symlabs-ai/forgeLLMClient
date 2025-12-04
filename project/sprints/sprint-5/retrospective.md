# Sprint 5 - Retrospective

**Sprint**: 5
**Date**: 2025-12-03
**Theme**: Token Counting & Response Format

---

## 1. What Went Well

### BDD Approach
- Features convertidas PT -> EN antes da implementacao
- Steps reutilizaram padroes de sprints anteriores
- 8 cenarios definidos e todos passando

### Mock Providers
- MockNoTokensProvider criado para cenario especifico
- MockAltProvider criado para teste de formato unificado
- Providers seguem interface ProviderPort

### Processo
- Revisores executados ANTES de solicitar aprovacao
- Aprendizado das Sprints anteriores aplicado
- Criterios de aceitacao verificados

---

## 2. What Didn't Go Well

### Cobertura
- Leve queda na cobertura (90.68% -> 89.14%)
- Novos mock providers tem 70% de cobertura

### Streaming
- Cenario de streaming nao valida tokens reais
- Mock provider limitacao, nao afeta providers reais

---

## 3. Action Items

### Para Sprint 6

| ID | Acao | Prioridade |
|----|------|-----------|
| A1 | Considerar testes de integracao real para tokens | Baixa |
| A2 | Implementar ChatResponseChunk como classe | Media |

### Processo

| ID | Acao | Owner |
|----|------|-------|
| P1 | Manter padrao de revisores ANTES de aprovacao | Team |
| P2 | Continuar conversao PT -> EN de features | Team |

---

## 4. Lessons Learned

### Tecnico
1. **Mock providers especificos**: Uteis para cenarios de edge case
2. **Campo index nos chunks**: Necessario para validar ordem
3. **Nomenclatura do dominio**: Manter consistencia (usage vs tokens)

### Processo
1. **BDD first**: Sempre definir features antes de steps
2. **Conversao PT -> EN**: Padrao bem estabelecido
3. **Reutilizar steps**: Steps de chat podem ser base para outros

---

## 5. Metrics Summary

| Metrica | Sprint 4 | Sprint 5 | Delta |
|---------|----------|----------|-------|
| Testes | 170 | 201 | +31 |
| Cobertura | 90.68% | 91.44% | +0.76% |
| Lint errors | 0 | 0 | = |
| BDD Scenarios | 8 | 16 | +8 |
| Mock Providers | 2 | 4 | +2 |

---

## 6. Team Kudos

- BDD first approach seguido
- Features convertidas corretamente
- Processo de revisao mantido

---

**Facilitador**: Team
**Data**: 2025-12-03
