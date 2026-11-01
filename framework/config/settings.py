"""Одни настройки на весь фреймворк: API, UI и отчёты читают их отсюда.

Откуда берутся значения (выигрывает верхнее):
1. переменные окружения процесса: BASE_URL=... uv run pytest (так делает CI);
2. файл config/envs/<ENV>.env, где ENV — переменная окружения (по умолчанию dev);
3. значения по умолчанию в классе ниже.
"""

import os
from functools import cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ENVS_DIR = Path(__file__).parent / "envs"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENVS_DIR / f"{os.getenv('ENV', 'dev')}.env",
        extra="ignore",
    )

    env: str = "dev"
    base_url: str = "http://localhost:8080"

    # API: таймаут одного HTTP-запроса, секунды
    timeout: float = 10

    # UI: ожидания Playwright, миллисекунды
    expect_timeout_ms: int = 5_000
    action_timeout_ms: int = 15_000
    matching_timeout_ms: int = 15_000

    @property
    def ws_url(self) -> str:
        # http://host:8080 → ws://host:8080, https → wss
        return "ws" + self.base_url.removeprefix("http")


@cache
def get_settings() -> Settings:
    # Один объект на весь прогон; создаётся при первом обращении, а не при импорте модуля
    return Settings(env=os.getenv("ENV", "dev"))
