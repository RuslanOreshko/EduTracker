from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from pathlib import Path
import os

# 3 для підключення тестової бд із завантажень
# 1 для продакш бд яка використовується
BASE_DIR = Path(__file__).resolve().parents[3] 

class Settings(BaseSettings):
    # конфіги для підключення до бд
    DB_PATH: Path = BASE_DIR / "data"  / "edutracker.sqlite3"
    AUTH_DB_PATH: Path = BASE_DIR / "data" / "auth.sqlite3"
    TEACHER_CATALOG_DB_PATH: Path = BASE_DIR / "data" / "teacher_catalog.sqlite3"
    DEBUG: bool = True

    # Конфіги для авторизації
    AUTH_ALLOWED_DOMAIM: str = "rcit.ukr.education"
    JWT_ACCESS_TLL_MIN: int = 15
    REFRESH_TLL_DAYS: int = 30
    
    # секретний ключ із токеном
    JWT_SECRET: str = Field(..., validation_alias="JWT_SECRET")
    JWT_ALG: str = Field("HS256", validation_alias="JWT_ALG")

    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID")

    # Синхронізація налаштувань розкладу
    SCHEDULE_SOURCE_MODE: str = "local"
    SCHEDULE_REMOTE_DB_PATH: Path = BASE_DIR / "fake_remote" / "schedule.sqlite3"
    SCHEDULE_LOCAL_CACHE_PATH: Path = BASE_DIR / "data" / "schedule_cache.sqlite3"
    SCHEDULE_LOCAL_PREV_PATH: Path = BASE_DIR / "data" / "schedule_cache.prev.sqlite3"
    SCHEDULE_LOCAL_TMP_PATH: Path = BASE_DIR / "data" / "schedule_cache.tmp.sqlite3"

    SCHEDULE_SYNC_ENABLED: bool = False
    SCHEDULE_SYNC_INTERVAL_HOURS: int = 24



    model_config = SettingsConfigDict(
        env_file= BASE_DIR / ".env",
        extra="ignore",
    )

settings = Settings()
