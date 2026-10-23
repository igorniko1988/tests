# Модуль 4. behave (BDD)

Два набора сценариев:
- `features/wallet.feature`   без браузера (быстрый, для понимания механики behave)
- `features/login_ui.feature` с браузером (Selenium + Page Object), тег `@ui`

## Установка (один раз)
    uv add behave selenium        # или: pip install behave selenium

## Команды
    behave                              все сценарии (кроме @exercise)
    behave features/wallet.feature      один файл
    behave --tags=@smoke                только с тегом smoke
    behave --tags=-@ui --tags=-@exercise   всё, кроме тестов с браузером
    behave --tags=@exercise             ваше задание (шаги надо дописать)
    behave -D headed=1                  показать окно браузера
    behave -D browser=firefox           другой браузер
    behave -f progress                  краткий вывод (точки)
    behave --dry-run                    проверить, что все шаги найдены, не выполняя их

## Как это работает
    .feature (текст)  ──behave читает строки──►  steps/*.py (код)
    Given/When/Then   ◄── совпадение по фразе ──  @given/@when/@then("фраза")

## Структура
    features/
      wallet.feature, login_ui.feature, exercise_refund.feature   сценарии
      steps/                                                      код шагов
      environment.py                                              хуки (запуск и закрытие)
    app/wallet.py        тестируемый код (кошелёк)
    pages/               Page Object для UI-сценариев
    site/                локальные HTML-страницы
    screenshots/         сюда сохраняются скриншоты упавших UI-шагов
    solutions/           эталон задания, не открывать до решения

## Ваше задание
Файл `features/exercise_refund.feature` (тег `@exercise`):
1. Запустите `behave --tags=@exercise`: увидите `undefined` и заготовки шагов.
2. Допишите шаг `When I refund {amount:d}` в `features/steps/wallet_steps.py`.
3. Добавьте метод `refund(amount)` в `app/wallet.py` (возвращает деньги на баланс).
4. Добейтесь, чтобы все сценарии стали зелёными.
