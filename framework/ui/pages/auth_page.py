import allure
from playwright.sync_api import Page, expect

from framework.ui.pages.base_page import BasePage


class AuthPage(BasePage):
    path = '/app/'

    def __init__(self, page: Page):
        super().__init__(page)
        self.email = self.page.get_by_label("Email")
        self.password = self.page.get_by_label("Пароль")
        self.login_button = self.page.get_by_role("button", name="Войти")
        self.register_button = self.page.get_by_role("button", name="Зарегистрироваться")
        self.auth_form = self.page.get_by_test_id("auth-page")
        self.error_message = self.page.get_by_test_id('auth-error')

    @allure.step('Дождаться страницы входа')
    def wait_loaded(self):
        expect(self.auth_form).to_be_visible()
        return self

    @allure.step('Ввести email {email}')
    def fill_credentials(self, email, password):
        self.email.fill(email)
        self.password.fill(password)
        return self

    @allure.step('Нажать «Войти»')
    def click_login(self):
        self.login_button.click()
        return self

    @allure.step('Нажать «Зарегистрироваться»')
    def click_register(self):
        self.register_button.click()
        return self
