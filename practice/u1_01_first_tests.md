# U1. Урок 1 — первые тесты на Playwright

Задания: `tests/ui/test_u1_01_first_tests.py` (условия в docstring, код пишешь сам).

## Зачем

Playwright управляет настоящим браузером: открывает страницу, кликает, вводит текст и проверяет,
что видит пользователь. С pytest-playwright браузер не надо создавать руками — его дают фикстуры.

## 1. Фикстуры pytest-playwright

```python
def test_open(page):          # page — новая вкладка в новом context на каждый тест
    page.goto("/app/")        # путь дописывается к --base-url
```

- `browser` — один браузер на весь прогон (дорогой).
- `context` — «чистый профиль»: свои cookies и localStorage, новый на каждый тест (дешёвый).
- `page` — вкладка внутри context.

## 2. Запуск

```bash
docker compose up -d --build                        # стенд на :8080
uv run pytest tests/ui --base-url http://localhost:8080
uv run pytest tests/ui --base-url http://localhost:8080 --headed --slowmo 500   # видно браузер
```

`--headed` — показать окно, `--slowmo 500` — пауза 500 мс между действиями, `--browser firefox` — другой браузер.

## 3. Действия

```python
page.goto("/app/")
page.get_by_label("Email").fill("a@test.com")        # ввести текст (поле очищается)
page.get_by_role("button", name="Войти").click()
page.get_by_test_id("deposit-asset").select_option("BTC")   # выбрать в <select>
page.get_by_label("Продать").check()                 # radio / checkbox
```

## 4. Локаторы — как искать элемент

Приоритет (от лучшего):

1. `get_by_role("button", name="Войти")` — как видит пользователь и скринридер.
2. `get_by_label("Email")`, `get_by_placeholder("Сумма")`, `get_by_text("Ордеров пока нет")`.
3. `get_by_test_id("login-button")` — атрибут `data-testid`, стабилен, если разработчики его ставят.
4. CSS / XPath — в крайнем случае: ломаются при любой правке вёрстки.

Локатор ленивый: `page.get_by_label("Email")` ничего не ищет, пока не вызовешь действие или проверку.

## 5. Проверки expect

```python
from playwright.sync_api import expect

expect(page.get_by_test_id("dashboard")).to_be_visible()
expect(page.get_by_test_id("auth-error")).to_have_text("Invalid email or password")
expect(page.get_by_test_id("deposit-amount")).to_have_value("100")
expect(page.get_by_test_id("balance-row")).to_have_count(1)
expect(page).to_have_url("http://localhost:8080/app/")
expect(page).to_have_title("Mini Exchange")
```

`expect` сам ждёт до 5 секунд, пока условие станет верным. Обычный `assert` проверяет один раз —
для UI это источник флейков.

## Собес

- **Какие локаторы выбираешь?** Роли и label — как видит пользователь; test-id — когда ролей нет.
  XPath и длинный CSS — нет: привязаны к вёрстке и ломаются.
- **Почему expect, а не assert?** expect повторяет проверку до таймаута, assert — один раз.
- **Что дают фикстуры page / context / browser?** browser — один на прогон, context и page — новые
  на каждый тест, поэтому тесты изолированы (нет общих cookies и логина).
