"""Общие фикстуры UI-тестов (урок U1.4). Хелперы — в tests/ui/helpers.py."""

from uuid import uuid4

import pytest
from playwright.sync_api import Page

from tests.ui.helpers import register


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {"width": 1440, "height": 900},
        "locale": "ru-RU",
    }


@pytest.fixture
def user_email() -> str:
    return f"user_{uuid4().hex[:8]}@test.com"


@pytest.fixture
def logged_in_page(page: Page, user_email: str) -> Page:
    return register(page, user_email)


@pytest.fixture
def create_user(new_context):
    """Фабрика: каждый вызов — новый context (своё хранилище) и новый пользователь."""

    def _create() -> Page:
        page = new_context().new_page()
        return register(page, f"user_{uuid4().hex[:8]}@test.com")

    return _create
