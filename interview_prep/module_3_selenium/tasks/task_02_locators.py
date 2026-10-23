"""Задача 2. Локаторы.

Во всех функциях страница {base_url}/login.html уже открыта.
Верните найденный ЭЛЕМЕНТ (не текст).

Нужные импорты:  from selenium.webdriver.common.by import By

Проверка: pytest -k task_02 -q
"""


def find_username_by_id(driver):
    """Поле логина по id (id="username")."""
    raise NotImplementedError


def find_login_button_by_css(driver):
    """Кнопку входа по CSS-селектору через классы: класс btn И класс primary."""
    raise NotImplementedError


def find_help_link_by_xpath(driver):
    """Ссылку по тексту "Help" через XPath."""
    raise NotImplementedError


def find_password_by_testid(driver):
    """Поле пароля по атрибуту data-testid="password" через CSS."""
    raise NotImplementedError
