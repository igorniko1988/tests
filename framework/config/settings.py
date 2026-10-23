from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from pathlib import Path


ENV = os.getenv('ENV','dev')
ENV_FILE = Path(__file__).parent.parent / 'envs' / f'{ENV}.env'

print(ENV_FILE)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_FILE)

    env: str = ENV
    base_url: str
    timeout: float = 10


settings = Settings()

print(settings.base_url)