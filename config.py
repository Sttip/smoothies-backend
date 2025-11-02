from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+psycopg://usuario:password@localhost:5432/smoothies"
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "https://tuusuario.github.io"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

