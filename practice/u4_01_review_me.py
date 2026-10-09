"""U4.1, задача 6 — ревью Page Object от «коллеги».

Код рабочий (почти), но на ревью его не пропустят. Найди минимум 10 проблем.
Для каждой: строка, что не так, как исправить. Ответы — внизу файла.
Подсказка: сверяйся с разделом 7 теории (антипаттерны) и с U2.1–U2.2.
"""

import time

from playwright.sync_api import Page, expect

EMAIL = "trader@test.com"
PASSWORD = "password123"


class ExchangePage:
    LOGIN_BUTTON = "[data-testid=login-button]"
    REGISTER_BUTTON = "text=Зарегистрироваться"
    DEPOSIT_BUTTON = "#deposit-form > button"

    def __init__(self, page: Page):
        self.page = page
        self.last_order_price = None

    def open(self):
        self.page.goto("http://localhost:8080/app/")
        self.page.wait_for_load_state("networkidle")

    def click_register_button(self):
        self.page.click(self.REGISTER_BUTTON)

    def login(self):
        self.page.fill("[data-testid=email-input]", EMAIL)
        self.page.fill("[data-testid=password-input]", PASSWORD)
        self.page.click(self.LOGIN_BUTTON)
        time.sleep(2)

    def deposit_and_check(self, asset, amount):
        self.page.select_option("[data-testid=deposit-asset]", asset)
        self.page.fill("[data-testid=deposit-amount]", amount)
        self.page.click(self.DEPOSIT_BUTTON)
        expect(self.page.locator(f"[data-asset={asset}] [data-testid=balance-available]")).to_have_text(amount)

    def get_balance(self, asset):
        return self.page.locator(f"[data-asset={asset}] [data-testid=balance-available]").text_content()

    def place_order(self, price, quantity):
        self.page.fill("[data-testid=order-price]", price)
        self.page.fill("[data-testid=order-quantity]", quantity)
        self.page.click("[data-testid=place-order-button]")
        self.last_order_price = price

    def cancel_last_order(self):
        self.page.locator("[data-testid=cancel-order]").first.click()

    def is_order_cancelled(self):
        return "CANCELED" in self.page.locator("[data-testid=order-status]").first.text_content()

    def logout(self):
        try:
            self.page.click("[data-testid=logout-button]", timeout=1000)
        except Exception:
            pass


def test_order_flow(page: Page):
    exchange = ExchangePage(page)
    exchange.open()
    exchange.login()
    exchange.deposit_and_check("USDT", "1000")
    exchange.place_order("100", "1")
    assert exchange.get_balance("USDT") == "900"
    exchange.cancel_last_order()
    assert exchange.is_order_cancelled()


# Ответы
"""
"""
