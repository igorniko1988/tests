import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV = os.getenv("ENV", "docker")
ENV_FILE = Path(__file__).parents[2] / "envs" / f"{ENV}.env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="UI_", env_file=ENV_FILE)

    env: str = ENV
    base_url: str
    expect_timeout_ms: int = 5_000
    action_timeout_ms: int = 15_000
    matching_timeout_ms: int = 15_000