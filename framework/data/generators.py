"""Тестовые данные — одни для API и UI.

Каждый тест получает своего пользователя: тесты не мешают друг другу и идут параллельно (-n 4).
"""

import random
from uuid import uuid4


def unique_email(prefix: str = "user_") -> str:
    return f"{prefix}{uuid4().hex[:8]}@test.io"


def unique_password() -> str:
    return uuid4().hex[:12]


def credentials() -> dict[str, str]:
    return {"email": unique_email(), "password": unique_password()}


def isolated_price(low: int = 300, high: int = 499) -> str:
    # Стакан общий для всех тестов: цена из «своего» диапазона,
    # чтобы наш ордер не исполнился о чужой ордер с обычной ценой.
    return str(random.randint(low, high))
