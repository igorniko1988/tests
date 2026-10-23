@ui
Feature: Login through the browser

  Scenario: Successful login
    Given I am on the login page
    When I log in as "tomsmith" with password "SuperSecretPassword!"
    Then I see the message "You logged into a secure area!"

  @smoke
  Scenario Outline: Failed login
    Given I am on the login page
    When I log in as "<user>" with password "<password>"
    Then I see the message "Your username or password is invalid!"

    Examples:
      | user     | password |
      | tomsmith | wrong    |
      | nobody   | wrong    |
