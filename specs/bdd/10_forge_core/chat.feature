@sdk @chat @ci-fast
Feature: Basic chat with LLM
  In order to send messages and receive responses from LLMs
  As a Python developer
  I want to use a unified interface regardless of provider

  Background:
    Given the ForgeLLMClient is installed
    And the test environment is configured

  # ========== SUCCESS SCENARIOS ==========

  @sync
  Scenario: Send message and receive response
    Given the client is configured with provider "mock"
    When I send the message "Hello, world!"
    Then I receive a response with status "success"
    And the response contains non-empty text
    And the response has valid ChatResponse format

  @sync
  Scenario: Send message with optional parameters
    Given the client is configured with provider "mock"
    When I send the message "Explain Python" with temperature 0.7
    Then I receive a response with status "success"
    And the response contains non-empty text

  @streaming
  Scenario: Send message with streaming
    Given the client is configured with provider "mock"
    When I send the message "Count to 5" with streaming enabled
    Then I receive response chunks progressively
    And the last chunk indicates end of stream
    And the final response is complete

  # ========== ERROR SCENARIOS ==========

  @error
  Scenario: Error when using without configured provider
    Given the client is NOT configured with any provider
    When I try to send a message
    Then I receive an error of type "RuntimeError"
    And the error message contains "nao configurado"

  @error
  Scenario: Error when sending empty message
    Given the client is configured with provider "mock"
    When I send an empty message
    Then I receive an error of type "ValidationError"
    And the error message contains "vazia"
