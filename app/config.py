from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DMS: str
    DMS_DRIVER: str
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def database_url(self):
        driver = f'{self.DMS}+{self.DMS_DRIVER}'
        user = f"{self.DB_USER}:{self.DB_PASS}"
        database = f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        return f"{driver}://{user}@{database}"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
