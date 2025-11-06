# config.py
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"
print(f"🔎 Leyendo .env en: {ENV_PATH}  (existe={ENV_PATH.exists()})")

class Settings(BaseSettings):
    DATABASE_URL: str

    # Orígenes permitidos para el front
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ]

    # (Opcional) claves para auth si luego usamos JWT
    # JWT_SECRET: str | None = None
    # JWT_ALG: str = "HS256"
    # ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    model_config = SettingsConfigDict(
        env_file=str(ENV_PATH),
        env_file_encoding="utf-8",
    )

settings = Settings()
print("📦 DATABASE_URL cargada:", ("OK" if bool(settings.DATABASE_URL) else "VACÍA"))
print("🌐 CORS_ORIGINS:", settings.CORS_ORIGINS)
