from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]

class Settings(BaseSettings):
    DB_PATH: Path = BASE_DIR / "infrastructure" / "db" / "edutracker.sqlite3"
    DEBUG: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

settings = Settings()