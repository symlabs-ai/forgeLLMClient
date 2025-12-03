# language: pt

@sdk @provider @openai @ci-int
FUNCIONALIDADE: Provedor OpenAI
  PARA usar modelos da OpenAI
  COMO um desenvolvedor Python
  QUERO integrar com a API da OpenAI de forma transparente

  CONTEXTO:
    DADO que o ForgeLLMClient esta instalado
    E a variavel de ambiente OPENAI_API_KEY esta configurada

  # ========== CENARIOS DE CONFIGURACAO ==========

  CENARIO: Configurar provedor OpenAI com API key
    QUANDO configuro o cliente com o provedor "openai"
    ENTAO o cliente esta pronto para uso
    E o provedor ativo e "openai"

  CENARIO: Configurar OpenAI com modelo especifico
    QUANDO configuro o cliente com o provedor "openai" e modelo "gpt-4"
    ENTAO o modelo ativo e "gpt-4"

  CENARIO: Configurar OpenAI com modelo GPT-3.5
    QUANDO configuro o cliente com o provedor "openai" e modelo "gpt-3.5-turbo"
    ENTAO o modelo ativo e "gpt-3.5-turbo"

  # ========== CENARIOS DE CHAT ==========

  @slow
  CENARIO: Enviar mensagem para GPT-4
    DADO que o cliente esta configurado com provedor "openai" e modelo "gpt-4"
    QUANDO envio a mensagem "Diga apenas: teste"
    ENTAO recebo uma resposta com status "success"
    E a resposta contem texto
    E provider.id na resposta e "openai"

  @slow @streaming
  CENARIO: Streaming com OpenAI
    DADO que o cliente esta configurado com provedor "openai"
    QUANDO envio a mensagem "Conte de 1 a 3" com streaming habilitado
    ENTAO recebo chunks progressivamente
    E a resposta final esta completa

  # ========== CENARIOS DE TOOL CALLING ==========

  @slow @tools
  CENARIO: Tool calling com OpenAI
    DADO que o cliente esta configurado com provedor "openai"
    E a ferramenta "get_weather" esta registrada
    QUANDO envio a mensagem "Qual o clima em Sao Paulo?"
    ENTAO recebo uma resposta com tool_call
    E o tool_call tem formato normalizado
    E o tool_call.name e "get_weather"

  # ========== CENARIOS DE ERRO ==========

  @error
  CENARIO: Erro com API key invalida
    DADO que configuro o cliente com api_key "sk-invalida"
    QUANDO tento enviar uma mensagem
    ENTAO recebo um erro do tipo "AuthenticationError"
    E a mensagem de erro contem "authentication" ou "api_key"
