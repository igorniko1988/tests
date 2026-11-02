@calculator
Feature: Calculator

  Background:
    Given The calculator is on

  # Уровень 6: Scenario Outline + Examples, уровень 8: теги на Outline и на Examples
  @smoke
  Scenario Outline: Add <a> and <b>
    When I add <a> and <b>
    Then The result is <expected>

    @positive
    Examples: Positive numbers
      | a  | b  | expected |
      | 2  | 5  | 7        |
      | 0  | 0  | 0        |
      | 10 | -4 | 6        |

    @negative
    Examples: Negative numbers
      | a  | b  | expected |
      | -1 | -3 | -4       |

  # Уровень 4: несколько проверок через And и But
  Scenario: Subtract with several checks
    When I subtract 3 from 10
    Then The result is 7
    And The result is positive
    But The result is not 13

  # Уровень 6: несколько именованных таблиц Examples
  Scenario Outline: Subtract <b> from <a>
    When I subtract <b> from <a>
    Then The result is <expected>

    Examples: Positive result
      | a  | b | expected |
      | 10 | 3 | 7        |

    Examples: Negative result
      | a | b  | expected |
      | 3 | 10 | -7       |

  # Уровень 7: таблица в шаге (context.table), уровень 8: несколько тегов
  @slow @wip
  Scenario: Sum of a list of numbers
    When I sum the numbers
      | number |
      | 10     |
      | 20     |
      | -5     |
    Then The result is 25

  # Уровень 7: таблица с несколькими колонками
  Scenario: Several operations in a row
    When I run the operations
      | operation | a  | b |
      | add       | 2  | 3 |
      | subtract  | 10 | 4 |
    Then The results are 5 and 6

  # Уровень 7: многострочный текст в шаге (context.text)
  Scenario: Expression from a text block
    When I evaluate the expression
      """
      2 + 3 + 10
      """
    Then The result is 15
