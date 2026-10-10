"""U4. Урок 4 — утилиты, Allure и структура проекта.

Теория: practice/u4_04_utils_allure_structure.md
Код: ui_framework/utils/{money,waiting}.py, ui_framework/data/{models,generators}.py,
     ui_framework/fixtures/reporting.py (заготовки есть).
Запуск:
    uv run pytest tests/ui/test_u4_04_utils_allure.py -v --alluredir allure-results --clean-alluredir
    allure serve allure-results          # нужна Java: brew install openjdk (см. теорию, раздел 6)

Задача 1. Деньги (utils/money.py).
    to_decimal(value) и format_amount(value) — как сервер (exchange/schemas.py, _format_amount).
    Короткие проверки здесь же (обычные pytest-тесты без браузера, без фикстуры page):
        "100.50" → "100.5"; "1000.000" → "1000"; "0" → "0"; "0.00000001" → "0.00000001"; 1000 - 100.50 → "899.5".
    Подумай: почему Decimal(0.1) != Decimal("0.1")? Проверь и запиши в «Ответах».
    Заметь: если autouse-фикстура из U4.3 берёт page, эти тесты без браузера всё равно поднимут браузер
    (теория U4.3, раздел 5). Как это исправить: перенести тесты утилит в tests/unit/? сделать autouse
    умнее? Реши и объясни в «Ответах».

Задача 2. wait_until (utils/waiting.py) — по теории, раздел 4, с параметром ignore=(исключения,).
    Тесты без браузера: условие становится True на 3-й попытке — проходит;
    никогда не True — AssertionError с твоим сообщением; исключение из ignore — считается «ещё нет».

Задача 3. Данные (data/).
    generators.py: unique_email (перенеси из fixtures/data.py — фикстура user_email пусть использует его),
                   isolated_price(low, high) с комментарием, зачем.
    models.py: OrderData (frozen dataclass) с полем-свойством cost.
    Тест через UI: BUY OrderData(price="100.5", quantity="2") → заблокировано USDT == format_amount(order.cost),
    доступно == format_amount(1000 - order.cost). Пополнение 1000 — маркером balance из U4.3.

Задача 4. Allure-шаги.
    @allure.step с параметрами на публичных методах AuthPage, DashboardPage и компонентов-форм/строки.
    Пароль в шаг не должен попасть — проверь в отчёте.
    В тестах — with allure.step(...) для блоков проверок.

Задача 5. Скриншот и URL при падении (fixtures/reporting.py, подключи через pytest_plugins).
    Тест, который падает специально, под @pytest.mark.xfail(strict=True):
    в отчёте у него есть screenshot и url. Посмотри в allure serve.

Задача 6. Метки.
    На тесты задач 3 и 7: epic/feature/story/title/severity. Для xfail из задачи 5 — allure.issue("DEMO-1").
    В отчёте открой вкладку Behaviors: как сгруппировались тесты?

Задача 7. parametrize + allure.dynamic.
    Неверные суммы пополнения ("0", "-5", "abc") — один тест; allure.dynamic.title с суммой в названии.

Задача 8. environment.properties.
    pytest_sessionstart в reporting.py: env и base_url из Settings в allure-results.
    Проверь на главной отчёта для ENV=docker и ENV=stage.

Задача 9. Логирование.
    Логгер "ui" в DepositForm и OrderForm (INFO: что отправили, что ответил сервер — статус и id).
    Запусти один тест с --log-cli-level=INFO -s — что видно? Пароль/токен не должен печататься.

Задача 10. Структура (письменно в «Ответах»).
    Нарисуй дерево своего ui_framework/ и tests/ после U4.1–U4.4. Для каждой папки — одна строка «зачем».
    Найди хотя бы одну зависимость «не в ту сторону» (компонент импортирует страницу, utils знает про page…)
    и исправь, если есть.

Вопросы собеса (ответы — в разделе «Собес» теории; ответь своими словами в «Ответах»):
    1. Как устроен твой UI-фреймворк целиком?
    2. Что кладёшь в utils, а что нет?
    3. Как работаешь с деньгами в тестах?
    4. Как делаешь шаги и вложения в Allure?
    5. Как прикрепить скриншот к упавшему тесту?
    6. Зачем модели тестовых данных?
"""

# Решение пиши в tests/ui/test_u4_04_utils_allure.py — файл и папки создаёшь сам.
