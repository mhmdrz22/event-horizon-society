from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Union, Optional # Added Optional
from pydantic import AnyHttpUrl # validator removed as it's not used with Pydantic V2 style

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "University Scientific Association API"
    PROJECT_VERSION: str = "0.1.0"

    # Security settings
    SECRET_KEY: str = "a_very_secret_key_that_should_be_in_env_file_or_generated"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # 7 days

    # Database settings
    # The default is to use SQLite for simple, local development.
    # You can override this with a full PostgreSQL DSN in your .env file
    # For example: DATABASE_URL="postgresql+psycopg2://user:password@host:port/dbname"
    DATABASE_URL: str = "sqlite:///./test.db"

    # The following property is kept for compatibility but the direct DATABASE_URL is preferred.
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return self.DATABASE_URL

    # Backend CORS origins
    BACKEND_CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

    @property
    def BACKEND_CORS_ORIGINS_LIST(self) -> list[str]:
        return [origin.strip() for origin in self.BACKEND_CORS_ORIGINS.split(',')]

    # Email settings
    SMTP_HOST: Optional[str] = None # Changed from "localhost" to None for more realistic default
    SMTP_PORT: Optional[int] = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[str] = None # Changed from "noreply@example-association.ir"
    EMAILS_FROM_NAME: Optional[str] = None # Changed from "University Scientific Association"

    # SMS settings
    SMS_API_KEY: Optional[str] = None
    SMS_SENDER_NUMBER: Optional[str] = None

    # Redis settings
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    # Pydantic V2 model_config
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra='ignore')

settings = Settings()
