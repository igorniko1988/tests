from pydantic_settings import BaseSettings, SettingsConfigDict


class ServiceSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="EXCHANGE_", env_file=".env", extra="ignore")

    database_url: str = "postgresql+asyncpg://exchange:exchange@localhost:5432/exchange"
    jwt_secret: str = "local-dev-secret-change-me-32-bytes-min"
    jwt_algorithm: str = "HS256"
    access_token_ttl_seconds: int = 900
    chaos_rate: float = 0.0


settings = ServiceSettings()
