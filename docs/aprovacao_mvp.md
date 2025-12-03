# Aprovacao de MVP — ForgeLLMClient

## 1. Contexto e Decisao

Após a conclusao das etapas 1-4 do MDD (Visao, Sumário Executivo, Pitch e Landing Pages), os stakeholders analisaram a proposta e **decidiram aprovar o avanço para o MVP**.

A decisao é baseada em:

- **Clareza da hipótese**: O problema de vendor lock-in e instabilidade de APIs de LLMs é real e bem documentado
- **Diferencial técnico validado**: Hot-Swap em runtime sem perda de contexto é um diferencial único no mercado
- **Modelo de negócio viável**: Open Core permite adocao massiva + revenue enterprise
- **Timing favorável**: O caos atual do mercado de LLMs justifica uma camada de abstracao

> **Decisao: APROVADO para desenvolvimento do MVP**

---

## 2. Resultados-Chave da Validacao

### Validacao por Stakeholders

| Critério | Avaliacao | Observacao |
|----------|-----------|------------|
| Problema é real | Sim | Experiencia própria com migracoes de API |
| Solucao é diferenciada | Sim | Hot-Swap + Context Management únicos |
| Público-alvo claro | Sim | Devs Python com LLMs em producao |
| Modelo de negócio sustentável | Sim | Open Core comprovado |
| Timing de mercado | Sim | Volatilidade atual favorece abstracao |

### Narrativa Mais Forte

Das três variacoes de landing page:
- **Site B (Funcional)** foi considerado o mais alinhado com o público-alvo (devs técnicos)
- Foco em features concretas: Gestao de Contexto, Tool Calling, MCP Client, Hot-swap

---

## 3. Escopo do MVP

### Incluído no MVP (Fase 1)

| Elemento | Prioridade | Justificativa |
|----------|------------|---------------|
| Interface unificada de chat | Alta | Core do produto |
| Chat sync e streaming | Alta | Essencial para UX |
| Tool Calling normalizado | Alta | Diferencial-chave |
| Consumo de tokens por requisicao | Alta | Visibilidade de custo |
| Normalizacao de respostas | Alta | Consistencia |
| Suporte OpenAI | Alta | Provedor mais usado |
| Suporte Anthropic | Alta | Segundo mais usado |

### Fora do MVP (Fases Futuras)

| Elemento | Fase | Motivo |
|----------|------|--------|
| AutoFallback | Fase 2 | Depende de múltiplos provedores estáveis |
| Hot-Swap em runtime | Fase 2 | Requer Context Management maduro |
| Context Management avancado | Fase 2 | Complexidade técnica |
| MCP Client | Fase 3 | Ecossistema ainda em formacao |
| Mock Provider | Fase 3 | Nice-to-have para CI/CD |
| Sistema de Eventos | Fase 3 | Extensibilidade |
| Plugins externos | Fase 3 | Comunidade |

---

## 4. Objetivos do MVP

### Métricas Quantitativas

| Métrica | Target | Prazo |
|---------|--------|-------|
| Publicacao no PyPI | 1 release | 4 semanas |
| Testes passando | 100% | Contínuo |
| Cobertura de testes | >= 80% | Contínuo |
| Documentacao básica | README + exemplos | 4 semanas |

### Métricas de Validacao (pós-lancamento)

| Métrica | Target | Prazo |
|---------|--------|-------|
| Downloads PyPI | >= 100 | 2 meses |
| Issues/feedback | >= 5 | 2 meses |
| Uso em projeto real | >= 1 | 3 meses |

### Critérios de Sucesso do MVP

1. **Funciona**: Chat sync/streaming com OpenAI e Anthropic
2. **É leve**: Instalacao simples, sem dependencias pesadas
3. **É explícito**: Zero mágica, código previsível
4. **Documenta tokens**: Cada requisicao informa consumo

---

## 5. Riscos e Cuidados

| Risco | Impacto | Mitigacao |
|-------|---------|-----------|
| **Escopo creep** | Alto | Manter foco estrito no MVP; dizer "nao" para features |
| **Complexidade de normalizacao** | Médio | Comecar simples, iterar |
| **APIs mudarem durante dev** | Médio | Arquitetura desacoplada por provedor |
| **Adocao lenta** | Médio | README excelente, exemplos funcionais |
| **Over-engineering** | Alto | Filosofia "zero-mágica", código explícito |

---

## 6. Stakeholders e Responsáveis

| Papel | Responsabilidade |
|-------|------------------|
| **Stakeholder/Fundador** | Decisoes de produto, prioridades, aprovacao final |
| **MDD Coach** | Coordenacao do processo, documentacao |
| **Dev Principal** | Implementacao técnica, arquitetura |

---

## 7. Proximos Passos

### Imediatos (esta semana)

1. **Iniciar BDD Process** — Mapear comportamentos do MVP em Gherkin
2. **Definir arquitetura** — HLD/LLD do Core SDK
3. **Setup do projeto** — Estrutura de pastas, CI/CD, pyproject.toml

### Curto Prazo (próximas 4 semanas)

1. **Implementar Core** — Chat sync/streaming
2. **Implementar provedores** — OpenAI + Anthropic
3. **Testes** — Cobertura >= 80%
4. **Documentacao** — README + exemplos básicos
5. **Publicar** — PyPI release v0.1.0

### Handoff para BDD

Este documento autoriza o início do **BDD Process** (Etapa 6 do MDD).
O BDD usará a visao e esta aprovacao como base para detalhar os comportamentos do sistema.

---

## 8. Assinaturas

| Stakeholder | Data | Status |
|-------------|------|--------|
| Fundador/PO | 2025-12-03 | **APROVADO** |

---

*Documento gerado pelo MDD Coach em colaboracao com stakeholders.*
*Data: 2025-12-03*
*Versao: 1.0*
