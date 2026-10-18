import pytest
from playwright.sync_api import Page, expect
from ui_framework.config.settings import Settings

pytest_plugins = [
    "ui_framework.fixtures.app",
    "ui_framework.fixtures.data",
    "ui_framework.plugins.reporting",
]


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
