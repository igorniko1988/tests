import os
from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).resolve().parents[2]
ENVS_DIR = ROOT_DIR / "envs"
ENV = os.getenv("ENV", "docker")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="UI_",
        env_file=(ENVS_DIR / f"{ENV}.env", ROOT_DIR / ".env"),
        extra="ignore",
    )

    env: str = ENV
    base_url: str
    user_email: str | None = None
    user_password: SecretStr
    expect_timeout_ms: int = 5_000
    action_timeout_ms: int = 15_000
    matching_timeout_ms: int = 15_000