"""Задача 3. Войти и прочитать сообщение.

login(driver, base_url, username, password):
  1. открыть {base_url}/login.html
  2. ввести логин и пароль
  3. нажать кнопку входа
  4. вернуть ТЕКСТ сообщения из блока с id="flash"

Верные данные: tomsmith / SuperSecretPassword!
  -> "You logged into a secure area!"
Неверные: любые другие
  -> "Your username or password is invalid!"

Подсказки: send_keys(), click(), .text

Проверка: pytest -k task_03 -q
"""


def login(driver, base_url, username, password):
    raise NotImplementedError
