from typing import Any

from pydantic_settings import BaseSettings
from sqlalchemy.ext.declarative import declarative_base

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    DB_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5433/courses"
    DBBaseModel: Any = declarative_base()

    class Config:
        # Define case sensitive settings
        case_sensitive = True


# Settings class instance to be used in other modules
settings = Settings()