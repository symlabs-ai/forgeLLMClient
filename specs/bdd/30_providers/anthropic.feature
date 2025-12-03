# language: pt

@sdk @provider @anthropic @ci-int
FUNCIONALIDADE: Provedor Anthropic
  PARA usar modelos da Anthropic (Claude)
  COMO um desenvolvedor Python
  QUERO integrar com a API da Anthropic de forma transparente

  CONTEXTO:
    DADO que o ForgeLLMClient esta instalado
    E a variavel de ambiente ANTHROPIC_API_KEY esta configurada

  # ========== CENARIOS DE CONFIGURACAO ==========

  CENARIO: Configurar provedor Anthropic com API key
    QUANDO configuro o cliente com o provedor "anthropic"
    ENTAO o cliente esta pronto para uso
    E o provedor ativo e "anthropic"

  CENARIO: Configurar Anthropic com modelo Claude 3
    QUANDO configuro o cliente com o provedor "anthropic" e modelo "claude-3-sonnet-20240229"
    ENTAO o modelo ativo e "claude-3-sonnet-20240229"

  CENARIO: Configurar Anthropic com modelo Claude 3.5
    QUANDO configuro o cliente com o provedor "anthropic" e modelo "claude-3-5-sonnet-20241022"
    ENTAO o modelo ativo e "claude-3-5-sonnet-20241022"

  # ========== CENARIOS DE CHAT ==========

  @slow
  CENARIO: Enviar mensagem para Claude
    DADO que o cliente esta configurado com provedor "anthropic"
    QUANDO envio a mensagem "Diga apenas: teste"
    ENTAO recebo uma resposta com status "success"
    E a resposta contem texto
    E provider.id na resposta e "anthropic"

  @slow @streaming
  CENARIO: Streaming com Anthropic
    DADO que o cliente esta configurado com provedor "anthropic"
    QUANDO envio a mensagem "Conte de 1 a 3" com streaming habilitado
    ENTAO recebo chunks progressivamente
    E a resposta final esta completa

  # ========== CENARIOS DE TOOL CALLING ==========

  @slow @tools
  CENARIO: Tool calling com Anthropic
    DADO que o cliente esta configurado com provedor "anthropic"
    E a ferramenta "get_weather" esta registrada
    QUANDO envio a mensagem "Qual o clima em Sao Paulo?"
    ENTAO recebo uma resposta com tool_call
    E o tool_call tem formato normalizado
    E o tool_call.name e "get_weather"

  # ========== CENARIOS DE NORMALIZACAO ==========

  CENARIO: Resposta Anthropic segue formato unificado
    DADO que o cliente esta configurado com provedor "anthropic"
    QUANDO envio a mensagem "Teste de formato"
    ENTAO a resposta e do tipo ChatResponse
    E a resposta tem os mesmos campos que resposta de outros provedores

  # ========== CENARIOS DE ERRO ==========

  @error
  CENARIO: Erro com API key invalida
    DADO que configuro o cliente com api_key "sk-ant-invalida"
    QUANDO tento enviar uma mensagem
    ENTAO recebo um erro do tipo "AuthenticationError"
    E a mensagem de erro contem "authentication" ou "api_key"
