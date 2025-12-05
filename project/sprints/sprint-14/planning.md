# Sprint 14 - Hot-Swap & Context Management

**Data**: 2025-12-05
**Objetivo**: Implementar troca de provider mid-conversation e gestão avançada de contexto

---

## Escopo

### 1. MessageMetadata (Value Object)
Metadados por mensagem para tracking e debug.

```python
@dataclass(frozen=True)
class MessageMetadata:
    timestamp: datetime
    provider: str | None = None
    model: str | None = None
```

### 2. EnhancedMessage (Value Object)
Wrapper que combina Message + Metadata.

```python
@dataclass(frozen=True)
class EnhancedMessage:
    message: Message
    metadata: MessageMetadata
```

### 3. Conversation Aprimorada

**Novos parâmetros:**
- `max_tokens: int | None` - Budget de tokens (além de max_messages)
- `model: str | None` - Para contagem de tokens

**Novas properties:**
- `token_count: int` - Total de tokens atual
- `last_provider: str | None` - Último provider usado
- `provider_history: list[str]` - Histórico de providers

**Novos métodos:**
- `change_provider(provider: str | ProviderPort, api_key: str | None = None)` - Hot-swap
- `to_dict() -> dict` - Serialização
- `from_dict(data: dict, client: Client) -> Conversation` - Deserialização

### 4. Integração com TokenCounter
- Reusar `ConversationMemory` internamente ou integrar `TokenCounter`
- Truncamento automático por tokens

---

## Arquivos a Modificar

| Arquivo | Mudança |
|---------|---------|
| `domain/value_objects.py` | + MessageMetadata, EnhancedMessage |
| `domain/entities.py` | Conversation aprimorada |
| `client.py` | Expor provider para hot-swap |

## Arquivos a Criar

| Arquivo | Descrição |
|---------|-----------|
| `tests/unit/domain/test_conversation_enhanced.py` | Testes unitários |
| `specs/bdd/10_forge_core/conversation.feature` | Cenários BDD |
| `tests/bdd/test_conversation_steps.py` | Steps BDD |

---

## Critérios de Aceite

- [ ] Conversation suporta max_tokens além de max_messages
- [ ] change_provider() troca provider preservando histórico
- [ ] MessageMetadata rastreia provider/model por mensagem
- [ ] Serialização to_dict/from_dict funciona
- [ ] Cobertura >= 80% nas novas features
- [ ] Todos os testes passando

---

## API Proposta

```python
# Criar conversa com budget de tokens
conv = client.create_conversation(
    system="Você é um assistente",
    max_tokens=4000,  # NOVO
    model="gpt-4"     # NOVO: para contagem
)

# Chat normal
response = await conv.chat("Olá!")

# Hot-swap mid-conversation
await conv.change_provider("anthropic", api_key="sk-ant-...")

# Continua com novo provider, histórico preservado
response = await conv.chat("Continue nossa conversa")

# Serialização
data = conv.to_dict()
# ... salvar em arquivo ...

# Restaurar
conv = Conversation.from_dict(data, client)
```

---

## Decisões Técnicas

| Decisão | Escolha | Razão |
|---------|---------|-------|
| MessageMetadata separado | Value Object | Não quebra Message existente |
| Token counting opcional | Via max_tokens | Compatibilidade com código existente |
| Hot-swap via Client | Reusar Client.configure | Menos código novo |
| Serialização simples | JSON-friendly dict | Permite YAML/JSON |
