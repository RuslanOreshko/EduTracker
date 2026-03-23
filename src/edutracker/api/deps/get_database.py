from collections.abc import Generator
from sqlalchemy.orm import Session

from edutracker.infrastructure.db.schedule_teachers.database import create_session_local



def get_db() -> Generator[Session, None, None]:
    SessionLocal = create_session_local(readonly=True)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


