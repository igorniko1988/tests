"""C8 t03 (required, ~20 min). Abstract base page.

Implement:

BasePage(ABC), created as BasePage(browser):
- abstract property path (each page must define its URL path);
- abstract method is_loaded() -> bool;
- open(): calls browser.goto(path), then checks is_loaded(); if it is False,
  raise AssertionError(f"{ClassName} is not loaded"); returns self.

LoginPage(BasePage):
- path = "/app/login.html";
- is_loaded() -> browser.is_visible("[data-testid=login-form]");
- login(email, password): browser.fill("[data-testid=email]", email),
  browser.fill("[data-testid=password]", password), browser.click("[data-testid=submit]").

Requirements:
- BasePage(browser) -> TypeError; a subclass without is_loaded -> TypeError on creation.

Follow-up questions:
- What is the "template method" here?
- ABC vs raise NotImplementedError: when does each fail?

Run (from interview_prep/python_course/week3_core): uv run pytest -k c08_t03
Теория: THEORY.md в этой папке, раздел 5.
"""


from abc import ABC, abstractmethod  # noqa: F401


class BasePage:
    pass


class LoginPage(BasePage):
    pass
