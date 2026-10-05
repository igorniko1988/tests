"""Тренажёр для лайвкодинга: маленькие API в стиле задач с собеседований.

Эндпоинты работают строго по документации из LIVECODING.md — цель тренажёра
научиться писать тесты, а не искать баги.
"""

from typing import Literal

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


# --- Уровень 2: GET /v1/catalog — фильтры через query-параметры ---------------

CATALOG = [
    {"id": 1, "name": "Laptop", "category": "electronics", "price": 999.0, "in_stock": True},
    {"id": 2, "name": "Phone", "category": "electronics", "price": 599.0, "in_stock": False},
    {"id": 3, "name": "Headphones", "category": "electronics", "price": 79.9, "in_stock": True},
    {"id": 4, "name": "T-shirt", "category": "clothes", "price": 15.0, "in_stock": True},
    {"id": 5, "name": "Jacket", "category": "clothes", "price": 120.0, "in_stock": True},
    {"id": 6, "name": "Sneakers", "category": "clothes", "price": 89.0, "in_stock": False},
    {"id": 7, "name": "Novel", "category": "books", "price": 12.5, "in_stock": True},
    {"id": 8, "name": "Cookbook", "category": "books", "price": 25.0, "in_stock": False},
    {"id": 9, "name": "Atlas", "category": "books", "price": 45.0, "in_stock": True},
    {"id": 10, "name": "Mug", "category": "home", "price": 9.99, "in_stock": True},
    {"id": 11, "name": "Lamp", "category": "home", "price": 45.0, "in_stock": True},
    {"id": 12, "name": "Chair", "category": "home", "price": 150.0, "in_stock": False},
]


@app.get("/v1/catalog")
async def search_catalog(
    category: Literal["electronics", "clothes", "books", "home"] | None = None,
    min_price: float | None = Query(default=None, ge=0),
    max_price: float | None = Query(default=None, ge=0),
    in_stock: bool | None = None,
):
    if min_price is not None and max_price is not None and min_price > max_price:
        return JSONResponse(status_code=400, content={"error": "bad_request"})
    items = [
        item
        for item in CATALOG
        if (category is None or item["category"] == category)
        and (min_price is None or item["price"] >= min_price)
        and (max_price is None or item["price"] <= max_price)
        and (in_stock is None or item["in_stock"] == in_stock)
    ]
    return {"count": len(items), "items": items}
