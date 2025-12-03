# Mapeamento de Comportamentos — [Nome do Projeto]

> **Data:** [AAAA-MM-DD]
>
> **Responsável:** [Nome]
>
> **Status:** [Rascunho / Em Revisão / Aprovado]

---

## ValueTrack: [Nome do Track]

**Tipo:** VALUE | SUPPORT

**Domínio:** [10_forge_core, 20_symclient_http, 21_symclient_stdio, 30_plugins, 40_mcp, 41_broker, 50_observabilidade, 60_seguranca]

**Referência MDD:** `project/docs/visao.md` (linha XX)

---

### Comportamentos Identificados

#### 1. [Nome do Comportamento - Sucesso]

**Ação (O QUÊ o usuário faz):**
[Descrever a ação em linguagem de negócio]

**Resultado esperado (O QUÊ ele vê):**
[Descrever o resultado observável]

**Critério de validação (COMO validar):**
[Como saber que funcionou — resposta, log, métrica]

**Cenário BDD futuro:**
```gherkin
CENÁRIO: [Nome descritivo]
  DADO [contexto]
  QUANDO [ação]
  ENTÃO [resultado]
```

---

#### 2. [Nome do Comportamento - Outro Caso]

**Ação:**


**Resultado esperado:**


**Critério:**


**Cenário BDD:**
```gherkin
CENÁRIO: [Nome]
  ...
```

---

### Casos de Erro

#### 1. [Nome do Erro]

**Condição (QUANDO ocorre):**
[Descrever condição que causa erro]

**Tratamento esperado (COMO o sistema reage):**
[Mensagem de erro, log, estado do sistema]

**Critério de validação:**
[Como verificar que erro foi tratado corretamente]

**Cenário BDD futuro:**
```gherkin
CENÁRIO: [Nome do erro]
  DADO [contexto de erro]
  QUANDO [ação que causa erro]
  ENTÃO [tratamento]
  E [evidência — log, mensagem, etc]
```

---

#### 2. [Outro Erro]

**Condição:**


**Tratamento esperado:**


**Cenário BDD:**
```gherkin
...
```

---

### Edge Cases (Opcional)

#### 1. [Nome do Edge Case]

**Descrição:**


**Comportamento esperado:**


**Cenário BDD:**
```gherkin
...
```

---

## ValueTrack: [Próximo Track]

[Repetir estrutura acima]

---

## Resumo de Mapeamento

| ValueTrack | Tipo | Comportamentos | Cenários BDD |
|------------|------|----------------|--------------|
| [Track 1] | VALUE | 3 | 5 |
| [Track 2] | SUPPORT | 2 | 4 |
| ... | ... | ... | ... |

**Total:** X comportamentos → Y cenários BDD

---

## Próximo Passo

- [ ] Revisão com PO/Stakeholder
- [ ] Aprovação do mapeamento
- [ ] Avançar para Subetapa 2: Escrita de Features Gherkin

---

**Autor:** [Nome]
**Revisado por:** [Nome/PO]
**Data de aprovação:** [AAAA-MM-DD]
