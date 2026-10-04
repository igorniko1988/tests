from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="API_", env_file=".env")

    base_url: str = "http://localhost:8080"
    timeout: float = 10
    db_url: str | None = None
