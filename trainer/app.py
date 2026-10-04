"""Тренажёр для лайвкодинга: маленькие API в стиле задач с собеседований.

В эндпоинтах намеренно спрятаны баги. Документация к каждой задаче —
в LIVECODING.md, исходник тренажёра во время решения не смотреть.
"""

from fastapi import FastAPI, Query, Request
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
