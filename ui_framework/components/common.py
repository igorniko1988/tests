import allure
from playwright.sync_api import Page, expect


class Toast:
    def __init__(self, page: Page):
        self.page = page
        self.message = page.get_by_test_id('toast')

    def wait_hidden(self):
        expect(self.message).to_be_hidden()


class Header:
    def __init__(self, page: Page):
        self.page = page
        self.email = page.get_by_test_id('user-email')
        self.logout_button = page.get_by_role('button', name='Выйти')

    @allure.step('Выйти из аккаунта')
    def logout(self):
        self.logout_button.click()
