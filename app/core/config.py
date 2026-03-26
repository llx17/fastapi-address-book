from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Address Book API"
    APP_VERSION: str = "1.0.0"
    DATABASE_URL: str = "sqlite:///./address_book.db"
    DEBUG: bool = True
    
    JWT_SECRET_KEY: str = "fallback-secret-key"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24
    
    DEMO_USERNAME: str = "demo"
    DEMO_PASSWORD: str = "demo123"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()