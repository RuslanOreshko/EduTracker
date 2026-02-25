from pathlib import Path
import sqlite3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine

from edutracker.core.config import settings


# Маршрутизатор посилань до бд
def build_engine(*, readonly: bool) -> Engine:
    db_path = Path(settings.DB_PATH).resolve()

    if readonly:
        if not db_path.exists():
            raise FileNotFoundError(f"SQLite DB file not found: {db_path}")
        
        sqlite_uri = f"file:{db_path.as_posix()}?mode=ro"

        def _creator():
            return sqlite3.connect(
                sqlite_uri,
                uri=True,
                check_same_thread=False,
            )
        
        return create_engine(
            "sqlite+pysqlite://",
            creator=_creator,
            pool_pre_ping=True
        )

    return create_engine(
            f"sqlite+pysqlite:///{db_path.as_posix()}",
            connect_args={"check_same_thread": False},
            pool_pre_ping=True
        )


def create_session_local(*, readonly: bool):
    engine = build_engine(readonly=readonly)
    return sessionmaker(bind=engine, autoflush=False, autocommit=False)