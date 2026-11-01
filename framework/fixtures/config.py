"""Фикстуры настроек: общие для всех слоёв."""

import pytest

from framework.config.settings import Settings, get_settings


@pytest.fixture(scope="session")
def settings() -> Settings:
    return get_settings()


@pytest.fixture(scope="session")
def base_url(settings: Settings) -> str:
    # pytest-playwright берёт base_url отсюда: page.goto("/app/") → http://localhost:8080/app/
    return settings.base_url
