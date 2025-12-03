# ForgeLLMClient — SDK Unificado para LLMs

> **Uma API. Qualquer provedor. Gestão de Contexto, Tool Calling, MCPClient e Hot-swap em runtime.**

---

## O Problema Tecnico

| Desafio | Impacto |
|---------|---------|
| APIs inconsistentes | Código diferente para cada provedor |
| Tool Calling nao padronizado | Reimplementar para cada LLM |
| Context Management variável | Perder histórico ao trocar modelo |
| Sem fallback nativo | Downtime quando provedor falha |
| Testes caros | Gastar tokens só para testar |

---

## A Solucao Tecnica

**ForgeLLMClient** é um SDK Python leve que normaliza tudo:

```python
from forge import Client

# Configurar com fallback
client = Client(
    primary="openai/gpt-4",
    fallback=["anthropic/claude-3", "local/llama"]
)

# Interface única — sync ou streaming
response = client.chat("Explique quantum computing")

# Hot-swap sem perder contexto
client.swap_provider("anthropic/claude-3")
response = client.chat("Continue a explicacao")  # contexto preservado
```

---

## Como Funciona

| Camada | Funcao |
|--------|--------|
| **Interface Unificada** | `client.chat()` para qualquer provedor |
| **Normalizacao** | Tool Calling e Context padronizados |
| **AutoFallback** | Troca automática se provedor falhar |
| **Hot-Swap** | Mudar modelo em runtime sem perder estado |
| **Mock Provider** | Testes sem gastar tokens |
| **MCP Client** | Acesso nativo ao Model Context Protocol |

---

## Comparativo

| Feature | SDKs Nativos | LangChain | LiteLLM | **ForgeLLMClient** |
|---------|--------------|-----------|---------|-------------------|
| Interface unificada | - | Parcial | Sim | **Sim** |
| Tool Calling normalizado | - | Parcial | Parcial | **Sim** |
| Context Management | - | Complexo | - | **Sim** |
| Hot-Swap em runtime | - | - | - | **Sim** |
| AutoFallback | - | - | Parcial | **Sim** |
| MCP Client | - | - | - | **Sim** |
| Leve e explícito | - | Pesado | Sim | **Sim** |

---

## Provedores Suportados

**Fase 1 (atual)**:
- OpenAI (GPT-4, GPT-3.5)
- Anthropic (Claude 3)

**Fase 2 (planejado)**:
- OpenRouter
- LlamaCPP (local)
- Gemini

**Plugin System**: Adicione qualquer provedor.

---

## Instalacao

```bash
pip install forge-llm  # em breve
```

---

## Chamada a Acao

> **Quer testar antes do lancamento?**

[Solicitar acesso ao beta](#)

---

*ForgeLLMClient — Cliente LLM para devs que querem controle*
