# Template de Feature Gherkin (PT-BR)

> **Use este template** para escrever features Gherkin seguindo o padrão Forge.
> Inclua sempre `# language: pt` no topo para garantir parsing correto.

---

## Arquivo: `specs/bdd/[prefixo]_[dominio]/[nome].feature`

```gherkin
# language: pt
# [prefixo]_[dominio]/[nome].feature
# Descrição breve do que esta feature especifica

@tag_dominio @tag_capacidade @tag_ci
Funcionalidade: [Título claro e descritivo]
  Para [benefício ou valor entregue]
  Como [ator ou tipo de usuário]
  Quero [capacidade ou ação desejada]

  Contexto:
    Dado [pré-condição compartilhada entre cenários]
    E [outra pré-condição se necessário]

  Cenário: [Nome do caso de sucesso - Happy Path]
    Dado [contexto específico deste cenário]
    E [mais contexto se necessário]
    Quando [ação executada pelo usuário]
    Então [resultado esperado observável]
    E [efeito colateral observável — log, métrica, estado]

  Cenário: [Nome do caso de erro]
    Dado [contexto que leva ao erro]
    Quando [ação que causa o erro]
    Então [tratamento de erro esperado]
    E [evidência do tratamento — mensagem, log, código de erro]

  Esquema do Cenário: [Nome do caso parametrizado]
    Dado [contexto com "<parametro>"]
    Quando [ação com "<parametro>"]
    Então [resultado com "<parametro>"]
    E [validação adicional]

    EXEMPLOS:
      | parametro  | resultado_esperado |
      | valor1     | esperado1          |
      | valor2     | esperado2          |
      | valor3     | esperado3          |
```

---

## Guia de Preenchimento

### Tags (primeira linha)

```gherkin
@tag_dominio @tag_capacidade @tag_ci
```

**Tags obrigatórias:**
- **Domínio**: `@sdk`, `@server`, `@http`, `@stdio`
- **CI**: `@ci-fast`, `@ci-int`, `@e2e`

**Tags opcionais:**
- **Capacidade**: `@contexto`, `@streaming`, `@capability:tool_calling`, `@fallback`
- **Integração**: `@mcp`, `@broker`, `@tecnospeed`
- **Categoria**: `@observabilidade`, `@seguranca`, `@erro`

**Exemplo:**
```gherkin
@sdk @contexto @ci-fast
```

---

### FUNCIONALIDADE

**PARA**: Benefício ou valor que esta feature entrega
**COMO**: Quem se beneficia (desenvolvedor, usuário final, admin)
**QUERO**: Capacidade específica desejada

**Exemplo:**
```gherkin
FUNCIONALIDADE: Chat básico no Forge SDK
  PARA enviar mensagens e receber respostas de LLMs
  COMO um desenvolvedor Python
  QUERO usar uma interface consistente independente do provedor
```

---

### CONTEXTO

Pré-condições comuns a **todos** os cenários desta feature.

**Exemplo:**
```gherkin
CONTEXTO:
  DADO que o Forge está instalado
  E o ambiente de teste está configurado
  E o provedor "echo" está disponível
```

---

### CENÁRIO (Happy Path)

Fluxo principal de sucesso.

**Estrutura:**
- **DADO**: Pré-condição (contexto inicial)
- **QUANDO**: Ação executada
- **ENTÃO**: Resultado esperado
- **E**: Efeito colateral observável

**Exemplo:**
```gherkin
CENÁRIO: Enviar mensagem simples e receber resposta
  DADO que o Forge está configurado com o provedor "echo"
  QUANDO envio a mensagem "Olá, mundo!"
  ENTÃO recebo uma resposta contendo "Olá, mundo!"
  E a resposta tem formato válido de ChatResponse
  E o log registra o evento com status "success"
```

---

### CENÁRIO (Erro)

Casos de erro e tratamento.

**Exemplo:**
```gherkin
CENÁRIO: Erro ao usar provedor não configurado
  DADO que o Forge não tem nenhum provedor configurado
  QUANDO tento enviar uma mensagem
  ENTÃO recebo um erro do tipo ConfigurationError
  E a mensagem de erro contém "Provedor não configurado"
  E o log registra o erro com severidade "ERROR"
```

---

### ESQUEMA DO CENÁRIO

Para testar o mesmo comportamento com múltiplos valores.

**Exemplo:**
```gherkin
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

## Boas Práticas

### ✅ Fazer

- **Linguagem de negócio** (não implementação)
- **Um comportamento por cenário**
- **Resultados observáveis** (resposta, log, estado)
- **Cenários curtos** (máximo 5-7 steps)
- **Incluir casos de erro** (não só happy path)

### ❌ Evitar

- Detalhes de implementação ("chamar método X da classe Y")
- Múltiplos comportamentos no mesmo cenário
- Resultados não verificáveis ("sistema processa internamente")
- Cenários longos com muitos steps
- Apenas happy path (sem casos de erro)

---

## Checklist de Qualidade

Antes de finalizar a feature, validar:

- [ ] Tags aplicadas (domínio + CI + capacidade se aplicável)
- [ ] FUNCIONALIDADE descreve claramente o valor
- [ ] CONTEXTO evita repetição nos cenários
- [ ] Pelo menos 1 cenário de sucesso
- [ ] Pelo menos 1 cenário de erro
- [ ] Steps em linguagem de negócio (não técnica)
- [ ] Resultados são observáveis e verificáveis
- [ ] Cenários curtos (≤ 7 steps)
- [ ] EXEMPLOS no ESQUEMA DO CENÁRIO cobrem casos relevantes
- [ ] Revisão com PO/Stakeholder

---

## Exemplo Completo

```gherkin
# 10_forge_core/sessao.feature

@sdk @contexto @ci-fast
FUNCIONALIDADE: Gestão de sessões no Forge
  PARA manter histórico de conversas
  COMO um desenvolvedor
  QUERO que mensagens na mesma sessão preservem contexto

  CONTEXTO:
    DADO que o Forge está instalado
    E o provedor "echo" está configurado

  CENÁRIO: Preservar histórico na mesma sessão
    DADO uma sessão com id "abc123"
    E enviei a mensagem "Olá" anteriormente
    QUANDO envio a mensagem "Como você está?"
    ENTÃO a resposta considera o contexto de "Olá"
    E o histórico da sessão contém ambas as mensagens

  CENÁRIO: Isolar contextos entre sessões diferentes
    DADO uma sessão "sessao_A" com mensagem "Olá"
    E uma sessão "sessao_B" com mensagem "Oi"
    QUANDO consulto o histórico de "sessao_A"
    ENTÃO vejo apenas "Olá"
    E não vejo "Oi"

  CENÁRIO: Erro ao usar sessão inexistente
    DADO que a sessão "sessao_inexistente" não existe
    QUANDO tento enviar mensagem para essa sessão
    ENTÃO recebo um erro do tipo SessionNotFoundError
    E a mensagem sugere criar nova sessão
```

---

**Autor:** Forge Framework Team
**Versão:** 1.0
**Data:** 2025-11-04
