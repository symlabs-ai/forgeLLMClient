@sdk @tools @ci-fast
Feature: Unified Tool Calling
  In order to use tools with any LLM
  As a Python developer
  I want to register tools and receive calls in a standardized format

  Background:
    Given the ForgeLLMClient is installed
    And the client is configured with provider "mock-tools"

  # ========== SUCCESS SCENARIOS ==========

  Scenario: Register tools for the LLM
    When I register the tool "calculator" with description "Performs mathematical calculations"
    And I register the tool "weather" with description "Gets weather forecast"
    Then the client has 2 tools registered
    And the tool "calculator" is available
    And the tool "weather" is available

  Scenario: Receive tool call request
    Given the tool "calculator" is registered
    When I send the message "What is 2 + 2?"
    Then I receive a response with tool_call
    And the tool_call has name "calculator"
    And the tool_call has arguments in JSON format
    And the tool_call has a unique id

  Scenario: Send tool call result
    Given the tool "calculator" is registered
    And I received a tool_call with id "tc_123" for "calculator"
    When I send the result "4" for tool_call "tc_123"
    Then I receive a final response from the LLM
    And the response incorporates the tool result

  Scenario: Multiple tool calls in one response
    Given the tools "calculator" and "weather" are registered
    When I send the message "What is 10 + 5 and what is the weather in SP?"
    Then I receive a response with multiple tool_calls
    And there is a tool_call for "calculator"
    And there is a tool_call for "weather"

  # ========== ERROR SCENARIOS ==========

  @error
  Scenario: Error registering tool without name
    When I try to register a tool without name
    Then I receive an error of type "ValidationError"
    And the error message contains "nome da tool"

  @error
  Scenario: Error sending result for nonexistent tool_call
    When I try to send result for tool_call "tc_nonexistent"
    Then I receive an error of type "ToolCallNotFoundError"
    And the error message contains "tool_call not found"
