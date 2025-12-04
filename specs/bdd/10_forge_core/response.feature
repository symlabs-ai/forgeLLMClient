@sdk @response @ci-fast
Feature: Unified response format
  In order to work with responses from any provider
  As a Python developer
  I want to receive responses in a standardized format

  Background:
    Given the ForgeLLMClient is installed

  # ========== SUCCESS SCENARIOS ==========

  Scenario: Response has unified ChatResponse format
    Given the client is configured with provider "mock"
    When I send the message "Any message"
    Then the response is of type ChatResponse
    And the response has field "content" with the text
    And the response has field "role" equal to "assistant"
    And the response has field "provider" with provider information
    And the response has field "model" with the model used
    And the response has field "tokens" with count

  Scenario: Provider metadata in response
    Given the client is configured with provider "mock"
    When I send the message "Any message"
    Then the response contains provider.id equal to "mock"
    And the response contains provider.model with the model used

  Scenario: Identical format between different providers
    Given the client is configured with provider "mock"
    When I send the message "Test Mock" and store the response as R1
    And I reconfigure the client to provider "mock-alt"
    And I send the message "Test Alt" and store the response as R2
    Then R1 and R2 have the same fields
    And R1.content is a string
    And R2.content is a string
    And R1.tokens and R2.tokens have the same structure

  # ========== STREAMING SCENARIOS ==========

  @streaming
  Scenario: Streaming chunks have standardized format
    Given the client is configured with provider "mock"
    When I send the message "Streaming test" with streaming enabled
    Then each chunk is of type ChatResponseChunk
    And each chunk has field "delta" with incremental text
    And each chunk has field "index" with position in stream
    And the last chunk has field "finish_reason"
