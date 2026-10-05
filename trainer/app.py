"""Тренажёр для лайвкодинга: маленькие API в стиле задач с собеседований.

В эндпоинтах намеренно спрятаны баги. Документация к каждой задаче —
в LIVECODING.md, исходник тренажёра во время решения не смотреть.
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
async def list_ads(commercial: int = Query(ge=0, le=101)):
    commercial_count = TOTAL_ADS * commercial // 101
    ads = []
    for i in range(commercial_count):
        ads.append({"ad_id": i + 1, "type": "commercial", "format": FORMATS[i % 2]})
    for i in range(TOTAL_ADS - commercial_count):
        ads.append({"ad_id": i + 1, "type": "nonprofit", "format": FORMATS[i % 2]})
    return {"count": len(ads), "ads": ads}


# --- Уровень 1: GET /v1/products/{product_id} --------------------------------

PRODUCTS = {
    1: {"id": 1, "name": "Keyboard", "price": 49.9, "in_stock": True},
    2: {"id": 2, "name": "Mouse", "price": 19.99, "in_stock": True},
    3: {"id": 3, "name": "Monitor", "price": 189.0, "in_stock": False},
    4: {"id": 4, "name": "Headset", "price": "59.5", "in_stock": True},
    5: {"id": 5, "name": "", "price": 9.99, "in_stock": True},
}


@app.get("/v1/products/{product_id}")
async def get_product(product_id: int = Path(ge=0)):
    product = PRODUCTS.get(product_id)
    if product is None:
        return JSONResponse(status_code=404, content={"error": "not_found"})
    return product
