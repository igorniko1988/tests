from pydantic_settings import BaseSettings, SettingsConfigDict


class ServiceSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="EXCHANGE_", env_file=".env", extra="ignore")

    database_url: str = "postgresql+asyncpg://exchange:exchange@localhost:5432/exchange"
    jwt_secret: str = "local-dev-secret-change-me-32-bytes-min"
    jwt_algorithm: str = "HS256"
    access_token_ttl_seconds: int = 900
    refresh_token_ttl_seconds: int = 86400
    login_max_failures: int = 5
    login_failure_window: int = 60
    admin_email: str = "admin@mini-exchange.io"
    admin_password: str = "admin-password"
    chaos_rate: float = 0.0
    matching_interval: float = 1.0
    webhook_max_attempts: int = 4
    webhook_retry_delay: float = 1.0
    kafka_bootstrap: str = ""
    rabbitmq_url: str = ""
    price_feed_url: str = ""
    price_feed_timeout: float = 2.0
    price_max_age: float = 10.0


settings = ServiceSettings()
