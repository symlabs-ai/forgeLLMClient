@sdk @provider @anthropic
Feature: Anthropic Provider
  In order to use Anthropic models (Claude)
  As a Python developer
  I want to integrate with the Anthropic API seamlessly

  Background:
    Given the ForgeLLMClient is installed
    And the environment variable ANTHROPIC_API_KEY is configured

  # ========== CONFIGURATION SCENARIOS ==========

  @ci-fast
  Scenario: Configure Anthropic provider with API key
    When I configure the client with provider "anthropic"
    Then the client is ready for use
    And the active provider is "anthropic"

  @ci-fast
  Scenario: Configure Anthropic with Claude 3 model
    When I configure the client with provider "anthropic" and model "claude-3-sonnet-20240229"
    Then the active model is "claude-3-sonnet-20240229"

  @ci-fast
  Scenario: Configure Anthropic with Claude 3.5 model
    When I configure the client with provider "anthropic" and model "claude-3-5-sonnet-20241022"
    Then the active model is "claude-3-5-sonnet-20241022"

  # ========== CHAT SCENARIOS ==========

  @slow @integration
  Scenario: Send message to Claude
    Given the client is configured with provider "anthropic"
    When I send the message "Say only: test"
    Then I receive a response with status "success"
    And the response contains text
    And provider.id in response is "anthropic"

  @slow @streaming @integration
  Scenario: Streaming with Anthropic
    Given the client is configured with provider "anthropic"
    When I send the message "Count from 1 to 3" with streaming enabled
    Then I receive chunks progressively
    And the final response is complete

  # ========== TOOL CALLING SCENARIOS ==========

  @slow @tools @integration
  Scenario: Tool calling with Anthropic
    Given the client is configured with provider "anthropic"
    And the tool "get_weather" is registered
    When I send the message "What is the weather in Sao Paulo?"
    Then I receive a response with tool_call
    And the tool_call has normalized format
    And the tool_call.name is "get_weather"

  # ========== NORMALIZATION SCENARIOS ==========

  @ci-fast
  Scenario: Anthropic response follows unified format
    Given the client is configured with provider "anthropic"
    When I send the message "Format test"
    Then the response is of type ChatResponse
    And the response has the same fields as responses from other providers

  # ========== ERROR SCENARIOS ==========

  @error @ci-fast
  Scenario: Error with invalid API key
    Given I configure the client with api_key "sk-ant-invalid"
    When I try to send a message
    Then I receive an error of type "AuthenticationError"
    And the error message contains "authentication" or "api_key"
