# language: en
@api @orders
Feature: Orders
  As a trader
  I want to place and cancel limit orders
  So that my money is locked only while the order is open

  Background:
    Given a registered user
    And the user has deposited 100 USDT

  @smoke
  Scenario: Placing a BUY order locks its cost
    When the user places a BUY order for 2 ETH at 10 USDT
    Then the response status is 201
    And the order status is "NEW"
    And the USDT balance is 80 available and 20 locked

  Scenario: Cancelling an order returns the money
    Given the user has placed a BUY order for 1 ETH at 30 USDT
    When the user cancels the order
    Then the response status is 200
    And the order status is "CANCELED"
    And the USDT balance is 100 available and 0 locked

  Scenario Outline: Invalid orders are rejected
    When the user places an order with <field> set to "<value>"
    Then the response status is <status>
    And the error points to the field "<field>"

    Examples:
      | field    | value   | status |
      | symbol   | XXX-YYY | 422    |
      | side     | HOLD    | 422    |
      | price    | -1      | 422    |
      | quantity | 0       | 422    |

  Scenario: Not enough money
    When the user places a BUY order for 100 ETH at 10 USDT
    Then the response status is 400
