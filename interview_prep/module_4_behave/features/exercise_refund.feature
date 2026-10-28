@exercise
Feature: Refunds (ВАШЕ ЗАДАНИЕ)

  # Запуск: behave --tags=@exercise
  # Напишите недостающие шаги в features/steps/ (behave сам подскажет заготовки).
  # Добавьте в app/wallet.py метод refund(amount), если нужно.

  Scenario: Refund returns money to the wallet
    Given a wallet with balance 50
    When I refund 20
    Then the balance is 70

  Scenario Outline: Refund of different amounts
    Given a wallet with balance 10
    When I refund <amount>
    Then the balance is <balance>

    Examples:
      | amount | balance |
      | 5      | 15      |
      | 90     | 100     |
