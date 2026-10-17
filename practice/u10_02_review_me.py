"""U10.2, задача 1 — финальное ревью: тесты «коллеги» на Playwright.

Найди минимум 20 проблем по всему курсу. Для каждой: строка, что не так, чем грозит, как исправить,
уровень (блокер / важно / мелочь). Ответы — внизу файла.
Это только чтение: файл в practice/ и не собирается pytest'ом.
"""

import random
import time

import pytest
from playwright.sync_api import Page, expect

URL = "http://localhost:8080/app/"
EMAIL = "qa@test.com"
PASSWORD = "Secret123!"


class Dashboard:
    def __init__(self, page):
        self.page = page
        self.last_order = None

    def login(self):
        self.page.goto(URL)
        self.page.locator("//input[@type='email']").fill(EMAIL)
        self.page.locator("//input[@type='password']").fill(PASSWORD)
        self.page.locator("text=Войти").click()
        self.page.wait_for_load_state("networkidle")

    def deposit(self, amount):
        self.page.locator("#deposit-form input").nth(0).fill(str(amount))
        self.page.locator("#deposit-form button").click(force=True)
        expect(self.page.get_by_test_id("toast")).to_contain_text("пополнен")

    def buy(self, price, qty):
        self.page.fill('[data-testid="order-price"]', str(price))
        self.page.fill('[data-testid="order-quantity"]', str(qty))
        self.page.click('[data-testid="place-order-button"]')
        self.last_order = price
        time.sleep(2)

    def balance(self):
        return float(self.page.locator('[data-asset="USDT"] [data-testid="balance-available"]').inner_text())


@pytest.fixture(scope="session")
def dash(browser):
    page = browser.new_page()
    d = Dashboard(page)
    d.login()
    return d


def test_1_deposit(dash):
    dash.deposit(1000)
    assert dash.balance() == 1000


def test_2_buy(dash):
    dash.buy(100.1, 1)
    assert dash.balance() == 899.9


def test_3_cancel(dash):
    dash.page.get_by_text("Отменить").first.click()
    rows = dash.page.get_by_test_id("order-row").all()
    assert "CANCELED" in rows[0].inner_text()
    assert dash.balance() == 1000


@pytest.mark.parametrize("amount", [random.randint(1, 100) for _ in range(3)])
def test_4_deposit_many(dash, amount):
    try:
        dash.deposit(amount)
    except Exception:
        pass
    assert dash.page.get_by_test_id("order-row").count() >= 0


def test_5_matching(dash, browser):
    seller = browser.new_page()
    seller.goto(URL)
    seller.pause()
    dash.buy(100, 1)
    time.sleep(10)
    assert "FILLED" in dash.page.content()


# Ответы
"""
"""
