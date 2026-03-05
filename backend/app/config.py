from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    redis_url: str = "redis://localhost:6379"
    rate_cache_ttl: int = 900
    log_level: str = "info"

    class Config:
        env_file = ".env"


settings = Settings()
