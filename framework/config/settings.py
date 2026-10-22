from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    base_url: str = 'http://localhost:8080'
    timeout: float = 10


settings = Settings()