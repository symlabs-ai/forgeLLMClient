# 🔹 BDD Subetapa 2: Escrita de Features Gherkin

## 🎯 Propósito

Transformar os **comportamentos mapeados** em **especificações executáveis** usando a linguagem Gherkin (PT-BR).

Esta é a etapa onde a **comunicação universal** acontece: todos — stakeholders, produto, dev, QA — leem a mesma especificação.

---

## ⚙️ Entradas e Saídas

| Tipo | Artefato | Descrição |
|------|----------|-----------|
| **Entrada** | `process/bdd/docs/behavior_mapping.md` | Mapeamento Track → Behaviors |
| **Saída** | `specs/bdd/**/*.feature` | Features Gherkin PT-BR |
| **Apoio** | `process/bdd/templates/template_feature.md` | Template de feature |

---

## 📖 Anatomia de uma Feature Gherkin (Padrão Forge)

```gherkin
# language: pt
@tag_dominio @tag_capacidade @tag_ci
Funcionalidade: [Título claro e descritivo]
  Para [benefício/valor entregue]
  Como [ator/usuário]
  Quero [capacidade desejada]

  Contexto:
    Dado [pré-condição compartilhada entre cenários]
    E [outra pré-condição]

  Cenário: [Nome do caso de sucesso]
    Dado [contexto específico]
    E [mais contexto se necessário]
    Quando [ação executada]
    Então [resultado esperado]
    E [efeito colateral observável]

  Cenário: [Nome do caso de erro]
    Dado [contexto que leva ao erro]
    Quando [ação que causa erro]
    Então [tratamento esperado]
    E [mensagem ou log específico]

  Esquema do Cenário: [Nome do caso parametrizado]
    Dado [contexto com <parametro>]
    Quando [ação com <parametro>]
    Então [resultado com <parametro>]

    Exemplos:
      | parametro | resultado |
      | valor1    | esperado1 |
      | valor2    | esperado2 |
```

---

## 🧩 Estrutura de Palavras-Chave Gherkin (PT-BR)

### **FUNCIONALIDADE** (Feature)
Define a capacidade ou módulo sendo especificado.

```gherkin
FUNCIONALIDADE: Chat básico no Forge SDK
  PARA enviar mensagens e receber respostas de LLMs
  COMO um desenvolvedor
  QUERO usar uma interface consistente independente do provedor
```

### **CONTEXTO** (Background)
Pré-condições compartilhadas entre todos os cenários da feature.

```gherkin
CONTEXTO:
  DADO que o Forge está instalado
  E o provedor "echo" está configurado
```

### **CENÁRIO** (Scenario)
Um comportamento específico com fluxo único.

```gherkin
CENÁRIO: Enviar mensagem e receber resposta
  DADO que estou conectado ao provedor "echo"
  QUANDO envio a mensagem "Olá"
  ENTÃO recebo uma resposta contendo "Olá"
  E a resposta tem formato válido
```

### **ESQUEMA DO CENÁRIO** (Scenario Outline)
Comportamento parametrizado testado com múltiplos valores.

```gherkin
ESQUEMA DO CENÁRIO: Validar diferentes provedores
  DADO que o Forge está configurado com "<provedor>"
  QUANDO envio uma mensagem de teste
  ENTÃO recebo resposta de sucesso
  E o log registra provedor "<provedor>"

  EXEMPLOS:
    | provedor   |
    | echo       |
    | llama_cpp  |
    | openrouter |
```

### **Steps: DADO / QUANDO / ENTÃO / E**

| Keyword | Propósito | Exemplo |
|---------|-----------|---------|
| **DADO** (Given) | Pré-condição, contexto inicial | `DADO que o usuário está autenticado` |
| **QUANDO** (When) | Ação executada | `QUANDO ele envia uma mensagem` |
| **ENTÃO** (Then) | Resultado esperado | `ENTÃO ele recebe uma resposta` |
| **E** (And) | Continuar contexto/ação/resultado | `E a resposta contém timestamp` |

---

## 🎨 Padrões de Escrita (Boas Práticas)

### ✅ Linguagem de Negócio, não Implementação

❌ **Errado** (acoplado à implementação):
```gherkin
QUANDO chamo o método `ForgeClient.chat(message="Olá")`
ENTÃO recebo um objeto `ChatResponse` com atributo `content`
```

✅ **Correto** (linguagem de domínio):
```gherkin
QUANDO envio a mensagem "Olá"
ENTÃO recebo uma resposta contendo "Olá"
```

---

### ✅ Um Comportamento por Cenário

❌ **Errado** (múltiplos comportamentos misturados):
```gherkin
CENÁRIO: Chat completo
  DADO que tenho uma sessão
  QUANDO envio "Olá"
  ENTÃO recebo resposta
  E o log registra evento
  E a métrica de latência é atualizada
  E a sessão persiste o histórico
```

✅ **Correto** (comportamentos separados):
```gherkin
CENÁRIO: Enviar mensagem e receber resposta
  QUANDO envio "Olá"
  ENTÃO recebo resposta contendo "Olá"

CENÁRIO: Registrar evento de chat no log
  QUANDO envio uma mensagem
  ENTÃO o log registra o evento com timestamp

CENÁRIO: Persistir histórico na sessão
  DADO uma sessão ativa
  QUANDO envio múltiplas mensagens
  ENTÃO o histórico contém todas as mensagens
```

---

### ✅ Observável e Verificável

❌ **Errado** (não verificável externamente):
```gherkin
ENTÃO o sistema processa internamente
E o algoritmo otimiza a resposta
```

✅ **Correto** (resultado observável):
```gherkin
ENTÃO recebo uma resposta válida
E o log registra o evento com status "success"
E a latência é menor que 5 segundos
```

---

### ✅ Curto e Objetivo (máximo 5-7 steps)

❌ **Errado** (cenário longo demais):
```gherkin
CENÁRIO: Fluxo completo de chat
  DADO que instalo o Forge
  E configuro credenciais
  E valido conexão
  E crio uma sessão
  E aguardo confirmação
  E envio primeira mensagem
  E valido resposta
  E envio segunda mensagem
  E valido contexto
  E encerro sessão
  ENTÃO tudo funcionou
```

✅ **Correto** (dividir em múltiplos cenários):
```gherkin
CONTEXTO:
  DADO que o Forge está configurado e conectado

CENÁRIO: Enviar primeira mensagem
  QUANDO envio "Olá"
  ENTÃO recebo resposta válida

CENÁRIO: Preservar contexto em mensagens subsequentes
  DADO que enviei "Olá" anteriormente
  QUANDO envio "Como você está?"
  ENTÃO a resposta considera o contexto anterior
```

---

## 📋 Exemplo Completo: Feature do Forge Chat

```gherkin
# specs/bdd/10_forge_core/chat.feature

@sdk @ci-fast
FUNCIONALIDADE: Chat básico no Forge SDK
  PARA enviar mensagens e receber respostas de LLMs
  COMO um desenvolvedor Python
  QUERO usar uma interface consistente independente do provedor

  CONTEXTO:
    DADO que o Forge está instalado
    E o ambiente de teste está configurado

  CENÁRIO: Enviar mensagem simples e receber resposta
    DADO que o Forge está configurado com o provedor "echo"
    QUANDO envio a mensagem "Olá, mundo!"
    ENTÃO recebo uma resposta contendo "Olá, mundo!"
    E a resposta tem formato válido de ChatResponse

  CENÁRIO: Erro ao usar provedor não configurado
    DADO que o Forge não está configurado com nenhum provedor
    QUANDO tento enviar uma mensagem
    ENTÃO recebo um erro do tipo ConfigurationError
    E a mensagem de erro contém "Provedor não configurado"

  CENÁRIO: Erro ao usar provedor inválido
    DADO que tento configurar o provedor "provedor_inexistente"
    ENTÃO recebo um erro do tipo ProviderNotFoundError
    E a mensagem de erro lista provedores disponíveis

  ESQUEMA DO CENÁRIO: Validar compatibilidade multi-provedor
    DADO que o Forge está configurado com "<provedor>"
    QUANDO envio a mensagem "teste"
    ENTÃO recebo uma resposta de sucesso
    E o log registra provedor "<provedor>"

    EXEMPLOS:
      | provedor   |
      | echo       |
      | llama_cpp  |
      | openrouter |
```

---

## 🗂️ Organização de Arquivos

### Convenção de Nomes

```
specs/bdd/[prefixo]_[dominio]/[nome_descritivo].feature

Exemplos:
✅ specs/bdd/10_forge_core/chat.feature
✅ specs/bdd/10_forge_core/sessao.feature
✅ specs/bdd/20_symclient_http/chat_http.feature
✅ specs/bdd/30_plugins_provedores/tool_calling_fallback.feature
```

### Estrutura por Domínio

| Prefixo | Domínio | Features Típicas |
|---------|---------|------------------|
| `10_*` | Forge Core (SDK) | chat, sessao, config, streaming |
| `20_*` | SymClient HTTP | health, chat_http, errors |
| `21_*` | SymClient STDIO | ping, chat_stdio, json_rpc |
| `30_*` | Plugins | tool_calling, fallback, capabilities |
| `40_*` | MCP | marketplace, discovery, invocation |
| `41_*` | Broker | routing, load_balance |
| `50_*` | Observability | logs, metrics, tracing |
| `60_*` | Security | redaction, auth, rate_limit |

---

## 🏷️ Sistema de Tags

Aplique tags no topo de cada feature para classificação e execução seletiva:

```gherkin
@sdk @contexto @ci-fast
FUNCIONALIDADE: Gestão de sessões
  ...
```

### Tags de Domínio
- `@sdk` - Forge SDK Python
- `@server` - SymClient (HTTP ou STDIO)
- `@http` - Protocolo HTTP
- `@stdio` - Protocolo STDIO

### Tags de Capacidade
- `@contexto` - Gestão de sessão/contexto
- `@streaming` - Respostas em stream
- `@capability:tool_calling` - Tool calling
- `@fallback` - Comportamentos de fallback

### Tags de Integração
- `@mcp` - Integração MCP
- `@broker` - Roteamento via broker

### Tags de CI
- `@ci-fast` - Rápido (mocks, sem deps externas)
- `@ci-int` - Integração (provedores locais)
- `@e2e` - End-to-end (deps externas)

### Dicas finais
- Mantenha palavras-chave em minúsculas e `# language: pt`.
- Casar textos dos steps com as step definitions (evitar variação “o/que/um”).
- Rode `pytest --collect-only` (com `PYTHONPATH=src`) para validar sintaxe antes de commitar.

---

## ✅ Critérios de Qualidade (DoD)

- [ ] Features escritas em Gherkin PT-BR válido
- [ ] Palavras-chave em MAIÚSCULAS (FUNCIONALIDADE, CENÁRIO, etc)
- [ ] Linguagem de negócio (não detalhes de implementação)
- [ ] Um comportamento por cenário
- [ ] Cenários curtos (máximo 7 steps)
- [ ] Casos de sucesso E erro cobertos
- [ ] Tags aplicadas corretamente
- [ ] Organização em pastas por domínio
- [ ] Revisão com stakeholder/PO

---

## 🚨 Checklist Antes de Finalizar

```markdown
Para cada feature:
- [ ] Título descreve claramente a capacidade
- [ ] Propósito (PARA/COMO/QUERO) está claro
- [ ] CONTEXTO evita repetição entre cenários
- [ ] Pelo menos 1 cenário de sucesso
- [ ] Pelo menos 1 cenário de erro
- [ ] Steps são observáveis e verificáveis
- [ ] Sem detalhes de implementação
- [ ] Tags de domínio, capacidade e CI aplicadas
```

---

## 🔄 Próximo Passo

Com as features Gherkin escritas, avance para:

**Subetapa 3: Organização e Tagging** (`etapa_03_organizacao_tagging.md`)

---

**Author**: Forge Framework Team
**Version**: 1.0
**Date**: 2025-11-04
