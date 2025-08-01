from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Union, Optional
from pydantic import AnyHttpUrl, model_validator

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "University Scientific Association API"
    PROJECT_VERSION: str = "0.1.0"

    # Security settings
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # 7 days

    # Database settings
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int = 5432
    SQLALCHEMY_DATABASE_URI: Optional[str] = None

    @model_validator(mode='before')
    def assemble_db_connection(cls, v):
        if isinstance(v, dict) and 'SQLALCHEMY_DATABASE_URI' not in v:
            v['SQLALCHEMY_DATABASE_URI'] = (
                f"postgresql+psycopg2://{v.get('POSTGRES_USER')}:{v.get('POSTGRES_PASSWORD')}"
                f"@{v.get('POSTGRES_SERVER')}:{v.get('POSTGRES_PORT')}/{v.get('POSTGRES_DB')}"
            )
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
