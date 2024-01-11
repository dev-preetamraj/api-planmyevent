from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_NAME: str
    DB_URL: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRY_MINUTES: int = 5
    REFRESH_TOKEN_EXPIRY_DAYS: int = 7

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
