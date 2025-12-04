@openrouter @provider
Feature: OpenRouter Provider Integration
  As a developer
  I want to use OpenRouter as an LLM provider
  So that I can access 400+ models through a unified API

  Background:
    Given an OpenRouter provider with API key

  @chat @basic
  Scenario: Basic chat with OpenRouter
    When I send a message "Say 'hello' in one word"
    Then I should receive a response
    And the response should contain text
    And the provider name should be "openrouter"

  @chat @model-selection
  Scenario: Chat with specific model
    When I send a message "Say 'test'" with model "openai/gpt-4o-mini"
    Then I should receive a response
    And the response model should contain "gpt-4o-mini"

  @streaming
  Scenario: Streaming response from OpenRouter
    When I send a streaming message "Count from 1 to 3"
    Then I should receive streaming chunks
    And the final response should be complete

  @error @authentication
  Scenario: Invalid API key returns authentication error
    Given an OpenRouter provider with invalid API key "invalid-key"
    When I send a message "Hello"
    Then I should receive an authentication error

  @vision @image
  Scenario: Send message with image URL
    Given a message with text "What is in this image?" and image URL "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Cat03.jpg/1200px-Cat03.jpg"
    When I send the message with images
    Then I should receive a response describing the image

  @tools @function-calling
  Scenario: Tool calling with OpenRouter
    Given a tool definition for "get_weather" with parameter "location"
    When I send a message "What's the weather in Paris?" with tools
    Then I should receive a tool call for "get_weather"
    And the tool call should have argument "location"
