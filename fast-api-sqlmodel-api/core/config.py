from pydantic import BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    DB_URL: str = "postgresql+asyncpq://postgres:postgres@localhost:5432/postgres"

    class Config:
        case_sensitive = True


settings = Settings()
