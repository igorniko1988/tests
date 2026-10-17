import pytest
from ui_framework.application import Application
from playwright.sync_api import Page
from ui_framework.config.settings import Settings
from faker import Faker

@pytest.fixture(scope="session")
def settings() -> Settings:
    return Settings()


@pytest.fixture(scope="session")
def base_url(settings) -> str:
    return settings.base_url


@pytest.fixture
def app(page: Page):
    app = Application(page)
    yield app


@pytest.fixture
def logged_user(app, credentials):
    (app.auth_page.open().
                       fill_credentials(credentials['email'], credentials['password'])
                       .click_register())
    app.dashboard_page.wait_loaded()
    return app

@pytest.fixture
def credentials():
    faker = Faker()
    data = {
        'email': faker.email(),
        'password': faker.password()
    }
    return data
