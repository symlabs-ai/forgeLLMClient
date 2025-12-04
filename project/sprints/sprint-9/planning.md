# Sprint 9 - Vision/Images Support

**Data Inicio**: 2025-12-04
**Status**: Em Andamento

---

## 1. Objetivo

Implementar suporte a envio de imagens nas mensagens para modelos com capacidade de visao (GPT-4o, Claude 3, etc).

---

## 2. Escopo

### Incluido
- [ ] Value object `ImageContent` para representar imagens
- [ ] Suporte a imagem por URL
- [ ] Suporte a imagem por base64
- [ ] Integracao com OpenAI provider (vision)
- [ ] Integracao com Anthropic provider (vision)
- [ ] BDD feature com cenarios de visao

### Fora do Escopo
- Upload de arquivos para storage
- Processamento/resize de imagens
- OCR ou extracao de texto

---

## 3. Criterios de Aceite

1. Usuario pode enviar imagem por URL em mensagem
2. Usuario pode enviar imagem em base64 em mensagem
3. OpenAI provider formata corretamente para API
4. Anthropic provider formata corretamente para API
5. Cobertura >= 80%
6. Todos os testes passando

---

## 4. Design Tecnico

### 4.1 Value Objects

```python
@dataclass(frozen=True)
class ImageContent:
    """Conteudo de imagem para mensagens multimodais."""

    url: str | None = None
    base64_data: str | None = None
    media_type: str = "image/jpeg"  # image/png, image/gif, image/webp

    def __post_init__(self):
        if not self.url and not self.base64_data:
            raise ValidationError("URL ou base64_data obrigatorio")
        if self.url and self.base64_data:
            raise ValidationError("Usar URL ou base64_data, nao ambos")
```

### 4.2 Message Content

Atualizar `Message` para suportar conteudo misto:

```python
@dataclass(frozen=True)
class Message:
    role: str
    content: str | list[str | ImageContent]  # texto ou lista mista
```

### 4.3 Provider Formatting

**OpenAI format:**
```python
{
    "role": "user",
    "content": [
        {"type": "text", "text": "O que ha nesta imagem?"},
        {"type": "image_url", "image_url": {"url": "https://..."}}
    ]
}
```

**Anthropic format:**
```python
{
    "role": "user",
    "content": [
        {"type": "text", "text": "O que ha nesta imagem?"},
        {"type": "image", "source": {"type": "url", "url": "https://..."}}
    ]
}
```

---

## 5. Tasks

1. [ ] Criar BDD feature `vision.feature`
2. [ ] Criar `ImageContent` value object
3. [ ] Atualizar `Message` para suportar conteudo misto
4. [ ] Atualizar OpenAI provider para formatar imagens
5. [ ] Atualizar Anthropic provider para formatar imagens
6. [ ] Implementar BDD steps
7. [ ] Testes unitarios
8. [ ] Validar cobertura

---

## 6. Riscos

| Risco | Mitigacao |
|-------|-----------|
| APIs de visao podem ter rate limits diferentes | Documentar limitacoes |
| Imagens grandes podem exceder limites | Validar tamanho |
| Formatos diferentes entre providers | Abstracoes claras |

---

## 7. Metricas Baseline

| Metrica | Sprint 8 | Target Sprint 9 |
|---------|----------|-----------------|
| Testes | 280 | +10 |
| Cobertura | 94.16% | >= 94% |
| BDD Scenarios | 45 | +4 |
