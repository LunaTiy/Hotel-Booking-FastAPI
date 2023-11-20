from pydantic import PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASS: str

    REDIS_HOST: str
    REDIS_PORT: int

    JWT_KEY: str
    JWT_ALGO: str

    ADMIN_SECRET_KEY: str

    @property
    def database_url(self) -> PostgresDsn:
        driver = "postgresql+asyncpg"
        user = f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
        database = f"{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB}"
        return f"{driver}://{user}@{database}"

    @property
    def redis_url(self) -> RedisDsn:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
