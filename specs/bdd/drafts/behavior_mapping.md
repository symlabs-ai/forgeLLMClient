# Mapeamento de Comportamentos — ForgeLLMClient

> Derivado de `docs/visao.md` e `docs/aprovacao_mvp.md`
> Data: 2025-12-03

---

## Escopo do MVP (Fase 1)

Conforme `aprovacao_mvp.md`, o MVP inclui:
- Interface unificada de chat (sync + streaming)
- Tool Calling normalizado
- Consumo de tokens por requisicao
- Normalizacao de respostas
- Suporte OpenAI + Anthropic

---

## ValueTrack 1: PortableChat

**Tipo:** VALUE
**Dominio:** 10_forge_core/
**Descricao:** Enviar mensagens para qualquer LLM com interface única (sync e streaming)

### Comportamentos Identificados

#### 1. Chat Sincrono Basico
- **Acao:** Usuario envia mensagem para o LLM
- **Resultado esperado:** Recebe resposta completa
- **Criterio:** Resposta contem texto e metadados
- **Cenario BDD:** `Enviar mensagem e receber resposta`

#### 2. Chat com Streaming
- **Acao:** Usuario envia mensagem solicitando streaming
- **Resultado esperado:** Recebe resposta em chunks progressivos
- **Criterio:** Chunks chegam incrementalmente, resposta final é completa
- **Cenario BDD:** `Enviar mensagem com streaming`

#### 3. Configuracao de Provedor
- **Acao:** Usuario configura provedor antes de usar
- **Resultado esperado:** Cliente pronto para enviar mensagens
- **Criterio:** Provedor é reconhecido e validado
- **Cenario BDD:** `Configurar provedor valido`

### Casos de Erro

#### 1. Provedor Nao Configurado
- **Condicao:** Usuario tenta enviar sem configurar provedor
- **Tratamento esperado:** Erro claro indicando necessidade de configuracao
- **Cenario BDD:** `Erro ao usar sem provedor configurado`

#### 2. Provedor Invalido
- **Condicao:** Usuario configura provedor que nao existe
- **Tratamento esperado:** Erro claro indicando provedor invalido
- **Cenario BDD:** `Erro ao configurar provedor invalido`

#### 3. Timeout de Requisicao
- **Condicao:** LLM demora mais que o timeout configurado
- **Tratamento esperado:** Erro de timeout com informacao clara
- **Cenario BDD:** `Timeout ao aguardar resposta`

#### 4. Erro de API do Provedor
- **Condicao:** Provedor retorna erro (rate limit, auth, etc)
- **Tratamento esperado:** Erro normalizado com detalhes do provedor
- **Cenario BDD:** `Erro de API do provedor`

---

## ValueTrack 2: UnifiedTools

**Tipo:** VALUE
**Dominio:** 10_forge_core/
**Descricao:** Tool Calling padronizado entre provedores

### Comportamentos Identificados

#### 1. Registrar Tools
- **Acao:** Usuario registra ferramentas disponiveis para o LLM
- **Resultado esperado:** Tools sao reconhecidas e enviadas ao provedor
- **Criterio:** Formato interno é convertido para formato do provedor
- **Cenario BDD:** `Registrar ferramentas para o LLM`

#### 2. LLM Solicita Tool Call
- **Acao:** LLM decide chamar uma ferramenta
- **Resultado esperado:** Usuario recebe tool_call normalizado
- **Criterio:** Formato é consistente independente do provedor
- **Cenario BDD:** `Receber solicitacao de tool call`

#### 3. Responder Tool Call
- **Acao:** Usuario executa tool e retorna resultado
- **Resultado esperado:** Resultado é enviado ao LLM no formato correto
- **Criterio:** LLM continua conversa com resultado da tool
- **Cenario BDD:** `Enviar resultado de tool call`

### Casos de Erro

#### 1. Tool Nao Registrada
- **Condicao:** LLM solicita tool que nao foi registrada
- **Tratamento esperado:** Erro claro indicando tool desconhecida
- **Cenario BDD:** `Erro ao receber tool call de tool nao registrada`

#### 2. Formato de Resposta Invalido
- **Condicao:** Usuario envia resposta de tool em formato invalido
- **Tratamento esperado:** Erro de validacao com detalhes
- **Cenario BDD:** `Erro ao enviar resposta de tool invalida`

---

## ValueTrack 3: TokenUsage

**Tipo:** SUPPORT
**Dominio:** 10_forge_core/
**Descricao:** Informar consumo de tokens em cada requisicao

### Comportamentos Identificados

#### 1. Tokens em Resposta Sincrona
- **Acao:** Usuario envia mensagem e recebe resposta
- **Resultado esperado:** Resposta inclui contagem de tokens (input, output, total)
- **Criterio:** Valores sao numericos e consistentes
- **Cenario BDD:** `Receber contagem de tokens na resposta`

#### 2. Tokens em Streaming
- **Acao:** Usuario recebe resposta via streaming
- **Resultado esperado:** Contagem final de tokens disponivel ao terminar stream
- **Criterio:** Tokens disponiveis após ultimo chunk
- **Cenario BDD:** `Receber contagem de tokens apos streaming`

### Casos de Erro

#### 1. Provedor Nao Informa Tokens
- **Condicao:** Provedor nao retorna informacao de tokens
- **Tratamento esperado:** Campo de tokens é None ou estimado
- **Cenario BDD:** `Tratar provedor que nao informa tokens`

---

## ValueTrack 4: ProviderNormalization

**Tipo:** SUPPORT
**Dominio:** 10_forge_core/
**Descricao:** Normalizacao de respostas entre provedores

### Comportamentos Identificados

#### 1. Formato de Resposta Unificado
- **Acao:** Usuario recebe resposta de qualquer provedor
- **Resultado esperado:** Formato é identico independente do provedor
- **Criterio:** Mesmos campos, mesmos tipos, mesma estrutura
- **Cenario BDD:** `Resposta tem formato unificado`

#### 2. Metadados do Provedor
- **Acao:** Usuario quer saber qual provedor respondeu
- **Resultado esperado:** Metadados incluem provider_id e model
- **Criterio:** Informacao é precisa e acessivel
- **Cenario BDD:** `Resposta inclui metadados do provedor`

---

## Provedores: OpenAI

**Tipo:** SUPPORT
**Dominio:** 10_forge_core/providers/
**Descricao:** Suporte ao provedor OpenAI

### Comportamentos Identificados

#### 1. Configurar OpenAI
- **Acao:** Usuario configura cliente com provedor OpenAI
- **Resultado esperado:** Cliente conecta e valida credenciais
- **Criterio:** API key é validada
- **Cenario BDD:** `Configurar provedor OpenAI`

#### 2. Chat com GPT-4
- **Acao:** Usuario envia mensagem usando modelo GPT-4
- **Resultado esperado:** Resposta é recebida e normalizada
- **Criterio:** Formato segue padrao unificado
- **Cenario BDD:** `Enviar mensagem para GPT-4`

#### 3. Tool Calling OpenAI
- **Acao:** Usuario registra tools e LLM as utiliza
- **Resultado esperado:** Tool calls sao normalizados do formato OpenAI
- **Criterio:** Formato interno é consistente
- **Cenario BDD:** `Tool calling com OpenAI`

---

## Provedores: Anthropic

**Tipo:** SUPPORT
**Dominio:** 10_forge_core/providers/
**Descricao:** Suporte ao provedor Anthropic

### Comportamentos Identificados

#### 1. Configurar Anthropic
- **Acao:** Usuario configura cliente com provedor Anthropic
- **Resultado esperado:** Cliente conecta e valida credenciais
- **Criterio:** API key é validada
- **Cenario BDD:** `Configurar provedor Anthropic`

#### 2. Chat com Claude
- **Acao:** Usuario envia mensagem usando modelo Claude
- **Resultado esperado:** Resposta é recebida e normalizada
- **Criterio:** Formato segue padrao unificado
- **Cenario BDD:** `Enviar mensagem para Claude`

#### 3. Tool Calling Anthropic
- **Acao:** Usuario registra tools e LLM as utiliza
- **Resultado esperado:** Tool calls sao normalizados do formato Anthropic
- **Criterio:** Formato interno é consistente
- **Cenario BDD:** `Tool calling com Anthropic`

---

## Resumo do Mapeamento

| ValueTrack | Tipo | Dominio | Cenarios Sucesso | Cenarios Erro |
|------------|------|---------|------------------|---------------|
| PortableChat | VALUE | 10_forge_core | 3 | 4 |
| UnifiedTools | VALUE | 10_forge_core | 3 | 2 |
| TokenUsage | SUPPORT | 10_forge_core | 2 | 1 |
| ProviderNormalization | SUPPORT | 10_forge_core | 2 | 0 |
| OpenAI Provider | SUPPORT | 10_forge_core/providers | 3 | 0 |
| Anthropic Provider | SUPPORT | 10_forge_core/providers | 3 | 0 |

**Total: 16 cenarios de sucesso + 7 cenarios de erro = 23 cenarios**

---

## Proxima Etapa

Com este mapeamento pronto, avancar para:
**BDD Etapa 2: Escrita de Features Gherkin**

---

*Documento gerado pelo BDD Coach*
*Data: 2025-12-03*
*Versao: 1.0*
