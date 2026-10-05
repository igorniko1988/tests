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

# BASE_URL = "http://localhost:8090/v1/products/"


# --- Уточняющие вопросы ---


# --- Чек-лист ---


# --- Самый важный кейс и почему ---


# --- Тесты ---
