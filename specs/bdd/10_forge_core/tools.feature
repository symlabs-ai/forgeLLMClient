# language: pt

@sdk @tools @ci-fast
FUNCIONALIDADE: Tool Calling unificado
  PARA usar ferramentas com qualquer LLM
  COMO um desenvolvedor Python
  QUERO registrar tools e receber chamadas em formato padronizado

  CONTEXTO:
    DADO que o ForgeLLMClient esta instalado
    E o cliente esta configurado com o provedor "mock-tools"

  # ========== CENARIOS DE SUCESSO ==========

  CENARIO: Registrar ferramentas para o LLM
    QUANDO registro a ferramenta "calculadora" com descricao "Faz calculos matematicos"
    E registro a ferramenta "clima" com descricao "Consulta previsao do tempo"
    ENTAO o cliente tem 2 ferramentas registradas
    E a ferramenta "calculadora" esta disponivel
    E a ferramenta "clima" esta disponivel

  CENARIO: Receber solicitacao de tool call
    DADO que a ferramenta "calculadora" esta registrada
    QUANDO envio a mensagem "Quanto e 2 + 2?"
    ENTAO recebo uma resposta com tool_call
    E o tool_call tem nome "calculadora"
    E o tool_call tem argumentos em formato JSON
    E o tool_call tem um id unico

  CENARIO: Enviar resultado de tool call
    DADO que a ferramenta "calculadora" esta registrada
    E recebi um tool_call com id "tc_123" para "calculadora"
    QUANDO envio o resultado "4" para o tool_call "tc_123"
    ENTAO recebo uma resposta final do LLM
    E a resposta incorpora o resultado da ferramenta

  CENARIO: Multiplos tool calls em uma resposta
    DADO que as ferramentas "calculadora" e "clima" estao registradas
    QUANDO envio a mensagem "Quanto e 10 + 5 e qual o clima em SP?"
    ENTAO recebo uma resposta com multiplos tool_calls
    E existe tool_call para "calculadora"
    E existe tool_call para "clima"

  # ========== CENARIOS DE ERRO ==========

  @error
  CENARIO: Erro ao registrar ferramenta sem nome
    QUANDO tento registrar uma ferramenta sem nome
    ENTAO recebo um erro do tipo "ValidationError"
    E a mensagem de erro contem "nome da ferramenta"

  @error
  CENARIO: Erro ao enviar resultado para tool_call inexistente
    QUANDO tento enviar resultado para tool_call "tc_inexistente"
    ENTAO recebo um erro do tipo "ToolCallNotFoundError"
    E a mensagem de erro contem "tool_call nao encontrado"
