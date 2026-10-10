"""U1. Урок 1 — первые тесты на Playwright.

Теория: practice/u1_01_first_tests.md
Стенд: docker compose up -d --build  →  http://localhost:8080/app/
Запуск:
    uv run pytest tests/ui/test_u1_01_first_tests.py --base-url http://localhost:8080 --headed

Задача 1. Страница входа открывается.
    Открой /app/. Проверь: заголовок вкладки "Mini Exchange", поля Email и Пароль видны,
    кнопка "Войти" видна. Локаторы — get_by_label и get_by_role.

Задача 2. Регистрация нового пользователя.
    Уникальный email (подсказка: uuid4), пароль от 8 символов.
    Заполни поля, нажми "Зарегистрироваться".
    Проверь: кабинет (test-id "dashboard") виден, в шапке (test-id "user-email") твой email,
    тост (test-id "toast") с текстом "Аккаунт создан".

Задача 3. Вход с неверным паролем.
    Зарегистрируй пользователя, выйди (кнопка "Выйти"), войди с неправильным паролем.
    Проверь: ошибка (test-id "auth-error") с текстом "Invalid email or password",
    кабинет не виден (to_be_hidden).

Задача 4. Пополнение баланса.
    Зарегистрируйся. В блоке "Пополнить" выбери актив BTC (select_option),
    введи сумму 0.5 (get_by_placeholder), нажми "Пополнить".
    Проверь: в таблице балансов строка BTC, в колонке "Доступно" — 0.5.
    Подсказка: строка — page.locator('[data-testid="balance-row"][data-asset="BTC"]'),
    ячейка внутри — .get_by_test_id("balance-available").

Задача 5 (со звёздочкой). Ордер на продажу.
    После пополнения BTC выбери пару BTC-USDT, сторону "Продать" (check),
    цена 100, количество 0.1, нажми "Разместить ордер".
    Проверь: в таблице "Мои ордера" одна строка (to_have_count), статус NEW.

Вопросы собеса (ответь устно или в секции «Ответы»):
    1. Какие локаторы выбираешь и почему не XPath? - im usually start from page_get_by_role becaouse its also tests accessabilty, the data test ids and so on
    2. Почему expect, а не assert? because its web first assertions and it has by default waiting 5se and frontend is asyncronius
    3. Чем отличаются фикстуры browser, context и page? browser - one instance on sesion, context its like browser in incognito mode has own cash/cookie/ page ist like tab for context
"""

# Решение пиши в tests/ui/test_u1_01_first_tests.py — файл и папки создаёшь сам.
