# Sprint 8 - Planning

**Sprint**: 8
**Tema**: Conversation History
**Data**: 2025-12-04

---

## Objetivo

Implementar suporte a conversas multi-turn, permitindo que o usuario mantenha contexto entre mensagens sem gerenciar manualmente o historico.

---

## Escopo

### Funcionalidades

1. **Conversation Entity**
   - Gerencia historico de mensagens
   - Adiciona mensagens user/assistant automaticamente
   - Suporta system prompt

2. **Integracao com Client**
   - Metodo `create_conversation()` para iniciar conversa
   - Conversation usa o Client internamente

3. **API Simples**
   ```python
   client = Client(provider="openai", api_key="sk-...")
   conv = client.create_conversation(system="Voce e um assistente util")

   response = await conv.chat("Ola!")
   response = await conv.chat("Qual foi minha primeira mensagem?")
   # Responde: "Voce disse 'Ola!'"
   ```

### Fora do Escopo
- Persistencia de conversas (futuro)
- Limite de tokens/truncamento (futuro)
- Branching de conversas (futuro)

---

## Criterios de Aceite

1. [ ] Conversation mantem historico entre chamadas
2. [ ] System prompt e enviado corretamente
3. [ ] Respostas do assistant sao adicionadas ao historico
4. [ ] Historico pode ser acessado e limpo
5. [ ] Testes BDD cobrindo cenarios principais
6. [ ] Cobertura >= 90%

---

## Arquitetura

### Nova Entity: Conversation

```
src/forge_llm/domain/entities.py
  - Conversation
    - messages: list[Message]
    - system_prompt: str | None
    - add_user_message(content)
    - add_assistant_message(content)
    - get_messages() -> list[Message]
    - clear()
```

### Integracao Client

```
src/forge_llm/client.py
  - create_conversation(system: str | None = None) -> Conversation
```

### Arquivos a Criar/Modificar
- `src/forge_llm/domain/entities.py` - adicionar Conversation
- `src/forge_llm/client.py` - adicionar create_conversation
- `specs/bdd/10_forge_core/conversation.feature` - BDD feature
- `tests/bdd/test_conversation_steps.py` - BDD steps
- `tests/unit/domain/test_entities.py` - testes Conversation

---

## Metricas Iniciais

| Metrica | Valor Atual |
|---------|-------------|
| Testes | 268 |
| Cobertura | 93.81% |
| BDD Scenarios | 39 |

---

## Riscos

1. **Token limit** - Conversas longas podem exceder limite
   - Mitigacao: Documentar limite, implementar truncamento em sprint futura

2. **Memory** - Historico cresce sem limite
   - Mitigacao: Metodo `clear()` para reset manual

---

**Status**: Planning completo, pronto para implementacao.
