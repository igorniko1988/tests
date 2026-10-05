import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """Настройки окружения. Значения берутся из envs/<ENV>.env и переменных API_*."""

    model_config = SettingsConfigDict(env_prefix="API_", extra="ignore")

    base_url: str = "http://localhost:8080"
    timeout: float = 10


def load_config() -> Config:
    env = os.environ.get("ENV", "docker")
    return Config(_env_file=f"envs/{env}.env")
