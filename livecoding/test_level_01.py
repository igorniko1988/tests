"""
1. Описать тест-кейсы / чек-лист для указанного эндпоинта.
2. Реализовать API-тесты на Python (requests + pytest): сначала самый важный кейс,
   затем остальные — сколько успеешь.

Test cases for GET /v1/products/{product_id} endpoint.

API Documentation:
- URL: http://localhost:8090/v1/products/{product_id}
- Method: GET
- Path parameters:
    - product_id: int, > 0
- Response 200:
    {
        "id": int,              # совпадает с product_id из запроса
        "name": str,            # не пустая строка
        "price": float,         # > 0, число (не строка)
        "in_stock": bool,
    }
- Response 404 (товара нет):
    {"error": "not_found"}
- Response 400 (невалидный product_id: 0, отрицательный, не число):
    {"error": "bad_request"}
- В каталоге товары с id от 1 до 5.
"""

# --- Уточняющие вопросы ---
# 1. Есть ли авторизация? (считаю, что нет)
# 2. id в пути — только целое? Что вернёт "1.5", "01", очень большое число?
# 3. Тело ошибки строго {"error": ...} или могут быть доп. поля?
# 4. price может быть целым (189) или всегда с дробной частью? (считаю: любое число, не строка)
# 5. Данные каталога стабильны (id 1..5 всегда есть)? — от этого зависит, можно ли хардкодить id.

# --- Чек-лист ---
# Позитивные (существующий товар → 200):
#   1. Для КАЖДОГО id 1..5: статус 200, ответ строго по схеме (нет лишних полей)
#   2. id в ответе == id из запроса
#   3. name — строка и не пустая
#   4. price — число (не строка) и > 0
#   5. in_stock — bool (может быть и true, и false!)
# Несуществующий товар → 404 {"error": "not_found"}:
#   6. Граница сразу за последним: 6
#   7. Заведомо большой: 999999
# Невалидный id → 400 {"error": "bad_request"}:
#   8. Граница: 0 (по документации id > 0)
#   9. Отрицательный: -1
#  10. Не число: abc
#  11. Дробное: 1.5
# Прочее (проговорить, если нет времени писать):
#  12. Неверный метод (POST/DELETE) → 405
#  13. Время ответа в пределах SLA
#  14. Content-Type ответа — application/json

# --- Самый важный кейс и почему ---
# Существующий товар возвращается корректно: 200, правильная схема и тот же id.
# Это основной сценарий эндпоинта — если он сломан, всё остальное неважно.

# --- Тесты ---
import pytest
import requests
from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictFloat, StrictInt, StrictStr

BASE_URL = "http://localhost:8090/v1/products"


class Product(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: StrictInt
    name: StrictStr = Field(min_length=1)
    price: StrictFloat | StrictInt = Field(gt=0)
    in_stock: StrictBool


def get_product(product_id):
    return requests.get(f"{BASE_URL}/{product_id}", timeout=10)


@pytest.mark.parametrize("product_id", [1, 2, 3, 4, 5])
def test_existing_product_is_returned(product_id):
    response = get_product(product_id)

    assert response.status_code == 200
    product = Product.model_validate(response.json())
    assert product.id == product_id


@pytest.mark.parametrize("product_id", [6, 999999])
def test_missing_product_returns_404(product_id):
    response = get_product(product_id)

    assert response.status_code == 404
    assert response.json() == {"error": "not_found"}


@pytest.mark.parametrize("product_id", [0, -1, "abc", 1.5])
def test_invalid_product_id_returns_400(product_id):
    response = get_product(product_id)

    assert response.status_code == 400
    assert response.json() == {"error": "bad_request"}
