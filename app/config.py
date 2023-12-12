import os
from typing import Literal

from pydantic import PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import NullPool


class Settings(BaseSettings):
    mode: Literal["DEV", "TEST", "PROD"]

    smtp_host: str
    smtp_port: int
    smtp_user: str
    smtp_pass: str

    redis_host: str
    redis_port: int

    secret_key: str
    secret_algo: str

    admin_secret_key: str

    model_config = SettingsConfigDict(
        env_file=".env.test" if os.getenv("MODE") == "TEST" else ".env",
        extra="ignore"
    )

    @property
    def redis_url(self) -> RedisDsn:
        return f"redis://{self.redis_host}:{self.redis_port}"


class DbSettings(BaseSettings):
    db_host: str
    db_port: int
    db_user: str
    db_password: str
    db_name: str

    @property
    def database_url(self) -> PostgresDsn:
        driver = "postgresql+asyncpg"
        user = f"{self.db_user}:{self.db_password}"
        database = f"{self.db_host}:{self.db_port}/{self.db_name}"
        return f"{driver}://{user}@{database}"

    model_config = SettingsConfigDict(
        env_file=".env.test" if os.getenv("MODE") == "TEST" else ".env",
        extra="ignore"
    )

    @property
    def database_params(self) -> dict:
        return {"poolclass": NullPool} if settings.mode == "TEST" else {}


settings = Settings()
db_settings = DbSettings()
