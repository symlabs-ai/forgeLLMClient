@sdk @tokens @ci-fast
Feature: Token counting
  In order to monitor costs and token usage
  As a Python developer
  I want to receive consumption information in each request

  Background:
    Given the ForgeLLMClient is installed
    And the client is configured with provider "mock"

  # ========== SUCCESS SCENARIOS ==========

  @sync
  Scenario: Receive token count in synchronous response
    When I send the message "Hello, world!"
    Then the response contains token information
    And usage.prompt_tokens is a number greater than zero
    And usage.completion_tokens is a number greater than zero
    And usage.total_tokens equals prompt plus completion

  @streaming
  Scenario: Receive token count after streaming
    When I send the message "Count to 3" with streaming enabled
    And the streaming completes
    Then the final response contains token information
    And usage.total_tokens is a number greater than zero

  Scenario: Tokens zero when provider does not inform
    Given the client is configured with provider "mock-no-tokens"
    When I send the message "Any message"
    Then the response contains token information
    And usage.prompt_tokens is zero
    And usage.completion_tokens is zero

  # ========== VALIDATION SCENARIOS ==========

  Scenario: Tokens consistent between calls
    When I send the message "Short message"
    And I store the response tokens
    And I send the same message "Short message" again
    Then the input tokens are approximately equal
