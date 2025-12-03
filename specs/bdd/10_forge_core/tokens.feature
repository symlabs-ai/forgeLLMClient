# language: pt

@sdk @tokens @ci-fast
FUNCIONALIDADE: Contagem de tokens
  PARA monitorar custos e uso de tokens
  COMO um desenvolvedor Python
  QUERO receber informacoes de consumo em cada requisicao

  CONTEXTO:
    DADO que o ForgeLLMClient esta instalado
    E o cliente esta configurado com o provedor "mock"

  # ========== CENARIOS DE SUCESSO ==========

  @sync
  CENARIO: Receber contagem de tokens na resposta sincrona
    QUANDO envio a mensagem "Ola, mundo!"
    ENTAO a resposta contem informacao de tokens
    E tokens.input e um numero maior que zero
    E tokens.output e um numero maior que zero
    E tokens.total e igual a input + output

  @streaming
  CENARIO: Receber contagem de tokens apos streaming
    QUANDO envio a mensagem "Conte ate 3" com streaming habilitado
    E o streaming termina
    ENTAO a resposta final contem informacao de tokens
    E tokens.total e um numero maior que zero

  CENARIO: Tokens zerados quando provedor nao informa
    DADO que o cliente esta configurado com o provedor "mock-sem-tokens"
    QUANDO envio a mensagem "Mensagem qualquer"
    ENTAO a resposta contem informacao de tokens
    E tokens.input e None ou zero
    E tokens.output e None ou zero

  # ========== CENARIOS DE VALIDACAO ==========

  CENARIO: Tokens consistentes entre chamadas
    QUANDO envio a mensagem "Mensagem curta"
    E armazeno os tokens da resposta
    E envio a mesma mensagem "Mensagem curta" novamente
    ENTAO os tokens de input sao aproximadamente iguais
