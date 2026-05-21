from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "dev"
    app_name: str = "LMS MVP API"
    database_url: str = "postgresql://postgres:xVFOrWrHXkYlYanwDNmaRvmcQbJayoOd@postgres.railway.internal:5432/railway"
    cors_origins: str = "https://cuongc15.vercel.app/"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
