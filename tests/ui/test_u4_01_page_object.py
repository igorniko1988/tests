"""U4. Урок 1 — Page Object.

Теория: practice/u4_01_page_object.md
Код страниц пишешь в ui_framework/pages/ (файлы-заготовки уже есть), тесты — здесь.
Запуск:
    uv run pytest tests/ui/test_u4_01_page_object.py -v

Правила:
    - в тестах НЕТ page.get_by_* / page.locator — только методы и локаторы из PO;
    - в PO нет бизнес-проверок (раздел 4 теории), разрешены wait_loaded и проверка ответа своего действия;
    - для проверок PO отдаёт Locator, тест делает expect;
    - tests/ui/helpers.py в этом уроке не используем — всё через PO.

Задача 1. BasePage (ui_framework/pages/base_page.py).
    Атрибут класса path, __init__(page) с локатором toast, метод open() -> self.

Задача 2. AuthPage (ui_framework/pages/auth_page.py).
    path = "/app/". Локаторы: root, email, password, login_button, register_button, error.
    Методы: wait_loaded() -> self; fill_credentials(email, password);
    register(email, password) -> DashboardPage; login(email, password) -> DashboardPage;
    login_expecting_error(email, password) -> AuthPage.
    Реши, как избежать циклического импорта с DashboardPage (раздел 5 теории).

Задача 3. DashboardPage (ui_framework/pages/dashboard_page.py).
    Локаторы: root, user_email, logout_button, order_rows. Методы:
        wait_loaded() -> self; logout() -> AuthPage;
        deposit(asset, amount) -> dict            — ждёт ответ POST /balances/deposit, падает не на 2xx;
        deposit_expecting_error(asset, amount)    — без проверки ответа, для негативных тестов;
        place_order(side, price, quantity, symbol="ETH-USDT") -> dict   — то же для POST /orders;
        balance_available(asset) -> Locator; balance_locked(asset) -> Locator;
        order_row(order_id) -> Locator; order_status(order_id) -> Locator; cancel_order(order_id).

Задача 4. Фикстуры (tests/ui/conftest.py).
    auth_page — AuthPage(page); dashboard — зарегистрированный пользователь, DashboardPage.

Задача 5. Тесты через PO.
    а) Регистрация → в шапке email; выход → видна форма входа.
    б) Вход: верные данные → кабинет; parametrize (неверный пароль, несуществующий email) →
       ошибка "Invalid email or password", кабинет скрыт.
    в) Пополнение USDT 1000 → доступно 1000, заблокировано 0.
    г) Неверные суммы пополнения ("0", "-5", "abc") через deposit_expecting_error:
       тост не «Баланс USDT пополнен», доступно 0. (Вспомни U2.1: дождись, что тост сменился.)
    д) Ордер BUY 100 x 1 → заблокировано 100, доступно 900; отмена → CANCELED, 1000 и 0.
       id ордера — из ответа place_order.

Задача 6. Ревью practice/u4_01_review_me.py — минимум 10 проблем, ответы в том файле.

Задача 7. Устойчивость к изменениям.
    Представь: кнопку «Пополнить» переименовали в «Зачислить».
    а) Сколько мест надо поправить в твоём коде? А в тестах U1.4 до PO?
    б) Временно поменяй локатор кнопки в DashboardPage на name="Зачислить", запусти тесты:
       как выглядит падение и по нему понятно, где чинить? Верни обратно.
    Ответ — в «Ответах».

Вопросы собеса (ответы — в разделе «Собес» теории; ответь своими словами в «Ответах»):
    1. Что такое Page Object и зачем он нужен?
    2. Где граница между Page Object и тестом? Можно ли проверки внутри PO?
    3. Что возвращают методы PO?
    4. Где хранить локаторы? Почему их можно создавать в __init__?
    5. Как не превратить Page Object в свалку?
    6. PO или хелперы-функции?
    7. Как PO в Playwright отличается от PO в Selenium?
"""

import pytest
from playwright.sync_api import expect

# Задача 5а


# Задача 5б


# Задача 5в


# Задача 5г


# Задача 5д


# Ответы
"""
Задача 7:

Собес:
"""
