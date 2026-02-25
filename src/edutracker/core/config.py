from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from pathlib import Path

# 3 для підключення тестової бд із завантажень
# 1 для продакш бд яка використовується
BASE_DIR = Path(__file__).resolve().parents[3] 

class Settings(BaseSettings):
    # конфіги для підключення до бд
    DB_PATH: Path = BASE_DIR / "data"  / "edutracker.sqlite3"
    AUTH_DB_PATH: Path = BASE_DIR / "data" / "auth.sqlite3"
    DEBUG: bool = True

    # Конфіги для авторизації
    AUTH_ALLOWED_DOMAIM: str = "rcit.ukr.education"
    JWT_ACCESS_TLL_MIN: int = 15
    REFRESH_TLL_DAYS: int = 30
    
    # секретний ключ із токеном
    JWT_SECRET: str = Field(..., validation_alias="JWT_SECRET")
    JWT_ALG: str = Field("HS256", validation_alias="JWT_ALG")

    model_config = SettingsConfigDict(
        env_file= BASE_DIR / ".env",
        extra="ignore",
    )

settings = Settings()
