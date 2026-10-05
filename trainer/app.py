"""Тренажёр для лайвкодинга: маленькие API в стиле задач с собеседований.

Эндпоинты работают строго по документации из LIVECODING.md — цель тренажёра
научиться писать тесты, а не искать баги.
"""

from fastapi import FastAPI, Path, Query, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

app = FastAPI(title="Livecoding trainer", version="0.1.0")


@app.exception_handler(RequestValidationError)
async def bad_request(_: Request, exc: RequestValidationError):
    return JSONResponse(status_code=400, content={"error": "bad_request"})


@app.get("/health")
async def health():
    return {"status": "ok"}


# --- Задача 1: GET /v1/ads/ ---------------------------------------------------

TOTAL_ADS = 20
FORMATS = ("video", "picture")


@app.get("/v1/ads/")
async def list_ads(commercial: int = Query(ge=0, le=100)):
    commercial_count = TOTAL_ADS * commercial // 100
    ads = []
    for i in range(commercial_count):
        ads.append({"ad_id": i + 1, "type": "commercial", "format": FORMATS[i % 2]})
    for i in range(TOTAL_ADS - commercial_count):
        ad_id = commercial_count + i + 1
        ads.append({"ad_id": ad_id, "type": "nonprofit", "format": FORMATS[i % 2]})
    return {"count": len(ads), "ads": ads}


# --- Уровень 1: GET /v1/products/{product_id} --------------------------------

PRODUCTS = {
    1: {"id": 1, "name": "Keyboard", "price": 49.9, "in_stock": True},
    2: {"id": 2, "name": "Mouse", "price": 19.99, "in_stock": True},
    3: {"id": 3, "name": "Monitor", "price": 189.0, "in_stock": False},
    4: {"id": 4, "name": "Headset", "price": 59.5, "in_stock": True},
    5: {"id": 5, "name": "Cable", "price": 9.99, "in_stock": True},
}


@app.get("/v1/products/{product_id}")
async def get_product(product_id: int = Path(gt=0)):
    product = PRODUCTS.get(product_id)
    if product is None:
        return JSONResponse(status_code=404, content={"error": "not_found"})
    return product


# --- Уровень 1, задача 2: GET /v1/users/{user_id} ----------------------------

USERS = {
    1: {
        "id": 1,
        "email": "anna@example.com",
        "age": 28,
        "status": "active",
        "created_at": "2025-03-14T10:00:00Z",
    },
    2: {
        "id": 2,
        "email": "boris@example.com",
        "age": 35,
        "status": "active",
        "created_at": "2025-04-01T08:30:00Z",
    },
    3: {
        "id": 3,
        "email": "vera@example.com",
        "age": 21,
        "status": "blocked",
        "created_at": "2025-05-20T15:45:00Z",
    },
    4: {
        "id": 4,
        "email": "gleb@example.com",
        "age": 42,
        "status": "active",
        "created_at": "2025-06-02T12:00:00Z",
    },
    5: {
        "id": 5,
        "email": "dina@example.com",
        "age": 63,
        "status": "blocked",
        "created_at": "2025-07-11T09:15:00Z",
    },
    6: {
        "id": 6,
        "email": "egor@example.com",
        "age": 19,
        "status": "active",
        "created_at": "2025-08-30T18:20:00Z",
    },
}


@app.get("/v1/users/{user_id}")
async def get_user(user_id: int = Path(gt=0)):
    user = USERS.get(user_id)
    if user is None:
        return JSONResponse(status_code=404, content={"error": "not_found"})
    return user
