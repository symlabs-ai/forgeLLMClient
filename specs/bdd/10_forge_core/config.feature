@sdk @config @ci-fast
Feature: Provider configuration
  In order to use different LLM providers
  As a Python developer
  I want to configure the client with the desired provider

  Background:
    Given the ForgeLLMClient is installed

  # ========== SUCCESS SCENARIOS ==========

  Scenario: Configure valid provider
    When I configure the client with provider "mock"
    Then the client is ready for use
    And the active provider is "mock"

  Scenario: Configure provider with API key
    When I configure the client with provider "openai" and api_key "sk-test-123"
    Then the client is ready for use
    And the active provider is "openai"

  Scenario: Configure provider with specific model
    When I configure the client with provider "openai" and model "gpt-4"
    Then the client is ready for use
    And the active model is "gpt-4"

  Scenario: Reconfigure provider at runtime
    Given the client is configured with provider "mock"
    When I reconfigure the client to provider "openai"
    Then the active provider is "openai"

  # ========== ERROR SCENARIOS ==========

  @error
  Scenario: Error configuring invalid provider
    When I try to configure the client with provider "nonexistent-provider"
    Then I receive an error of type "ProviderNotFoundError"
    And the error message contains "nao encontrado"

  @error
  Scenario: Error configuring without API key when required
    When I try to configure the client with provider "openai" without api_key
    Then I receive an error of type "ConfigurationError"
    And the error message contains "api_key"
