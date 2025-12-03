# 🧩 Template — Handoff para BDD (MDD)

## 🎯 Propósito

O `handoff_bdd.md` formaliza a **transferência de controle do MDD para o BDD Process** após a aprovação do MVP.
Este documento conecta a visão de mercado validada com a especificação comportamental do sistema, servindo como ponte entre as fases de validação e desenvolvimento.

> **Dica:** O handoff deve ser claro o suficiente para que a equipe de BDD compreenda o contexto de negócio sem precisar revisar todos os artefatos anteriores. Inclua links para documentos-chave.

---

## 🧱 Estrutura

```markdown
# 🔗 Handoff MDD → BDD — [Nome do Projeto]

## 1. Resumo Executivo
Breve descrição do produto validado e contexto da transferência.
> Exemplo: "O [Nome do Produto] foi validado com sucesso na fase MDD, demonstrando forte interesse de mercado. Este documento autoriza o início da especificação comportamental via BDD Process."

---

## 2. Visão do Produto
Resumo da visão aprovada (referência ao `visao.md`).
| Aspecto | Descrição |
|---------|-----------|
| Propósito | [Propósito central do produto] |
| Público-alvo | [Segmento principal] |
| Proposta de valor | [Diferencial competitivo] |
| Métrica de sucesso | [KPI principal] |

---

## 3. Escopo Aprovado do MVP
Resumo do escopo definido na aprovação (referência ao `aprovacao_mvp.md`).
| Funcionalidade | Prioridade | Observações |
|----------------|------------|-------------|
| [Feature 1] | Alta | Core da solução |
| [Feature 2] | Média | Diferenciação |
| [Feature 3] | Baixa | Nice-to-have |

---

## 4. Artefatos de Referência
Lista dos documentos MDD que devem ser consultados durante o BDD.
| Artefato | Caminho | Relevância |
|----------|---------|------------|
| Visão | `docs/visao.md` | Contexto de negócio |
| Sumário Executivo | `docs/sumario_executivo.md` | Estratégia e modelo |
| Aprovação MVP | `docs/aprovacao_mvp.md` | Escopo e decisões |
| Resultados Validação | `docs/resultados_validacao.md` | Dados de mercado |

---

## 5. Glossário de Domínio
Termos-chave do domínio que devem ser usados nas especificações BDD.
| Termo | Definição |
|-------|-----------|
| [Termo 1] | [Definição clara e concisa] |
| [Termo 2] | [Definição clara e concisa] |

---

## 6. Personas e Atores
Perfis de usuários identificados durante a validação de mercado.
| Persona | Descrição | Necessidades Principais |
|---------|-----------|------------------------|
| [Persona 1] | [Breve descrição] | [Lista de necessidades] |
| [Persona 2] | [Breve descrição] | [Lista de necessidades] |

---

## 7. Restrições e Premissas
Limitações técnicas ou de negócio identificadas durante o MDD.
| Tipo | Descrição | Impacto no BDD |
|------|-----------|----------------|
| Técnica | [Restrição] | [Como afeta especificações] |
| Negócio | [Premissa] | [Como afeta especificações] |

---

## 8. Critérios de Aceite Macro
Condições de alto nível que o MVP deve atender.
- [ ] [Critério 1]
- [ ] [Critério 2]
- [ ] [Critério 3]

---

## 9. Transferência de Responsabilidade
| Papel | Nome | Responsabilidade |
|-------|------|------------------|
| Product Owner | [Nome] | Priorização e validação de features |
| BDD Coach | [Nome] | Facilitação do processo BDD |
| MDD Coach | [Nome] | Suporte para dúvidas de contexto |

---

## 10. Data e Assinaturas
| Papel | Nome | Data | Status |
|-------|------|------|--------|
| Aprovador MDD | [Nome] | [Data] | ✅ Aprovado |
| Receptor BDD | [Nome] | [Data] | ✅ Recebido |

---
```

## 📋 Checklist de Qualidade

- [ ] Visão do produto está clara e atualizada
- [ ] Escopo do MVP está definido e priorizado
- [ ] Todos os artefatos de referência estão linkados
- [ ] Glossário contém termos essenciais do domínio
- [ ] Personas refletem os usuários validados
- [ ] Restrições e premissas estão documentadas
- [ ] Critérios de aceite macro estão definidos
- [ ] Responsabilidades estão atribuídas

---

## 🔗 Relacionamentos

| Artefato | Relação |
|----------|---------|
| `aprovacao_mvp.md` | Input principal — contém decisão de aprovação |
| `visao.md` | Referência — contexto de negócio |
| `specs/bdd/` | Output — especificações BDD serão criadas aqui |
