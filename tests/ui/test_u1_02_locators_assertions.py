"""U1. Урок 2 — локаторы и проверки подробно.

Теория: practice/u1_02_locators_assertions.md
Запуск:
    uv run pytest tests/ui/test_u1_02_locators_assertions.py --base-url http://localhost:8080 --headed

Правила для всех задач:
    - только page.goto("/app/") (без полного адреса);
    - уникальный email через uuid4;
    - локаторы по приоритету: роль → label/placeholder/text → test-id → CSS. XPath нельзя;
    - никаких sleep, is_visible() и count() в проверках — только expect.

Задача 0. Хелперы.
    Напиши функции register(page) -> str (регистрирует нового пользователя и ждёт кабинет)
    и deposit(page, asset, amount) (пополняет и ждёт тост "Баланс <asset> пополнен").
    Используй их в задачах ниже.

Задача 1. Форма входа целиком.
    Открой /app/. Одной проверкой to_match_aria_snapshot проверь блок auth-page:
    заголовок "Вход" уровня 2, поля Email и Пароль, кнопки "Войти" и "Зарегистрироваться".
    Отдельно: у поля Пароль атрибут type="password", у поля Email — type="email".

Задача 2. Пустой список ордеров.
    Новый пользователь: виден текст "Ордеров пока нет", строк ордеров 0 (to_have_count).

Задача 3. Три ордера и фильтры локаторов.
    Пополни USDT 1000 и ETH 10. Размести три ордера на ETH-USDT:
        BUY  цена 100 кол-во 1
        BUY  цена 101 кол-во 1
        SELL цена 500 кол-во 2
    Сторону выбирай через get_by_label("Купить"/"Продать").check().
    Проверь:
        - строк ордеров 3;
        - строк с SELL ровно 1 (filter(has_text=...));
        - у всех статус NEW — ОДНОЙ проверкой списком (to_have_text([...]));
        - у строки SELL в колонке "Исполнено" 0 (get_by_test_id("order-filled") внутри строки).

Задача 4. Отмена конкретного ордера.
    Создай два BUY-ордера с ценами 100 и 200. Отмени тот, что с ценой 200:
    найди строку по цене (не через nth!), нажми "Отменить" внутри строки.
    Проверь:
        - у этой строки статус CANCELED, кнопки "Отменить" в ней больше нет (to_have_count(0));
        - у ордера с ценой 100 статус по-прежнему NEW и кнопка есть;
        - выбери фильтр "Статус" = CANCELED: в таблице одна строка, и в ней цена 200.

Задача 5. Ошибка валидации ордера.
    Нажми "Разместить ордер" с пустыми ценой и количеством.
    Проверь: ошибка (role="alert" внутри формы ордера) видна и содержит "price" и "quantity"
    (to_contain_text или регулярка). Тост не появился.

Задача 6. Блокировка средств.
    Пополни USDT 1000, размести BUY ETH-USDT цена 100 кол-во 2.
    Проверь в строке USDT таблицы балансов: "Доступно" 800, "Заблокировано" 200.
    Отмени ордер — снова 1000 и 0.
    Подсказка: числа могут прийти как "800" или "800.00" — подумай, какую проверку выбрать
    (to_have_text с регуляркой?). Если результат не совпадает с ожидаемым — это повод
    разобраться, а не подгонять тест.

Вопросы собеса (ответы — в разделе «Собес» теории; ответь своими словами в секции «Ответы»):
    1. Как работает get_by_role? Что такое accessible name? So how does it works browser build accesability tree in the dom tree and playwright looking for the element with role
    2. Как найти кнопку в нужной строке таблицы? find string in the table for example using has-text and than in founded element finds needed element
    3. Чем отличаются to_have_text и to_contain_text? Как проверить список? to have text checking the whole text, and containing only the part
    4. Почему не assert loc.is_visible() / assert loc.count() == 3? is visible works without timing , count with timeot may be
    5. Что делать, если у элементов нет ни ролей, ни test-id? asks for developers to add ids
    6. Чем отличаются to_be_hidden, not_to_be_visible, to_be_attached, to_have_count(0)? to be hidden - may be with disable state, no to be visible - disable state, to be attached may be only in the dom tree
    , count can be not visible may be but exists in the dom tree
    7. Как проверить структуру формы целиком? using aria snapshow in the yaml format, codegen suits very good with it
"""

import re
from uuid import uuid4

from playwright.sync_api import Page, expect


# Задача 0
def register_user(page: Page) -> str:
    email = f"user_{uuid4().hex[:8]}@test.com"

    page.goto("/app/")
    page.get_by_role("textbox", name="Email").fill(email)
    page.get_by_role("textbox", name="Пароль").fill("password123")
    page.get_by_role("button", name="Зарегистрироваться").click()

    expect(page.get_by_test_id("dashboard")).to_be_visible()
    expect(page.get_by_test_id("user-email")).to_have_text(email)
    return email


def deposit(page: Page, asset: str, amount: str) -> None:
    form = page.locator("#deposit-form")
    form.get_by_label("Актив").select_option(asset)
    form.get_by_placeholder("Сумма").fill(amount)
    form.get_by_role("button", name="Пополнить").click()
    expect(page.get_by_test_id("toast")).to_have_text(f"Баланс {asset} пополнен")


def place_order(page: Page, side: str, price: str, quantity: str, symbol: str = "ETH-USDT") -> None:
    # Тост "Ордер размещён" может висеть от прошлого ордера, поэтому ждём новую строку в таблице.
    rows = page.get_by_test_id("order-row")
    rows_before = rows.count()  # прошлый вызов уже дождался своей строки, значит число верное

    form = page.locator("#order-form")
    form.get_by_label("Пара").select_option(symbol)
    form.get_by_label(side).check()  # "Купить" / "Продать"
    form.get_by_label("Цена").fill(price)
    form.get_by_label("Количество").fill(quantity)
    form.get_by_role("button", name="Разместить ордер").click()
    expect(rows).to_have_count(rows_before + 1)


# Задача 1
def test_auth_form_structure(page: Page):
    page.goto("/app/")

    expect(page.get_by_test_id("auth-page")).to_match_aria_snapshot("""
      - heading "Вход" [level=2]
      - textbox "Email"
      - textbox "Пароль"
      - button "Войти"
      - button "Зарегистрироваться"
    """)
    expect(page.get_by_label("Email")).to_have_attribute("type", "email")
    expect(page.get_by_label("Пароль")).to_have_attribute("type", "password")


# Задача 2
def test_empty_orders(page: Page):
    register_user(page)

    expect(page.get_by_text("Ордеров пока нет")).to_be_visible()
    expect(page.get_by_test_id("order-row")).to_have_count(0)


# Задача 3
def test_three_orders(page: Page):
    register_user(page)
    deposit(page, "USDT", "1000")
    deposit(page, "ETH", "10")

    place_order(page, "Купить", "100", "1")
    place_order(page, "Купить", "101", "1")
    place_order(page, "Продать", "500", "2")

    rows = page.get_by_test_id("order-row")
    expect(rows).to_have_count(3)

    sell_rows = rows.filter(has_text="SELL")
    expect(sell_rows).to_have_count(1)

    expect(page.get_by_test_id("order-status")).to_have_text(["NEW", "NEW", "NEW"])
    expect(sell_rows.get_by_test_id("order-filled")).to_have_text(re.compile(r"^0(\.0+)?$"))


# Задача 4
def test_cancel_specific_order(page: Page):
    register_user(page)
    deposit(page, "USDT", "1000")
    place_order(page, "Купить", "100", "1")
    place_order(page, "Купить", "200", "1")

    rows = page.get_by_test_id("order-row")
    row_100 = rows.filter(has=page.get_by_role("cell", name="100", exact=True))
    row_200 = rows.filter(has=page.get_by_role("cell", name="200", exact=True))

    row_200.get_by_role("button", name="Отменить").click()

    expect(row_200.get_by_test_id("order-status")).to_have_text("CANCELED")
    expect(row_200.get_by_role("button", name="Отменить")).to_have_count(0)

    expect(row_100.get_by_test_id("order-status")).to_have_text("NEW")
    expect(row_100.get_by_role("button", name="Отменить")).to_be_visible()

    page.get_by_label("Статус").select_option("CANCELED")
    expect(rows).to_have_count(1)
    expect(rows.get_by_role("cell", name="200", exact=True)).to_be_visible()


# Задача 5
def test_order_validation_error(page: Page):
    register_user(page)

    form = page.locator("#order-form")
    form.get_by_role("button", name="Разместить ордер").click()

    error = form.get_by_role("alert")
    expect(error).to_be_visible()
    expect(error).to_contain_text("price")
    expect(error).to_contain_text("quantity")
    expect(page.get_by_test_id("toast")).to_be_hidden()


# Задача 6
def test_funds_locked_by_order(page: Page):
    register_user(page)
    deposit(page, "USDT", "1000")

    usdt = page.locator('[data-testid="balance-row"][data-asset="USDT"]')
    available = usdt.get_by_test_id("balance-available")
    locked = usdt.get_by_test_id("balance-locked")

    place_order(page, "Купить", "100", "2")
    expect(available).to_have_text(re.compile(r"^800(\.0+)?$"))
    expect(locked).to_have_text(re.compile(r"^200(\.0+)?$"))

    page.get_by_test_id("order-row").get_by_role("button", name="Отменить").click()
    expect(available).to_have_text(re.compile(r"^1000(\.0+)?$"))
    expect(locked).to_have_text(re.compile(r"^0(\.0+)?$"))
