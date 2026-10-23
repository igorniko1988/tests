"""Задача 5. Действия с формой, списком и таблицей.

Все функции сами открывают {base_url}/form.html.

Нужный импорт для списка:  from selenium.webdriver.support.ui import Select

Проверка: pytest -k task_05 -q
"""


def select_country(driver, base_url, country_name):
    """Выбрать страну в выпадающем списке по видимому тексту (например "Poland").
    Вернуть текст выбранного пункта."""
    raise NotImplementedError


def tick_agree(driver, base_url):
    """Отметить чекбокс "I agree" (id="agree"), только если он ещё не отмечен.
    Вернуть True, если после этого он отмечен."""
    raise NotImplementedError


def get_items(driver, base_url):
    """Вернуть список текстов всех элементов <li class="item">.
    Ожидается: ["Apple", "Banana", "Cherry"]"""
    raise NotImplementedError


def get_admin_name(driver, base_url):
    """В таблице id="users" найти пользователя с ролью admin и вернуть его имя.
    Ожидается: "Anna" """
    raise NotImplementedError
