Feature: QuantaSynapse Class Behavior
  As a developer, I want to ensure the QuantaSynapse class behaves as expected.

  Scenario: Connecting to Quanta projects
    Given a new QuantaSynapse instance
    When the connect method is called
    Then the output should be "Connecting to Quanta projects..."

  Scenario: Disconnecting from Quanta projects
    Given a new QuantaSynapse instance
    When the disconnect method is called
    Then the output should be "Disconnecting from Quanta projects..."
