"""U4. Урок 3 — фикстуры состояния и конфиг окружений.

Теория: practice/u4_03_fixtures_config.md
Код: ui_framework/config/settings.py, ui_framework/fixtures/{app,data}.py, tests/conftest.py (создать).
Запуск:
    uv run pytest tests/ui/test_u4_03_fixtures_config.py -v
    ENV=stage uv run pytest tests/ui/test_u4_03_fixtures_config.py -m smoke -v   # stage: up -d --build

Задача 1. Settings (ui_framework/config/settings.py).
    Поля: env, base_url, user_password (SecretStr), expect_timeout_ms, action_timeout_ms, matching_timeout_ms.
    Выбор окружения переменной ENV (local | docker | stage, по умолчанию docker),
    файлы envs/ui.<env>.env (в git) и envs/ui.<env>.local.env (не в git — проверь .gitignore).
    Создай envs/ui.local.env, envs/ui.docker.env, envs/ui.stage.env с адресами из таблицы теории;
    на stage таймауты больше.

Задача 2. Связать с pytest (tests/conftest.py — корневой, создать).
    - pytest_plugins с фикстурами из ui_framework/fixtures;
    - фикстуры settings (session) и base_url (session; --base-url из командной строки главнее);
    - pytest_configure: expect.set_options(timeout=...) из настроек;
    - pytest_report_header: env и base_url в шапке прогона;
    - убери base_url из pyproject.toml и проверь, что тесты U1.4 и U4.1 по-прежнему идут на :8080.

Задача 3. Фикстуры данных и приложения.
    data.py: unique_email() (функция) и фикстура user_email.
    app.py: app, logged_in_app (пароль — из settings), new_app (фабрика: новый context → залогиненный Application).
    Перенеси сюда app и logged_in_app из tests/ui/conftest.py (U4.1), чтобы не было
    двух источников. Фикстуры U1.4 (logged_in_page, create_user) оставь — на них опираются старые уроки.

Задача 4. autouse.
    Фикстура, выставляющая page.set_default_timeout(settings.action_timeout_ms) всем UI-тестам.
    Где ей место: tests/ui/conftest.py или ui_framework/fixtures? Объясни в «Ответах».

Задача 5. Маркер с данными.
    Зарегистрируй маркер balance. logged_in_app читает его и пополняет счёт:
        @pytest.mark.balance(USDT="1000", ETH="2")
    Тест: доступно USDT 1000 и ETH 2, BTC 0.

Задача 6. Уборка.
    order_factory: создаёт ордера через order_form, после теста отменяет те, что ещё открыты.
    Тест 1: создай 3 ордера, один отмени сам — уборка не должна упасть на уже отменённом.
    Тест 2: создай ордер и упади (assert False) под @pytest.mark.xfail(strict=True) — запусти с -s:
            покажи (print в teardown), что уборка выполнилась.

Задача 7. Параметризация.
    а) Параметризованная фикстура asset (USDT, BTC, ETH) с ids; тест пополнения на 1 — 3 прогона.
    б) funded_app через indirect=True: два набора — {"USDT": "1000"} и {"ETH": "5", "BTC": "1"};
       проверь доступные балансы из request.param (один тест, проверки в цикле по словарю).

Задача 8. Два пользователя через new_app.
    Продавец SELL ETH-USDT, покупатель BUY по той же цене (вспомни U1.4: цена вне чужих ордеров),
    оба ордера FILLED (таймаут — settings.matching_timeout_ms), балансы обоих после сделки.

Задача 9. Наборы.
    Пометь smoke тесты задач 5 и 8. Зарегистрируй regression; модуль целиком — pytestmark = regression.
    Запусти: uv run pytest tests/ui/test_u4_03_fixtures_config.py -m smoke и ENV=stage ... -m smoke.
    В «Ответах»: что показала шапка прогона, и сколько упало на stage (5% сбоев).

Вопросы собеса (ответы — в разделе «Собес» теории; ответь своими словами в «Ответах»):
    1. Какие scope у фикстур и что когда используешь?
    2. Как выполняется cleanup в фикстурах?
    3. Как запустить одни и те же UI-тесты на разных окружениях?
    4. Где хранишь секреты?
    5. Когда используешь autouse?
    6. Как передать фикстуре параметры из теста?
    7. Где лежат фикстуры в твоём фреймворке?
"""

# Решение пиши в tests/ui/test_u4_03_fixtures_config.py — файл и папки создаёшь сам.
