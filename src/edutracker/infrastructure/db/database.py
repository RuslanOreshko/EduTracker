from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine

from edutracker.core.config import settings


# Маршрутизатор посилань до бд
def build_engine(*, readonly: bool) -> str:
    db_path = Path(settings.DB_PATH)

    if readonly:
        if not db_path.exists():
            raise FileNotFoundError(f"SQLite DB file not found: {db_path}")
        url = f"sqlite+pysqlite:///file:{db_path.as_posix()}?mode=ro"
        connect_args = {"check_same_thread": False, "uri": True}
    else:
        url = f"sqlite+pysqlite:///{db_path.as_posix()}"
        connect_args = {"check_same_thread": False}

    return create_engine(
        url,
        connect_args=connect_args,
        pool_pre_ping=True
    )


def create_session_local(*, readonly: bool):
    engine = build_engine(readonly=readonly)
    return sessionmaker(bind=engine, autoflush=False, autocommit=False)