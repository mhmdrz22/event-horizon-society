from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Union, Optional
from pydantic import AnyHttpUrl, model_validator

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "University Scientific Association API"
    PROJECT_VERSION: str = "0.1.0"

    # Security settings
    SECRET_KEY: str = "a_very_secret_key_that_should_be_in_env_file_or_generated"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # 7 days

    # Database settings
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int = 5432
    DATABASE_URL: Optional[str] = None

    @model_validator(mode='before')
    def assemble_db_connection(cls, v):
        if isinstance(v, dict) and 'DATABASE_URL' not in v:
            postgres_user = v.get('POSTGRES_USER')
            postgres_password = v.get('POSTGRES_PASSWORD')
            postgres_server = v.get('POSTGRES_SERVER')
            postgres_port = v.get('POSTGRES_PORT')
            postgres_db = v.get('POSTGRES_DB')
            v['DATABASE_URL'] = f"postgresql+psycopg2://{postgres_user}:{postgres_password}@{postgres_server}:{postgres_port}/{postgres_db}"
        return v

    # Backend CORS origins
    BACKEND_CORS_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000"

    @property
    def BACKEND_CORS_ORIGINS_LIST(self) -> list[str]:
        return [origin.strip() for origin in self.BACKEND_CORS_ORIGINS.split(',')]

    # Email settings
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: Optional[int] = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[str] = None
    EMAILS_FROM_NAME: Optional[str] = None

    # SMS settings
    SMS_API_KEY: Optional[str] = None
    SMS_SENDER_NUMBER: Optional[str] = None

    # Redis settings
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    # First superuser
    FIRST_SUPERUSER_EMAIL: str = "admin@example.com"
    FIRST_SUPERUSER_FULL_NAME: str = "Admin User"
    FIRST_SUPERUSER_PASSWORD: str = "adminpassword"

    # Pydantic V2 model_config
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra='ignore')

settings = Settings()
