import allure
from playwright.sync_api import Page
from ui_framework.components.common import Toast


class BasePage:
    path = '/'

    def __init__(self, page: Page):
        self.page = page
        self.toast = Toast(page)

    @allure.step('Открыть страницу')
    def open(self):
        self.page.goto(self.path)
        return self
