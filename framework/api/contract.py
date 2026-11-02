"""Сверка тела ответа со схемой из OpenAPI самого сервиса."""

from functools import cache

import jsonschema
import requests

from framework.config.settings import get_settings


@cache
def openapi_spec() -> dict:
    settings = get_settings()
    return requests.get(f"{settings.base_url}/openapi.json", timeout=settings.timeout).json()


def assert_matches_schema(data, schema_name: str) -> None:
    schema = {"$ref": f"#/components/schemas/{schema_name}", "components": openapi_spec()["components"]}
    jsonschema.validate(data, schema)
