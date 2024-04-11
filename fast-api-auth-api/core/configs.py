from typing import Any

from pydantic_settings import BaseSettings
from sqlalchemy.ext.declarative import declarative_base

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    DB_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5433/courses"
    DBBaseModel: Any = declarative_base()

    # Auth settings
    """
    # Generate a random secret key
    import secrets

    token: str = secrets.token_urlsafe(32)

    To read more about secret_key: https://stackoverflow.com/questions/31309759/what-is-secret-key-for-jwt-based-authentication-and-how-to-generate-it
    """
    JWT_SECRET: str = 'QF44SLdls4dcjdJqg3noY5qcoiIilx_jPSuWNandl7o'
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # one week = 60 minutes * 24 hours * 7 days

    class Config:
        case_sensitive = True


settings = Settings()