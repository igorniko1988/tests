"""
1. Описать тест-кейсы / чек-лист для указанного эндпоинта.
2. Реализовать API-тесты на Python (requests + pytest): сначала самый важный кейс,
   затем остальные — сколько успеешь.

Test cases for GET /v1/users/{user_id} endpoint.

API Documentation:
- URL: http://localhost:8090/v1/users/{user_id}
- Method: GET
- Path parameters:
    - user_id: int, > 0
- Response 200:
    {
        "id": int,              # совпадает с user_id из запроса
        "email": str,           # валидный email
        "age": int,             # от 18 до 120 (сервис только для совершеннолетних)
        "status": str,          # active | blocked
        "created_at": str,      # дата-время в ISO 8601, UTC
    }
- Response 404 (пользователя нет):
    {"error": "not_found"}
- Response 400 (невалидный user_id):
    {"error": "bad_request"}
- В системе пользователи с id от 1 до 6.
"""

# BASE_URL = "http://localhost:8090/v1/users/"


# --- Уточняющие вопросы ---


# --- Чек-лист ---


# --- Самый важный кейс и почему ---


# --- Тесты ---
