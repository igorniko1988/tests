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
class Account:
    def __init__(self, email, balance = 0):
        self.email = email
        self.balance = balance

    def describe(self):
        return f'{self.email} with the balance {self.balance}'


class AdminAccount(Account):
    def __init__(self, email, balance, permissions: list):
        super().__init__(email, balance)
        self.permissions = permissions

    def describe(self):
        return f'{self.email} with the balance {self.balance} and its admin'

a = Account('nk@gmail.com', 100)
b = AdminAccount('sad@gmail.com',0,[1,2,3,5,5])

print(a.describe())
print(b.describe())

# --- Задача 2 ---

class Balance:
    def __init__(self, asset, available=0):
        self.asset = asset
        self.available = available

    def deposit(self, value):
        self.available += value

class Wallet:
    assets = {'BTC', 'ETH', 'USDT'}

    def __init__(self):
        self.balances = {v:Balance(v) for v in self.assets}

    def get(self, asset):
        return self.balances[asset].available

    def deposit(self, asset, value):
        self.balances[asset].deposit(value)

class Trader:
    def __init__(self, email):
        self.email = email
        self.wallet = Wallet()


w = Wallet()
w.deposit('ETH',12312312)
print(w.get('ETH'))
# --- Задача 3 ---
class Position:
    def __init__(self, quantity, price):
        self.quantity = quantity
        self.price = price

    @property
    def value(self):
        val = self.price * self.quantity
        return val

    @property
    def quantity(self):
        return self._quantity


    @quantity.setter
    def quantity(self, value: int):
        if value < 0:
            raise ValueError('Value is under zero')
        self._quantity = value

p = Position(23,2)

# --- Задача 4 ---

from faker import Faker


class Credentials:
    def __init__(self, email, password):
        self.email = email
        self.password = password

    @staticmethod
    def is_strong(password: str):
        return len(password) > 8

    @classmethod
    def from_dict(cls, data: dict):
        return cls(data['email'], data['password'])

    @classmethod
    def random(cls):
        faker = Faker()
        return cls(faker.email(), faker.password())

print('**********')
fake_creds = Credentials.random()
print(fake_creds.password, fake_creds.email)
print(fake_creds.is_strong(fake_creds.password))
# --- Задача 5 ---
from dataclasses import dataclass, field

@dataclass()
class Order:
    symbol: str
    side: str
    price: float
    quantity: int
    status: str = 'NEW'
    tags: list = field(default_factory=list)

o1 = Order('BTC','short', 2, 10, 'NEW',[1,2,3,4])
o2 = Order('BTC','short', 2, 10, 'NEW',[1,2,3,4,6])

print(o1 == o2 )
o1.tags.append(123)
o1.quantity = 23
print(o1.tags)


# --- Ответы на вопросы собеса ---
# 1. Inheritance answears the question "Is object the parent class", as for composition is parent class has object
# 2. By calling super initializator we adding propertis from parent class
# 3. Property helps for example make validation on definite property
# 4. Classmethod usually uses for creating alternative object, as for staticmethod its like for helping function outside of the using self
# 5. Dataclass uses for models defference between pydantics, dataclass doesnts use type validation
