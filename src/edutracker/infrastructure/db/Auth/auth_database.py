from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from edutracker.core.config import settings


engine = create_engine(
    f"sqlite:///{settings.AUTH_DB_PATH}",
    connect_args={"check_same_thread": False},
    future=True,
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

def create_auth_session() -> Session:
    return SessionLocal()