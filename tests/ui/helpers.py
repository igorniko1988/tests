"""Хелперы UI-тестов: обычные функции, их вызывают и фикстуры, и тесты."""

import re

from playwright.sync_api import Locator, Page, expect

PASSWORD = "password123"


def amount(value: str) -> re.Pattern:
    """Число как на экране: "100" совпадёт и с "100", и с "100.00000000"."""
    return re.compile(rf"^{re.escape(value)}(\.0+)?$")


def register(page: Page, email: str, password: str = PASSWORD) -> Page:
    page.goto("/app/")
    page.get_by_label("Email").fill(email)
    page.get_by_label("Пароль").fill(password)
    page.get_by_role("button", name="Зарегистрироваться").click()

    expect(page.get_by_test_id("dashboard")).to_be_visible()
    expect(page.get_by_test_id("user-email")).to_have_text(email)
    return page


# Хелперы ждут ОТВЕТ сервера, а не тост: у двух пополнений (или ордеров) подряд тост
# одинаковый, проверка второго проходит по старому тосту, а пришедший позже ответ
# первого запроса делает form.reset() и стирает уже введённые значения (разбор — U2.2).


def deposit(page: Page, asset: str, value: str) -> dict:
    form = page.locator("#deposit-form")
    form.get_by_label("Актив").select_option(asset)
    form.get_by_placeholder("Сумма").fill(value)
    with page.expect_response(
        lambda r: r.url.endswith("/balances/deposit") and r.request.method == "POST"
    ) as info:
        form.get_by_role("button", name="Пополнить").click()
    assert info.value.ok, f"пополнение не прошло: {info.value.status} {info.value.text()}"
    expect(page.get_by_test_id("toast")).to_have_text(f"Баланс {asset} пополнен")
    return info.value.json()


def place_order(
    page: Page, side: str, price: str, quantity: str, symbol: str = "ETH-USDT"
) -> dict:
    form = page.locator("#order-form")
    form.get_by_label("Пара").select_option(symbol)
    form.get_by_label("Купить" if side == "BUY" else "Продать").check()
    form.get_by_label("Цена").fill(price)
    form.get_by_label("Количество").fill(quantity)
    with page.expect_response(
        lambda r: r.url.endswith("/orders") and r.request.method == "POST"
    ) as info:
        form.get_by_role("button", name="Разместить ордер").click()
    assert info.value.ok, f"ордер не создан: {info.value.status} {info.value.text()}"
    expect(page.get_by_test_id("toast")).to_have_text("Ордер размещён")
    return info.value.json()


def balance_row(page: Page, asset: str) -> Locator:
    return page.locator(f'[data-testid="balance-row"][data-asset="{asset}"]')


def slow_network(page: Page, latency_ms: int) -> None:
    """Добавить задержку к каждому запросу страницы — как медленный CI или мобильная сеть.

    Только Chromium: работает через CDP (Network.emulateNetworkConditions).
    """
    cdp = page.context.new_cdp_session(page)
    cdp.send("Network.enable")
    cdp.send(
        "Network.emulateNetworkConditions",
        {"offline": False, "latency": latency_ms, "downloadThroughput": -1, "uploadThroughput": -1},
    )
