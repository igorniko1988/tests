"""Задача 4. Явное ожидание.

get_dynamic_text(driver, base_url):
  1. открыть {base_url}/dynamic.html
  2. нажать кнопку Start (id="start")
  3. дождаться, пока появится блок id="result" (появится через ~2 секунды)
  4. вернуть его текст ("Hello World!")

ЗАПРЕЩЕНО: time.sleep(...). Используйте WebDriverWait + expected_conditions.

Нужные импорты:
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

Проверка: pytest -k task_04 -q
"""


def get_dynamic_text(driver, base_url):
    raise NotImplementedError
