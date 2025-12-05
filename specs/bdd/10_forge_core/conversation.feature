@conversation @forge-core
Feature: Conversation History
  Como usuario do ForgeLLMClient
  Eu quero manter conversas multi-turn
  Para ter contexto entre mensagens

  Background:
    Given um client configurado com provider "mock"

  @conversation-basic
  Scenario: Criar conversa simples
    When eu crio uma conversa
    Then a conversa deve estar vazia
    And a conversa nao deve ter system prompt

  @conversation-system
  Scenario: Criar conversa com system prompt
    When eu crio uma conversa com system prompt "Voce e um assistente"
    Then a conversa deve ter system prompt "Voce e um assistente"

  @conversation-history
  Scenario: Conversa mantem historico
    Given uma conversa criada
    When eu envio a mensagem "Ola"
    And eu recebo a resposta "Oi, como posso ajudar?"
    Then o historico deve ter 2 mensagens
    And a primeira mensagem deve ser do usuario com "Ola"
    And a segunda mensagem deve ser do assistant com "Oi, como posso ajudar?"

  @conversation-multi-turn
  Scenario: Conversa multi-turn envia historico completo
    Given uma conversa com system prompt "Seja breve"
    And a conversa tem mensagem do usuario "Ola"
    And a conversa tem mensagem do assistant "Oi"
    When eu envio a mensagem "Tudo bem?"
    Then o provider deve receber 4 mensagens
    And a primeira mensagem enviada deve ser system "Seja breve"

  @conversation-clear
  Scenario: Limpar historico da conversa
    Given uma conversa com historico
    When eu limpo a conversa
    Then a conversa deve estar vazia
    But a conversa deve manter o system prompt

  @conversation-access
  Scenario: Acessar mensagens do historico
    Given uma conversa com historico
    When eu acesso as mensagens
    Then eu devo receber uma lista de Message
    And cada mensagem deve ter role e content

  # Sprint 14 - Hot-Swap & Context Management

  @conversation-max-tokens
  Scenario: Conversa com limite de tokens
    When eu crio uma conversa com max_tokens 100
    And eu adiciono muitas mensagens longas
    Then o historico deve ser truncado por tokens
    And token_count deve ser menor ou igual a 100

  @conversation-metadata
  Scenario: Mensagens com metadados
    Given uma conversa criada
    When eu adiciono mensagem com provider "openai" e model "gpt-4"
    Then a mensagem deve ter timestamp
    And a mensagem deve ter provider "openai"
    And a mensagem deve ter model "gpt-4"

  @conversation-hot-swap
  Scenario: Hot-swap de provider mid-conversation
    Given uma conversa com historico
    When eu troco o provider para "anthropic"
    Then o historico deve ser preservado
    And o proximo chat deve usar o novo provider

  @conversation-provider-history
  Scenario: Rastrear historico de providers
    Given uma conversa criada
    When eu uso provider "openai" para uma mensagem
    And eu troco o provider para "anthropic"
    And eu uso provider "anthropic" para uma mensagem
    Then provider_history deve conter "openai" e "anthropic"
    And last_provider deve ser "anthropic"

  @conversation-serialization
  Scenario: Serializar e restaurar conversa
    Given uma conversa com historico
    When eu serializo a conversa com to_dict
    And eu restauro com from_dict
    Then a conversa restaurada deve ter o mesmo historico
    And a conversa restaurada deve ter o mesmo system prompt

  @conversation-enhanced-messages
  Scenario: Acessar mensagens com metadados
    Given uma conversa com historico enriquecido
    When eu acesso enhanced_messages
    Then cada mensagem deve ser EnhancedMessage
    And cada mensagem deve ter metadata com timestamp
