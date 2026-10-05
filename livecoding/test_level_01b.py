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
import requests
import pytest

from datetime import datetime
from pydantic import BaseModel, ConfigDict, StrictInt, StrictStr, EmailStr, Field
from enum import StrEnum


BASE_URL = 'http://localhost:8090/v1/users/'

class UserStatus(StrEnum):
    ACTIVE = 'active'
    BLOCKED = 'blocked'


class User(BaseModel):
    model_config = ConfigDict(extra='forbid')


    id: StrictInt
    email: EmailStr
    age: StrictInt = Field(ge=18, lt=120)
    status: UserStatus
    created_at: datetime

class ErrorMessage(BaseModel):
    model_config = ConfigDict(extra='forbid')


def get_user(user_id):
    return requests.get(BASE_URL + f'{user_id}')

@pytest.mark.parametrize('user_id', [1,2,3,4,5,6])
def test_get_valid_users_by_id(user_id):
    response = get_user(user_id)

    assert response.status_code == 200
    user = User.model_validate(response.json())

    assert user.id == user_id
    assert '@' in user.email


@pytest.mark.parametrize('user_id, status_code,error_message',[
    (0,400,'bad_request'),
    (7,404,    'not_found'),
    (123213,404,'not_found'),
    (-1,400,'bad_request'),
])
def test_undefined_user(user_id, status_code, error_message):
    response = get_user(user_id)

    assert response.status_code == status_code

    assert response.json()['error'] == error_message
