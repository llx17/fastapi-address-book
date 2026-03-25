from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Address Book API"
    APP_VERSION: str = "1.0.0"
    DATABASE_URL: str = "sqlite:///./address_book.db"
    DEBUG: bool = True

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()