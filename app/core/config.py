from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Union, Optional
import os
from pydantic import AnyHttpUrl, model_validator, PostgresDsn

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "University Scientific Association API"
    PROJECT_VERSION: str = "0.1.0"

    # Security settings
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # 7 days

    # Database settings
    POSTGRES_SERVER: Optional[str] = None
    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None
    POSTGRES_DB: Optional[str] = None
    POSTGRES_PORT: Optional[int] = 5432
    SQLALCHEMY_DATABASE_URI: Optional[str] = None

    @model_validator(mode='before')
    def assemble_db_connection(cls, v):
        if os.getenv("TESTING") == "True":
            v['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"
            return v

        if isinstance(v, dict) and 'SQLALCHEMY_DATABASE_URI' not in v:
            # Only build the DSN if we are NOT in testing mode
            # and if the necessary environment variables are provided.
            if v.get("POSTGRES_SERVER"):
                dsn = PostgresDsn.build(
                    scheme="postgresql+psycopg2",
                    username=v.get("POSTGRES_USER"),
                    password=v.get("POSTGRES_PASSWORD"),
                    host=v.get("POSTGRES_SERVER"),
                    port=v.get("POSTGRES_PORT"),
                    path=f"/{v.get('POSTGRES_DB') or ''}",
                )
                v['SQLALCHEMY_DATABASE_URI'] = str(dsn)
        return v

    # Backend CORS origins
    BACKEND_CORS_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000"

    @property
    def BACKEND_CORS_ORIGINS_LIST(self) -> list[str]:
        return [origin.strip() for origin in self.BACKEND_CORS_ORIGINS.split(',')]

    # First superuser
    FIRST_SUPERUSER_EMAIL: str = "admin@example.com"
    FIRST_SUPERUSER_FULL_NAME: str = "Admin User"
    FIRST_SUPERUSER_PASSWORD: str = "adminpassword"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra='ignore')

settings = Settings()
