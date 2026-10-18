import random
from uuid import uuid4


def unique_email(prefix: str = 'user_'):
    return f'{prefix}{uuid4().hex[:8]}@gmail.com'


def unique_password():
    return uuid4().hex[:8]


def credentials():
    email = unique_email()
    password = unique_password()

    return {
        'email': email,
        'password': password
    }


def isolated_price(low: int = 300, high: int = 499) -> str:
    # Стакан общий для всех тестов: цена из «своего» диапазона,
    # чтобы наш ордер не исполнился о чужой ордер с обычной ценой.
    return str(random.randint(low, high))
