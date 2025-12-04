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
