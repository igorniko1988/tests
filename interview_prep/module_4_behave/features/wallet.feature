Feature: Wallet payments

  Background:
    Given a wallet with balance 100

  @smoke
  Scenario: Spend money when balance is enough
    When I spend 30
    Then the payment is accepted
    And the balance is 70

  Scenario: Not enough money
    When I spend 500
    Then the payment is declined
    And the balance is 100

  Scenario: Add money
    When I add 50
    Then the balance is 150

  Scenario: Several payments in a row
    When I make the following payments:
      | amount |
      | 10     |
      | 20     |
    Then the balance is 70

  Scenario Outline: Payments with different amounts
    When I spend <amount>
    Then the payment is <result>
    And the balance is <balance>

    Examples:
      | amount | result   | balance |
      | 1      | accepted | 99      |
      | 100    | accepted | 0       |
      | 101    | declined | 100     |
