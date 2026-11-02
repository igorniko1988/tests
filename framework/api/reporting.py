"""Лог и Allure для каждого HTTP-запроса. Секреты в отчёт не попадают."""

import json
import logging

import allure
from requests import Response

logger = logging.getLogger("api")

SECRET_KEYS = {"password", "access_token", "refresh_token", "secret", "signature"}


def mask(body: bytes | str | None) -> str | None:
    """JSON-тело с секретами → то же тело, где значения секретов заменены на ***."""
    if not body:
        return None
    text = body.decode() if isinstance(body, bytes) else body
    try:
        data = json.loads(text)
    except ValueError:
        return text
    if isinstance(data, dict):
        data = {key: "***" if key in SECRET_KEYS else value for key, value in data.items()}
    return json.dumps(data, ensure_ascii=False, indent=2)


def report(response: Response) -> None:
    request = response.request
    logger.info(
        "%s %s -> %s (%d ms) request_id=%s",
        request.method, response.url, response.status_code,
        response.elapsed.total_seconds() * 1000, response.headers.get("X-Request-ID"),
    )
    request_body = mask(request.body)
    if request_body:
        allure.attach(request_body, name="request", attachment_type=allure.attachment_type.JSON)
    allure.attach(mask(response.text) or "", name=f"response {response.status_code}",
                  attachment_type=allure.attachment_type.JSON)
