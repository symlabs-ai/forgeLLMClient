# language: pt

@sdk @response @ci-fast
FUNCIONALIDADE: Formato de resposta unificado
  PARA trabalhar com respostas de qualquer provedor
  COMO um desenvolvedor Python
  QUERO receber respostas em formato padronizado

  CONTEXTO:
    DADO que o ForgeLLMClient esta instalado

  # ========== CENARIOS DE SUCESSO ==========

  CENARIO: Resposta tem formato ChatResponse unificado
    DADO que o cliente esta configurado com o provedor "mock"
    QUANDO envio a mensagem "Qualquer mensagem"
    ENTAO a resposta e do tipo ChatResponse
    E a resposta tem campo "content" com o texto
    E a resposta tem campo "role" igual a "assistant"
    E a resposta tem campo "provider" com informacoes do provedor
    E a resposta tem campo "model" com o modelo usado
    E a resposta tem campo "tokens" com contagem

  CENARIO: Metadados do provedor na resposta
    DADO que o cliente esta configurado com o provedor "mock"
    QUANDO envio a mensagem "Qualquer mensagem"
    ENTAO a resposta contem provider.id igual a "mock"
    E a resposta contem provider.model com o modelo usado

  CENARIO: Formato identico entre provedores diferentes
    DADO que o cliente esta configurado com o provedor "mock-openai"
    QUANDO envio a mensagem "Teste OpenAI" e armazeno a resposta como R1
    E reconfiguro o cliente para o provedor "mock-anthropic"
    E envio a mensagem "Teste Anthropic" e armazeno a resposta como R2
    ENTAO R1 e R2 tem os mesmos campos
    E R1.content e uma string
    E R2.content e uma string
    E R1.tokens e R2.tokens tem a mesma estrutura

  # ========== CENARIOS DE STREAMING ==========

  @streaming
  CENARIO: Chunks de streaming tem formato padronizado
    DADO que o cliente esta configurado com o provedor "mock"
    QUANDO envio a mensagem "Streaming test" com streaming habilitado
    ENTAO cada chunk e do tipo ChatResponseChunk
    E cada chunk tem campo "delta" com texto incremental
    E cada chunk tem campo "index" com posicao no stream
    E o ultimo chunk tem campo "finish_reason"
