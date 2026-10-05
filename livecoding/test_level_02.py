"""
1. Описать тест-кейсы / чек-лист для указанного эндпоинта.
2. Реализовать API-тесты на Python (requests + pytest): сначала самый важный кейс,
   затем остальные — сколько успеешь.

Test cases for GET /v1/catalog endpoint.

API Documentation:
- URL: http://localhost:8090/v1/catalog
- Method: GET
- Query parameters (все необязательные, можно комбинировать):
    - category: str — electronics | clothes | books | home
    - min_price: float, >= 0 — цена от (включительно)
    - max_price: float, >= 0 — цена до (включительно)
    - in_stock: bool — true | false
- Response 200:
    {
        "count": int,                 # сколько товаров в items
        "items": [
            {
                "id": int,
                "name": str,
                "category": str,      # electronics | clothes | books | home
                "price": float,       # > 0
                "in_stock": bool,
            },
        ]
    }
- Без фильтров возвращается весь каталог (12 товаров).
- Если ничего не подошло: {"count": 0, "items": []}
- Response 400 (невалидное значение фильтра или min_price > max_price):
    {"error": "bad_request"}
"""

# BASE_URL = "http://localhost:8090/v1/catalog"


# --- Уточняющие вопросы ---


# --- Чек-лист ---


# --- Самый важный кейс и почему ---


# --- Тесты ---
