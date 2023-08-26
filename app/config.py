from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DMS: Optional[str] = None
    DMS_DRIVER: Optional[str] = None
    DB_HOST: Optional[str] = None
    DB_PORT: Optional[int] = None
    DB_USER: Optional[str] = None
    DB_PASS: Optional[str] = None
    DB_NAME: Optional[str] = None

    @property
    def database_url(self) -> str:
        driver = f'{self.DMS}+{self.DMS_DRIVER}'
        user = f"{self.DB_USER}:{self.DB_PASS}"
        database = f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        return f"{driver}://{user}@{database}"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
