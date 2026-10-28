import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Один файл окружения на оба фреймворка: framework/envs/<ENV>.env (BASE_URL, TIMEOUT …)
ENV = os.getenv("ENV", "dev")
ENV_FILE = Path(__file__).parents[2] / "framework" / "envs" / f"{ENV}.env"


class Settings(BaseSettings):
    # extra="ignore": в общем env-файле есть ключи API-фреймворка (TIMEOUT), UI они не нужны
    model_config = SettingsConfigDict(env_file=ENV_FILE, extra="ignore")

    env: str = ENV
    base_url: str
    expect_timeout_ms: int = 5_000
    action_timeout_ms: int = 15_000
    matching_timeout_ms: int = 15_000
