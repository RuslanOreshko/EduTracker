from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

# 3 для підключення тестової бд із завантажень
# 1 для продакш бд яка використовується
BASE_DIR = Path(__file__).resolve().parents[3] 

class Settings(BaseSettings):
    DB_PATH: Path = BASE_DIR / "data"  / "edutracker.sqlite3"
    AUTH_DB_PATH: Path = BASE_DIR / "data" / "auth.sqlite3"
    DEBUG: bool = True

    model_config = SettingsConfigDict(
        env_file= BASE_DIR / ".env",
        extra="ignore",
    )

settings = Settings()