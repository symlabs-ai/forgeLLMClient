# language: pt

@sdk @config @ci-fast
FUNCIONALIDADE: Configuracao de provedor
  PARA usar diferentes provedores de LLM
  COMO um desenvolvedor Python
  QUERO configurar o cliente com o provedor desejado

  CONTEXTO:
    DADO que o ForgeLLMClient esta instalado

  # ========== CENARIOS DE SUCESSO ==========

  CENARIO: Configurar provedor valido
    QUANDO configuro o cliente com o provedor "mock"
    ENTAO o cliente esta pronto para uso
    E o provedor ativo e "mock"

  CENARIO: Configurar provedor com API key
    QUANDO configuro o cliente com o provedor "openai" e api_key "sk-test-123"
    ENTAO o cliente esta pronto para uso
    E o provedor ativo e "openai"

  CENARIO: Configurar provedor com modelo especifico
    QUANDO configuro o cliente com o provedor "openai" e modelo "gpt-4"
    ENTAO o cliente esta pronto para uso
    E o modelo ativo e "gpt-4"

  CENARIO: Reconfigurar provedor em runtime
    DADO que o cliente esta configurado com o provedor "mock"
    QUANDO reconfiguro o cliente para o provedor "openai"
    ENTAO o provedor ativo e "openai"

  # ========== CENARIOS DE ERRO ==========

  @error
  CENARIO: Erro ao configurar provedor invalido
    QUANDO tento configurar o cliente com o provedor "provedor-inexistente"
    ENTAO recebo um erro do tipo "ProviderNotFoundError"
    E a mensagem de erro contem "provedor nao encontrado"

  @error
  CENARIO: Erro ao configurar sem API key quando necessario
    QUANDO tento configurar o cliente com o provedor "openai" sem api_key
    ENTAO recebo um erro do tipo "ConfigurationError"
    E a mensagem de erro contem "api_key"
