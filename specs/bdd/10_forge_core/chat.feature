# language: pt

@sdk @chat @ci-fast
FUNCIONALIDADE: Chat basico com LLM
  PARA enviar mensagens e receber respostas de LLMs
  COMO um desenvolvedor Python
  QUERO usar uma interface unica independente do provedor

  CONTEXTO:
    DADO que o ForgeLLMClient esta instalado
    E o ambiente de teste esta configurado

  # ========== CENARIOS DE SUCESSO ==========

  @sync
  CENARIO: Enviar mensagem e receber resposta
    DADO que o cliente esta configurado com o provedor "mock"
    QUANDO envio a mensagem "Ola, mundo!"
    ENTAO recebo uma resposta com status "success"
    E a resposta contem texto nao vazio
    E a resposta tem formato ChatResponse valido

  @sync
  CENARIO: Enviar mensagem com parametros opcionais
    DADO que o cliente esta configurado com o provedor "mock"
    QUANDO envio a mensagem "Explique Python" com temperatura 0.7
    ENTAO recebo uma resposta com status "success"
    E a resposta contem texto nao vazio

  @streaming
  CENARIO: Enviar mensagem com streaming
    DADO que o cliente esta configurado com o provedor "mock"
    QUANDO envio a mensagem "Conte ate 5" com streaming habilitado
    ENTAO recebo chunks de resposta progressivamente
    E o ultimo chunk indica fim do stream
    E a resposta final esta completa

  # ========== CENARIOS DE ERRO ==========

  @error
  CENARIO: Erro ao usar sem provedor configurado
    DADO que o cliente NAO esta configurado com nenhum provedor
    QUANDO tento enviar uma mensagem
    ENTAO recebo um erro do tipo "ConfigurationError"
    E a mensagem de erro contem "provedor nao configurado"

  @error
  CENARIO: Erro ao enviar mensagem vazia
    DADO que o cliente esta configurado com o provedor "mock"
    QUANDO envio uma mensagem vazia
    ENTAO recebo um erro do tipo "ValidationError"
    E a mensagem de erro contem "mensagem nao pode ser vazia"

  @error @timeout
  CENARIO: Timeout ao aguardar resposta
    DADO que o cliente esta configurado com o provedor "slow-mock"
    E o timeout esta configurado para 1 segundo
    QUANDO envio a mensagem "Mensagem que demora"
    ENTAO recebo um erro do tipo "TimeoutError"
    E a mensagem de erro contem "timeout"
