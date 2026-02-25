from collections.abc import Generator
from sqlalchemy.orm import Session

from edutracker.infrastructure.db.Auth.auth_database import SessionLocal


def get_auth_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()