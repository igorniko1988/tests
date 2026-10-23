from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class LoginPage(BasePage):
    USERNAME = (By.ID, "username")
    PASSWORD = (By.ID, "password")
    SUBMIT = (By.ID, "login-btn")
    FLASH = (By.ID, "flash")

    def open_page(self):
        return self.open("login.html")

    def login(self, user, password):
        self.type_text(self.USERNAME, user)
        self.type_text(self.PASSWORD, password)
        self.click(self.SUBMIT)
        return self

    def message(self):
        return self.text_of(self.FLASH)
