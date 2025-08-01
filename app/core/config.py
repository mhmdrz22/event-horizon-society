from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Union, Optional
from pydantic import AnyHttpUrl, model_validator, ValidationError

# Base settings class that doesn't include database configuration
class CoreSettings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "University Scientific Association API"
    PROJECT_VERSION: str = "0.1.0"
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    BACKEND_CORS_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000"

    @property
    def BACKEND_CORS_ORIGINS_LIST(self) -> list[str]:
        return [origin.strip() for origin in self.BACKEND_CORS_ORIGINS.split(',')]

    SMTP_HOST: Optional[str] = None
    SMTP_PORT: Optional[int] = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[str] = None
    EMAILS_FROM_NAME: Optional[str] = None
    SMS_API_KEY: Optional[str] = None
    SMS_SENDER_NUMBER: Optional[str] = None
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    FIRST_SUPERUSER_EMAIL: str = "admin@example.com"
    FIRST_SUPERUSER_FULL_NAME: str = "Admin User"
    FIRST_SUPERUSER_PASSWORD: str = "adminpassword"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra='ignore')

# Separate class for PostgreSQL settings
class PostgresSettings(BaseSettings):
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int = 5432

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra='ignore')

# Final settings class that will be used by the application
class Settings(CoreSettings):
    SQLALCHEMY_DATABASE_URI: str
    DB_TYPE: str

# --- Logic to assemble the final settings object ---
try:
    # Try to load PostgreSQL settings from environment variables
    pg_settings = PostgresSettings()
    db_uri = f"postgresql+psycopg2://{pg_settings.POSTGRES_USER}:{pg_settings.POSTGRES_PASSWORD}@{pg_settings.POSTGRES_SERVER}:{pg_settings.POSTGRES_PORT}/{pg_settings.POSTGRES_DB}"
    db_type = "postgresql"
except ValidationError:
    # If it fails (i.e., env vars are not set), fall back to SQLite
    db_uri = "sqlite:///./app.db"
    db_type = "sqlite"

# Instantiate the core settings
core_settings = CoreSettings()

# Create the final settings object, injecting the determined database URI
settings = Settings(
    **core_settings.model_dump(),
    SQLALCHEMY_DATABASE_URI=db_uri,
    DB_TYPE=db_type
)
