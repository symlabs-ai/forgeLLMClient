Feature: Error Handling and Retry
  As a developer using ForgeLLMClient
  I want proper error handling and automatic retries
  So that my application is resilient to transient failures

  Background:
    Given a retry configuration with max_retries 2 and base_delay 0.01

  Scenario: Successful request without retry
    Given a mock provider that succeeds immediately
    When I make a chat request with retry enabled
    Then the request should succeed
    And the provider should be called 1 time

  Scenario: Retry on rate limit error
    Given a mock provider that fails with rate limit 2 times then succeeds
    When I make a chat request with retry enabled
    Then the request should succeed
    And the provider should be called 3 times

  Scenario: Retry on timeout error
    Given a mock provider that fails with timeout 1 time then succeeds
    When I make a chat request with retry enabled
    Then the request should succeed
    And the provider should be called 2 times

  Scenario: No retry on authentication error
    Given a mock provider that fails with authentication error
    When I make a chat request with retry enabled
    Then the request should fail with AuthenticationError
    And the provider should be called 1 time

  Scenario: Exhaust all retries
    Given a mock provider that always fails with rate limit
    When I make a chat request with retry enabled
    Then the request should fail with RetryExhaustedError
    And the provider should be called 3 times
    And the error should contain the original rate limit error

  Scenario: Respect retry-after header
    Given a mock provider that fails with rate limit and retry_after 1 second
    When I make a chat request with retry enabled
    Then the retry should wait at least 1 second
