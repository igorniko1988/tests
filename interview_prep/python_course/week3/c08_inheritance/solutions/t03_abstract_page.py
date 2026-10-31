from abc import ABC, abstractmethod


class BasePage(ABC):
    def __init__(self, browser) -> None:
        self.browser = browser

    @property
    @abstractmethod
    def path(self) -> str: ...

    @abstractmethod
    def is_loaded(self) -> bool: ...

    def open(self):
        self.browser.goto(self.path)
        if not self.is_loaded():
            raise AssertionError(f"{type(self).__name__} is not loaded")
        return self


class LoginPage(BasePage):
    path = "/app/login.html"

    def is_loaded(self) -> bool:
        return self.browser.is_visible("[data-testid=login-form]")

    def login(self, email: str, password: str) -> None:
        self.browser.fill("[data-testid=email]", email)
        self.browser.fill("[data-testid=password]", password)
        self.browser.click("[data-testid=submit]")
