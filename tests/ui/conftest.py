from pytest import fixture
from ui_framework.config.settings import Settings
from playwright.sync_api import Page


@fixture(autouse=True)
def set_actionability_timeout(page: Page, settings: Settings):
    page.set_default_timeout(settings.action_timeout_ms)