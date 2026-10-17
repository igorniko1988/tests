"""U1. Урок 4 — BrowserContext, ожидания и pytest для UI.

Теория: practice/u1_04_context_pytest.md
Запуск:
    uv run pytest tests/ui/test_u1_04_context_pytest.py -v

Задача 1. Настройка проекта (pyproject.toml и tests/ui/conftest.py).
    а) В pyproject.toml в [tool.pytest.ini_options] добавь base_url = "http://localhost:8080".
       Проверь, что тесты U1.2 запускаются без --base-url.
    б) В conftest.py переопредели browser_context_args: locale "ru-RU",
       viewport 1440x900. Не потеряй настройки плагина.
    в) Зарегистрируй маркер smoke в pyproject.toml.

Задача 2. Фикстуры в conftest.py.
    - user_email — уникальный email (uuid4).
    - logged_in_page — берёт page и user_email, регистрирует пользователя, ждёт кабинет,
      возвращает page.
    - create_user — фабрика: каждый вызов создаёт НОВЫЙ context (через фикстуру new_context),
      регистрирует в нём нового пользователя и возвращает page.
    - deposit-хелпер оставь обычной функцией (как в U1.2) — где его держать, реши сам.

Задача 3. Изоляция context.
    test_logged_in: через logged_in_page проверь, что в localStorage есть токен:
        page.evaluate("localStorage.getItem('token')") не None.
    test_fresh_context: с обычной page открой /app/ — видна форма входа, токена нет.
    Запусти оба теста вместе — объясни в «Ответах»,
    почему второй не видит логина первого.

Задача 4. Две вкладки одного context.
    Через logged_in_page открой вторую вкладку в ТОМ ЖЕ context (page.context.new_page()),
    перейди на /app/ — проверь, что там тоже кабинет и тот же email.
    Нажми «Выйти» во второй вкладке, перезагрузи первую (reload) — что увидишь и почему?

Задача 5. Два пользователя: продавец и покупатель.
    create_user() дважды. Продавец пополняет ETH 1 и выставляет SELL ETH-USDT цена 100 кол-во 1.
    Покупатель пополняет USDT 1000 и выставляет BUY ETH-USDT цена 100 кол-во 1.
    Проверь у обоих: ордер исполнился (статус FILLED). Сопоставление идёт в фоне, таблица
    обновляется раз в 2 с — подумай про timeout у expect.
    Затем проверь балансы: у продавца USDT 100 доступно, у покупателя ETH 1 и USDT 900.
    Если что-то не совпало — сначала убедись, что тест прав, потом разбирайся со стендом.

Задача 6. storage_state.
    Создай пользователя через create_user, сохрани state: page.context.storage_state().
    Новый context с этим state (new_context(storage_state=...)) → /app/ сразу кабинет без логина.
    Выйди в новом context. Первый context после reload — всё ещё залогинен? Почему?

Задача 7. parametrize: неверные суммы пополнения.
    Через logged_in_page пополни USDT суммами: "0", "-5", "abc", "" — один тест, четыре набора,
    читаемые ids. Проверь: тост НЕ «Баланс USDT пополнен» (to_have_text с not_ или регулярка),
    доступный USDT остался 0.

Задача 8. Маркеры.
    Пометь задачи 3 и 5 как smoke. Запусти: uv run pytest -m smoke -v (должно быть 3 теста).
    Убедись, что опечатка @pytest.mark.smok даёт ошибку, и объясни почему.

Вопросы собеса (ответы — в разделе «Собес» теории; ответь своими словами в «Ответах»):
    1. Что такое BrowserContext и зачем новый context на каждый тест?
    2. Как в одном тесте сыграть за двух пользователей?
    3. Как не логиниться в каждом тесте?
    4. Что Playwright проверяет перед кликом?
    5. Как устроены фикстуры pytest? Что такое scope, yield, conftest?
    6. Как настроить pytest-playwright под проект?
    7. Зачем --strict-markers и что такое xfail?
"""

# Решение пиши в tests/ui/test_u1_04_context_pytest.py — файл и папки создаёшь сам.
