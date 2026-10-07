"""
F1. Урок 2 — наследование, композиция, @property, @classmethod, @staticmethod, dataclasses.

Теория: practice/f1_02_inheritance.md
Запуск: uv run python practice/f1_02_inheritance.py

Задача 1. Наследование.
    Класс Account с атрибутами email и balance (по умолчанию 0) и методом describe(),
    который возвращает строку "email: balance".
    Класс AdminAccount(Account): дополнительно принимает permissions (список),
    вызывает super().__init__(...) и переопределяет describe(), добавляя "(admin)" в конце.
    Создай оба объекта и выведи describe().

Задача 2. Композиция.
    Класс Wallet содержит три объекта Balance (из урока 1, можно упрощённый: asset, available)
    для "USDT", "BTC", "ETH" — в словаре self.balances.
    Метод get(asset) возвращает нужный Balance.
    Класс Trader содержит email и Wallet. Пополни trader.wallet.get("USDT") на 100 и выведи остаток.

Задача 3. @property.
    Класс Position(quantity, price) со свойством value = quantity * price.
    Добавь свойство quantity с сеттером: отрицательное количество -> ValueError.
    Проверь: поменяй quantity и выведи value (должно пересчитаться); попробуй -1 (поймай ошибку).

Задача 4. @classmethod и @staticmethod.
    Класс Credentials(email, password):
    - @staticmethod is_strong(password) -> True, если длина >= 8 и есть хотя бы одна цифра;
    - @classmethod from_dict(data) -> Credentials из словаря {"email": ..., "password": ...};
    - @classmethod random() -> Credentials со случайным email и сильным паролем (можно через Faker).
    Создай объекты обоими способами и проверь пароли через is_strong.

Задача 5. dataclass.
    @dataclass Order: symbol, side, price, quantity, status="NEW", tags (список, свой у каждого).
    - создай два одинаковых ордера и сравни через == (должно быть True);
    - добавь тег в один ордер и убедись, что у второго список пустой;
    - сделай вариант @dataclass(frozen=True) и попробуй изменить поле — что будет?

Вопросы собеса (ответь своими словами внизу файла):
    1. Чем наследование отличается от композиции? Что выбираешь чаще и почему?
    2. Зачем super()? Что будет, если не вызвать super().__init__()?
    3. Зачем @property, если можно сделать обычный метод?
    4. Чем @classmethod отличается от @staticmethod? Пример, когда нужен каждый.
    5. Что даёт @dataclass? Чем dataclass отличается от Pydantic-модели?
"""


# --- Задача 1 ---


# --- Задача 2 ---


# --- Задача 3 ---


# --- Задача 4 ---


# --- Задача 5 ---


# --- Ответы на вопросы собеса ---
# 1.
# 2.
# 3.
# 4.
# 5.
