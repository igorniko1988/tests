"""U1. Урок 5 — ревью чужого теста.

Задание как на собесе: «Вот тест коллеги, проведи ревью».
Найди все проблемы (их больше 12) — используй чек-лист из раздела 5 теории
practice/u1_05_interview.md. Для каждой запиши в «Ответы»: строка — что не так — почему — как правильно.

Потом перепиши тесты правильно в tests/ui/test_u1_05_livecoding.py (задача 4).

Файл лежит в practice/, а не в tests/, — чтобы pytest его не запускал.
"""

import time

from playwright.sync_api import Page, expect

EMAIL = "qa_user@test.com"
PASSWORD = "password123"


def test_1_register(page: Page):
    page.goto("http://localhost:8080/app/")
    page.locator("//input[@type='email']").fill(EMAIL)
    page.locator("//input[@type='password']").fill(PASSWORD)
    page.locator("//form[@id='auth-form']/div/button[2]").click()
    time.sleep(2)
    assert page.locator("#dashboard").is_visible()


def test_2_deposit(page: Page):
    page.goto("http://localhost:8080/app/")
    page.locator("//input[@type='email']").fill(EMAIL)
    page.locator("//input[@type='password']").fill(PASSWORD)
    page.locator("#auth-form button[type=submit]").click()
    time.sleep(2)
    page.locator("#deposit-form select").select_option("USDT")
    page.locator("#deposit-form input").fill("1000")
    page.locator("#deposit-form button").click(force=True)
    time.sleep(1)
    assert page.locator(".toast").text_content() != ""


def test_3_order(page: Page):
    page.goto("http://localhost:8080/app/")
    page.locator("//input[@type='email']").fill(EMAIL)
    page.locator("//input[@type='password']").fill(PASSWORD)
    page.locator("#auth-form button[type=submit]").click()
    time.sleep(2)
    page.locator("input[name=price]").fill("100")
    page.locator("input[name=quantity]").fill("1")
    page.locator("#order-form button").click()
    time.sleep(3)
    try:
        assert page.locator("table").nth(1).locator("tr").nth(1).locator("td").nth(5).inner_text() == "NEW"
    except AssertionError:
        print("статус не NEW, но это иногда бывает")


def test_4_cancel(page: Page):
    page.goto("http://localhost:8080/app/")
    page.locator("//input[@type='email']").fill(EMAIL)
    page.locator("//input[@type='password']").fill(PASSWORD)
    page.locator("#auth-form button[type=submit]").click()
    time.sleep(2)
    page.locator("button.danger").first.click()
    time.sleep(2)
    assert page.locator("table").nth(1).locator("tr").count() > 0


# Ответы
"""
строка — что не так — почему — как правильно

"""
