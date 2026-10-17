"""U5.4, задача 1 — ревью conftest от «коллеги».

⚠️ НЕ ЗАПУСКАТЬ и не копировать в tests/: уборка в конце удаляет ВСЕХ пользователей стенда
с адресом на test.com (это одна из ошибок, которые надо найти). Только читать.

Это фикстуры подготовки данных для UI-тестов биржи. Работает «у него на машине».
Найди минимум 12 проблем: строка, что не так, чем грозит, как исправить.
Чек-лист — раздел 4 теории (practice/u5_04_interview.md). Ответы — внизу файла.
"""

import time

import pytest
from faker import Faker
from playwright.sync_api import Page

API = "http://localhost:8080"
DB = "postgresql://exchange:exchange@localhost:5432/exchange"
SEED_EMAIL = "seed@test.com"
PASSWORD = "Qwerty123!"


@pytest.fixture(scope="session")
def seed_user(page: Page):
    page.goto(f"{API}/app/")
    page.get_by_label("Email").fill(SEED_EMAIL)
    page.get_by_label("Пароль").fill(PASSWORD)
    page.get_by_role("button", name="Зарегистрироваться").click()
    time.sleep(3)
    return SEED_EMAIL


@pytest.fixture(scope="session")
def token(playwright):
    api = playwright.request.new_context(base_url=API)
    r = api.post("/auth/login", data={"email": SEED_EMAIL, "password": PASSWORD})
    print("logged in with", PASSWORD, r.json())
    return r.json()["access_token"]


@pytest.fixture
def rich_user(playwright, token):
    api = playwright.request.new_context(base_url=API)
    api.post(
        "/balances/deposit",
        data={"asset": "USDT", "amount": "1000"},
        headers={"Authorization": f"Bearer {token}"},
    )
    return SEED_EMAIL


@pytest.fixture
def new_user(playwright, faker: Faker):
    api = playwright.request.new_context(base_url=API)
    email = faker.email()
    api.post("/auth/register", data={"email": email, "password": PASSWORD})
    return email


@pytest.fixture
def order(playwright, token):
    api = playwright.request.new_context(base_url=API)
    headers = {"Authorization": f"Bearer {token}"}
    for _ in range(3):
        r = api.post(
            "/orders",
            data={"symbol": "ETH-USDT", "side": "BUY", "price": "100", "quantity": "1"},
            headers=headers,
        )
        if r.status == 201:
            break
    yield r.json()
    api.delete(f"/orders/{r.json()['id']}", headers=headers)


@pytest.fixture
def browser_as_seed(context, token):
    context.add_init_script(f"localStorage.setItem('token', '{token}')")
    page = context.new_page()
    page.goto(f"{API}/app/")
    return page


@pytest.fixture(scope="session", autouse=True)
def cleanup():
    yield
    import psycopg

    with psycopg.connect(DB) as conn:
        prefix = "%test.com"
        conn.execute(f"DELETE FROM orders WHERE user_id IN (SELECT id FROM users WHERE email LIKE '{prefix}')")
        conn.execute(f"DELETE FROM users WHERE email LIKE '{prefix}'")


# Ответы
"""
"""
