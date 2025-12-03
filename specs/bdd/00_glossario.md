# Glossario — Linguagem Ubiqua do ForgeLLMClient

Este documento define os termos usados nas especificacoes BDD, garantindo que todos (stakeholders, devs, QA) falem a mesma lingua.

---

## Termos do Dominio

### Cliente / Client
Instancia do ForgeLLMClient configurada e pronta para uso. O ponto de entrada para todas as operacoes.

### Provedor / Provider
Servico de LLM que processa as mensagens (ex: OpenAI, Anthropic). O cliente abstrai os provedores para oferecer interface unica.

### Mensagem / Message
Texto enviado ao LLM para processamento. Pode ser uma pergunta, instrucao ou continuacao de conversa.

### Resposta / Response
Retorno do LLM apos processar uma mensagem. Contem texto, metadados e informacoes de tokens.

### ChatResponse
Tipo padronizado de resposta do ForgeLLMClient. Independente do provedor, sempre tem os mesmos campos.

### Streaming
Modo de receber resposta em partes (chunks) progressivas, em vez de aguardar resposta completa.

### Chunk
Fragmento de resposta durante streaming. Contem parte do texto e metadados de posicao.

---

## Termos de Tool Calling

### Tool / Ferramenta
Funcao externa que o LLM pode solicitar que seja executada. Registrada pelo desenvolvedor antes do uso.

### Tool Call
Solicitacao do LLM para executar uma ferramenta especifica com determinados argumentos.

### Tool Result
Resposta do desenvolvedor apos executar a ferramenta solicitada pelo LLM.

---

## Termos de Configuracao

### API Key
Chave de autenticacao para acessar um provedor de LLM.

### Modelo / Model
Versao especifica do LLM a ser usado (ex: gpt-4, claude-3-sonnet).

### Timeout
Tempo maximo de espera por uma resposta antes de considerar erro.

### Temperatura / Temperature
Parametro que controla aleatoriedade das respostas (0 = deterministico, 1 = criativo).

---

## Termos de Metricas

### Tokens
Unidades de texto processadas pelo LLM. Usados para calcular custo e limites.

### Input Tokens
Tokens da mensagem enviada ao LLM.

### Output Tokens
Tokens da resposta gerada pelo LLM.

### Total Tokens
Soma de input + output tokens.

---

## Termos de Erro

### ConfigurationError
Erro de configuracao do cliente (ex: provedor nao configurado).

### ValidationError
Erro de validacao de entrada (ex: mensagem vazia).

### ProviderNotFoundError
Erro ao tentar usar provedor que nao existe.

### AuthenticationError
Erro de autenticacao com o provedor (ex: API key invalida).

### TimeoutError
Erro quando resposta demora mais que o timeout configurado.

### ToolCallNotFoundError
Erro ao tentar responder tool call que nao existe.

---

## Abreviacoes

| Sigla | Significado |
|-------|-------------|
| LLM | Large Language Model |
| API | Application Programming Interface |
| SDK | Software Development Kit |
| MCP | Model Context Protocol |
| CI | Continuous Integration |
| BDD | Behavior Driven Development |
| TDD | Test Driven Development |

---

*Ultima atualizacao: 2025-12-03*
