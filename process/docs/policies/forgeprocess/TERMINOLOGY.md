# Terminologia do ForgeProcess

**Version**: 1.0
**Created**: 2025-11-25
**Status**: Active
**Authority**: Rodrigo Palhano (Project Owner)

---

## 🎯 Propósito

Este documento estabelece a terminologia padrão usada na documentação do ForgeProcess, garantindo consistência e clareza na comunicação sobre o processo.

---

## 📋 Decisões de Terminologia

### 1. Symbiotas (não "Symbiotas Cognitivos")

**Decisão**: Usar apenas **"symbiota"** ou **"agente symbiota"**.

**Rationale**:
- O termo "cognitivo" é redundante — todos os symbiotas processam informação e tomam decisões
- Simplifica a linguagem sem perder clareza
- Evita conotação excessivamente acadêmica/teórica
- "Symbiota" já implica um agente inteligente que colabora com humanos

**Exemplos de Uso**:
- ✅ "O **symbiota** MDD Coach conduz o ciclo MDD"
- ✅ "Symbiotas são agentes especializados que executam partes do processo"
- ❌ ~~"O symbiota cognitivo MDD Coach..."~~
- ❌ ~~"Agentes cognitivos do ForgeProcess..."~~

---

### 2. Sessões (não "Sessões Cognitivas")

**Decisão**: Usar **"sessões"** ou **"sessões internas"** para registros de raciocínio dos symbiotas.

**Rationale**:
- "Sessões" é suficiente para descrever registros de trabalho do symbiota
- Quando necessário distinguir: "sessões internas" (do symbiota) vs. "sessões formais" (do projeto)
- Simplifica nomenclatura de diretórios e arquivos
- Mantém foco na função (registrar trabalho) ao invés da natureza (processamento cognitivo)

**Estrutura de Diretórios**:
```
symbiotes/mdd_coach/
├── prompt.md
└── sessions/           # ✅ Sessões internas do symbiota
    └── README.md

project/docs/sessions/mdd_coach/  # ✅ Sessões formais do projeto
```

**Exemplos de Uso**:
- ✅ "Sessões do MDD Coach"
- ✅ "Registros internos de raciocínio"
- ✅ "Sessões internas vs. sessões formais"
- ❌ ~~"Sessões cognitivas do MDD Coach"~~

---

### 3. Ciclo de Raciocínio (não "Ciclo Cognitivo")

**Decisão**: Usar **"ciclo de raciocínio"** ou simplesmente **"ciclo"** quando apropriado.

**Rationale**:
- "Raciocínio" é mais direto e acessível que "cognitivo"
- Em contextos claros, apenas "ciclo" é suficiente
- Mantém o conceito essencial: processo iterativo de transformação de informação

**Exemplos de Uso**:
- ✅ "ForgeProcess: Ciclo de Raciocínio Completo"
- ✅ "O ciclo transforma intenção em execução"
- ✅ "Feedback fecha o ciclo"
- ❌ ~~"Ciclo cognitivo completo"~~

**Exceção**: Manter "cognitivo" apenas quando absolutamente necessário para clareza técnica ou acadêmica.

---

### 4. Ambiente de Execução (não "Ambiente Cognitivo")

**Decisão**: Usar **"ambiente de execução"**, **"ambiente de teste"** ou **"ambiente para IA"**.

**Rationale**:
- Mais preciso: descreve o que o ambiente permite (executar, testar, observar)
- Evita abstração desnecessária
- Terminologia alinhada com práticas de engenharia de software

**Exemplos de Uso**:
- ✅ "CLI é um ambiente de execução para UseCases"
- ✅ "Ambiente de teste onde IA pode explorar"
- ✅ "Ambiente para IA validar comportamentos"
- ❌ ~~"Espaço cognitivo para IA"~~
- ❌ ~~"Ambiente cognitivo para validação"~~

---

### 5. Transformação/Tradução (não "Tradução Cognitiva")

**Decisão**: Usar **"transformação"** ou **"tradução"** sem qualificador.

**Rationale**:
- O contexto já deixa claro que é uma operação intelectual/de processamento
- Simplifica descrição de transições entre fases

**Exemplos de Uso**:
- ✅ "Transformação de valor em comportamento"
- ✅ "Tradução de ValueTracks em features BDD"
- ✅ "A transição crítica: MDD → BDD"
- ❌ ~~"Tradução cognitiva entre fases"~~

---

## 📊 Impacto da Mudança

### Arquivos Atualizados (2025-11-25)

| Arquivo | Mudanças |
|---------|----------|
| `symbiotes/bdd_coach/prompt.md` | "Symbiota cognitivo" → "Symbiota" |
| `symbiotes/bdd_coach/sessions/README.md` | "Sessões Cognitivas" → "Sessões" |
| `symbiotes/test_writer/sessions/README.md` | "Sessões Cognitivas" → "Sessões" |

### Arquivos a Atualizar (Próxima Fase)

- [ ] `PROCESS.md` (9 ocorrências de "cognitivo")
- [ ] `symbiotes/mdd_coach/prompt.md`
- [ ] `symbiotes/mdd_coach/sessions/README.md`
- [ ] `symbiotes/mdd_publisher/prompt.md`
- [ ] `symbiotes/bill_review/sessions/README.md`
- [ ] `symbiotes/jorge_forge/sessions/README.md`
- [ ] Outros arquivos conforme identificados

---

## 🔄 Princípio Geral

**Regra de Ouro**: Use a terminologia mais **simples e direta** possível.

- Se "symbiota" comunica a ideia, não adicione "cognitivo"
- Se "sessão" é claro no contexto, não adicione "cognitiva"
- Se "ciclo" é suficiente, não adicione "cognitivo"

**Quando usar termos técnicos**: Apenas quando necessário para:
1. Precisão técnica que impacta implementação
2. Diferenciação entre conceitos similares
3. Referência a literatura acadêmica específica

---

## ✅ Checklist para Novos Documentos

Ao criar documentação nova, verificar:
- [ ] Usa "symbiota" (não "symbiota cognitivo")
- [ ] Usa "sessões" ou "sessões internas" (não "sessões cognitivas")
- [ ] Usa "ciclo" ou "ciclo de raciocínio" (não "ciclo cognitivo")
- [ ] Usa "ambiente de execução/teste" (não "ambiente cognitivo")
- [ ] Terminologia é consistente com este documento

---

## 🔗 Referências

- **ForgeProcess Overview**: `PROCESS.md`
- **Symbiotes Directory**: `symbiotes/README.md`
- **Project Layout**: `docs/layout/PROJECT_LAYOUT.md`

---

## 📝 Histórico de Mudanças

### v1.0 (2025-11-25)
- **Criação inicial do documento**
- **Decisão**: Remover "cognitivo" da terminologia padrão
- **Rationale**: Simplificação e clareza
- **Impacto**: Atualização de symbiotas criados (bdd_coach, test_writer)
- **Próximo passo**: Atualizar arquivos legados (PROCESS.md, mdd_coach, etc.)

---

**Aprovado por**: Rodrigo Palhano
**Data**: 2025-11-25
