from typing import Literal

from pydantic import PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MODE: Literal["DEV", "TEST", "PROD"]

    DB_HOST: str
    DB_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_USER: str
    TEST_DB_PASSWORD: str
    TEST_DB_NAME: str

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASS: str

    REDIS_HOST: str
    REDIS_PORT: int

    JWT_KEY: str
    JWT_ALGO: str

    ADMIN_SECRET_KEY: str

    model_config = SettingsConfigDict(env_file=".env")

    @property
    def database_url(self) -> PostgresDsn:
        user = f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
        database = f"{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB}"
        return f"{self._database_driver}://{user}@{database}"

    @property
    def test_database_url(self) -> PostgresDsn:
        user = f"{self.TEST_DB_USER}:{self.TEST_DB_PASSWORD}"
        database = f"{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}"
        return f"{self._database_driver}://{user}@{database}"

    @property
    def redis_url(self) -> RedisDsn:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

    @property
    def _database_driver(self) -> str:
        return "postgresql+asyncpg"


settings = Settings()
