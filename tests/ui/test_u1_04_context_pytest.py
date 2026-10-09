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

import random

import pytest
from playwright.sync_api import Page, expect

from tests.ui.helpers import amount, balance_row, deposit, place_order

# Сопоставление раз в 1 с + опрос таблицы раз в 2 с: 5 с по умолчанию впритык, берём с запасом
MATCHING_TIMEOUT = 15_000


# Задача 3
@pytest.mark.smoke
def test_logged_in(logged_in_page: Page):
    token = logged_in_page.evaluate("localStorage.getItem('token')")
    assert token is not None


@pytest.mark.smoke
def test_fresh_context(page: Page):
    page.goto("/app/")

    expect(page.get_by_test_id("auth-page")).to_be_visible()
    expect(page.get_by_test_id("dashboard")).to_be_hidden()
    assert page.evaluate("localStorage.getItem('token')") is None


# Задача 4
def test_two_tabs_share_context(logged_in_page: Page, user_email: str):
    first = logged_in_page
    second = first.context.new_page()
    second.goto("/app/")

    expect(second.get_by_test_id("dashboard")).to_be_visible()
    expect(second.get_by_test_id("user-email")).to_have_text(user_email)

    second.get_by_role("button", name="Выйти").click()
    expect(second.get_by_test_id("auth-page")).to_be_visible()

    first.reload()
    expect(first.get_by_test_id("auth-page")).to_be_visible()
    expect(first.get_by_test_id("dashboard")).to_be_hidden()


# Задача 5
@pytest.mark.smoke
def test_seller_and_buyer_trade(create_user):
    # Стакан общий для всех пользователей, а в нём висят ордера других тестов
    # (BUY 100 и 101, SELL 500 из U1.2). По цене 100 наш SELL исполнится об чужой
    # BUY 101 и покупатель останется без пары. Берём цену между чужими BUY и SELL.
    price = random.randint(300, 499)
    seller = create_user()
    buyer = create_user()

    deposit(seller, "ETH", "1")
    place_order(seller, "SELL", str(price), "1")
    deposit(buyer, "USDT", "1000")
    place_order(buyer, "BUY", str(price), "1")

    for user in (seller, buyer):
        expect(user.get_by_test_id("order-status")).to_have_text(
            "FILLED", timeout=MATCHING_TIMEOUT
        )

    expect(balance_row(seller, "USDT").get_by_test_id("balance-available")).to_have_text(
        amount(str(price))
    )
    expect(balance_row(buyer, "ETH").get_by_test_id("balance-available")).to_have_text(
        amount("1")
    )
    expect(balance_row(buyer, "USDT").get_by_test_id("balance-available")).to_have_text(
        amount(str(1000 - price))
    )


# Задача 6
def test_storage_state(create_user, new_context):
    first = create_user()
    state = first.context.storage_state()

    second = new_context(storage_state=state).new_page()
    second.goto("/app/")
    expect(second.get_by_test_id("dashboard")).to_be_visible()

    second.get_by_role("button", name="Выйти").click()
    expect(second.get_by_test_id("auth-page")).to_be_visible()

    first.reload()
    expect(first.get_by_test_id("dashboard")).to_be_visible()


# Задача 7
@pytest.mark.parametrize(
    "value",
    ["0", "-5", "abc", ""],
    ids=["zero", "negative", "not a number", "empty"],
)
def test_deposit_rejects_invalid_amount(logged_in_page: Page, value: str):
    page = logged_in_page
    toast = page.get_by_test_id("toast")
    expect(toast).to_have_text("Аккаунт создан")  # дождались тоста регистрации

    form = page.locator("#deposit-form")
    form.get_by_label("Актив").select_option("USDT")
    form.get_by_placeholder("Сумма").fill(value)
    form.get_by_role("button", name="Пополнить").click()

    # Сначала ждём, что тост сменился, иначе not_ пройдёт мгновенно — ещё до ответа сервера
    expect(toast).not_to_have_text("Аккаунт создан")
    expect(toast).not_to_have_text("Баланс USDT пополнен")
    expect(balance_row(page, "USDT").get_by_test_id("balance-available")).to_have_text(
        amount("0")
    )


# Ответы
"""
Задача 3:
    Каждый тест получает свой context, а это отдельный профиль, как окно инкогнито.
    Токен лежит в localStorage, а localStorage у каждого context свой. Context первого
    теста закрылся вместе с его хранилищем, второй тест стартовал с пустым.
    Поэтому тесты не зависят друг от друга и от порядка запуска.

Задача 4:
    После reload первая вкладка показывает форму входа. Вкладки одного context делят
    localStorage. «Выйти» во второй вкладке удалил token из общего хранилища, а первая
    вкладка при перезагрузке прочитала уже пустой localStorage. Без reload первая вкладка
    ещё показывала бы кабинет: токен лежит в переменной JS-страницы, пока она не
    перезагрузится.

Задача 6:
    Да, первый context после reload всё ещё залогинен. storage_state — это копия
    хранилища, а не ссылка на него: новый context получил свой экземпляр localStorage.
    Выход удаляет токен только в своём context. Сервер о выходе тоже не знает: logout
    на стенде только чистит localStorage, а JWT stateless и продолжает действовать до истечения.

Задача 8:
    В addopts стоит --strict-markers. Метки smok нет в списке markers, и pytest падает
    ещё на сборке тестов. Без этого флага было бы только предупреждение, а
    `-m smoke` молча не нашёл бы тест с опечаткой: он выпал бы из smoke-прогона,
    и никто бы этого не заметил.


# Вопросы собеса (ответы — в разделе «Собес» теории; ответь своими словами в «Ответах»):
#     1. Что такое BrowserContext и зачем новый context на каждый тест?
#     2. Как в одном тесте сыграть за двух пользователей?
#     3. Как не логиниться в каждом тесте?
#     4. Что Playwright проверяет перед кликом?
#     5. Как устроены фикстуры pytest? Что такое scope, yield, conftest?
#     6. Как настроить pytest-playwright под проект?
#     7. Зачем --strict-markers и что такое xfail?

Собес:
    1. BrowserContext — изолированный профиль внутри браузера, как окно инкогнито:
       свои cookies, localStorage, кэш, разрешения и настройки (viewport, locale).
       Context создаётся за миллисекунды в уже запущенном браузере, а запуск браузера
       занимает секунды. Новый context на тест даёт изоляцию: тесты не делят логин и
       состояние, не зависят от порядка и могут идти параллельно.
    2. Через два context: у каждого своё хранилище, поэтому каждый залогинен под своим
       пользователем. Две вкладки одного context не подходят, у них общий localStorage.
       В pytest-playwright — фикстура new_context, у меня это фабрика create_user.
    3. Залогиниться один раз (лучше через API) и сохранить storage_state, то есть cookies
       и localStorage. Новые context создавать с этим state, они сразу залогинены.
       Минусы: токен истекает, тесты одного пользователя делят его данные, а тесты
       логина и логаута надо запускать без state.
    4. Actionability: элемент есть в DOM, видим, стабилен (не анимируется), принимает
       события (его не перекрывает оверлей) и enabled; для fill — ещё editable.
       Playwright ждёт, пока все проверки пройдут, до таймаута действия (30 с).
       force=True пропускает проверки, но обычно маскирует реальную проблему.
    5. Фикстура — функция с @pytest.fixture, её результат pytest передаёт в тест по имени
       аргумента. Код до yield — setup, после — teardown, он выполнится даже при падении
       теста. scope (function, class, module, session) задаёт, сколько живёт фикстура.
       Фикстура не может зависеть от фикстуры с более коротким scope, иначе ScopeMismatch.
       conftest.py — файл с общими фикстурами, pytest находит его сам; фикстуры видны
       в его папке и ниже, вложенный conftest может переопределить фикстуру.
    6. В conftest переопределить session-фикстуры browser_context_args и
       browser_type_launch_args, дополняя словарь плагина через **, а не затирая его.
       Для одного теста — маркер browser_context_args. base_url — в pyproject,
       окружение переключаю через --base-url. Ещё опции --browser, --device,
       --tracing/--screenshot/--video.
    7. --strict-markers требует регистрировать метки, и опечатка становится ошибкой,
       а не молча пропущенным фильтром. xfail — тест на известный баг: прогон зелёный,
       в отчёте XFAIL со ссылкой на баг. Когда баг починят, будет XPASS — пора снять метку.
       С strict=True XPASS считается падением.
"""
