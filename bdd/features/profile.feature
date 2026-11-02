@auth
Feature: Profile

  @smoke
  Scenario: A new user sees own profile
    Given a registered user
    When the user requests the profile
    Then the response status is 200

  Scenario: A new user sees own email in the profile
    Given a registered user
    When the user requests the profile
    Then the response status is 200
    And the profile email is the user's email

  Scenario: Profile without a token is rejected
    When an anonymous client requests the profile
    Then the response status is 401
