import pytest
from playwright.sync_api import expect, Playwright
from ui_framework.config.settings import Settings
from ui_framework.data.generators import unique_email, unique_password
from ui_framework.api.client import ExchangeApi


@pytest.fixture(scope="session")
def api_context(playwright: Playwright, base_url):
    api = playwright.request.new_context(base_url=base_url)
    yield api
    api.dispose()

@pytest.fixture()
def create_api(api_context, new_context):
    def _create():
        email, password = unique_email(), unique_password()
        exchange_api = ExchangeApi(api_context)
        exchange_api.register(email=email, password=password)
        exchange_api.login(email=email, password=password)
        return exchange_api, email
    return _create




def pytest_configure(config: pytest.Config) -> None:
    expect.set_options(timeout=Settings().expect_timeout_ms)

def pytest_report_header(config: pytest.Config) -> str:
    settings = Settings()
    return f'env {settings.env}, base_url {settings.base_url}'

@pytest.fixture(scope="session")
def settings() -> Settings:
    return Settings()


@pytest.fixture(scope="session")
def base_url(settings) -> str:
    return settings.base_url
