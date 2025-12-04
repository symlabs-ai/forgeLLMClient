@sdk @provider @openai
Feature: OpenAI Provider
  In order to use OpenAI models
  As a Python developer
  I want to integrate with the OpenAI API transparently

  Background:
    Given the ForgeLLMClient is installed
    And the environment variable OPENAI_API_KEY is configured

  # ========== CONFIGURATION SCENARIOS ==========

  @ci-fast
  Scenario: Configure OpenAI provider with API key
    When I configure the client with provider "openai"
    Then the client is ready for use
    And the active provider is "openai"

  @ci-fast
  Scenario: Configure OpenAI with specific model
    When I configure the client with provider "openai" and model "gpt-4"
    Then the active model is "gpt-4"

  @ci-fast
  Scenario: Configure OpenAI with GPT-3.5 model
    When I configure the client with provider "openai" and model "gpt-3.5-turbo"
    Then the active model is "gpt-3.5-turbo"

  # ========== CHAT SCENARIOS ==========

  @slow @integration
  Scenario: Send message to GPT-4
    Given the client is configured with provider "openai" and model "gpt-4"
    When I send the message "Say only: test"
    Then I receive a response with status "success"
    And the response contains text
    And provider.id in response is "openai"

  @slow @streaming @integration
  Scenario: Streaming with OpenAI
    Given the client is configured with provider "openai"
    When I send the message "Count from 1 to 3" with streaming enabled
    Then I receive chunks progressively
    And the final response is complete

  # ========== TOOL CALLING SCENARIOS ==========

  @slow @tools @integration
  Scenario: Tool calling with OpenAI
    Given the client is configured with provider "openai"
    And the tool "get_weather" is registered
    When I send the message "What is the weather in Sao Paulo?"
    Then I receive a response with tool_call
    And the tool_call has normalized format
    And the tool_call.name is "get_weather"

  # ========== ERROR SCENARIOS ==========

  @error @ci-fast
  Scenario: Error with invalid API key
    Given I configure the client with api_key "sk-invalid"
    When I try to send a message
    Then I receive an error of type "AuthenticationError"
    And the error message contains "authentication" or "api_key"
