"""Фасад UI-слоя: все страницы через один объект — app.auth_page, app.dashboard_page."""

from playwright.sync_api import Page

from framework.ui.pages.auth_page import AuthPage
from framework.ui.pages.dashboard_page import DashboardPage


class Application:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.auth_page = AuthPage(page)
        self.dashboard_page = DashboardPage(page)
