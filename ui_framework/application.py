from playwright.sync_api import Page
from ui_framework.pages.auth_page import AuthPage
from ui_framework.pages.dashboard_page import DashboardPage


class Application:
    def __init__(self, page):
        self.page = page
        self.auth_page = AuthPage(self.page)
        self.dashboard_page = DashboardPage(self.page)