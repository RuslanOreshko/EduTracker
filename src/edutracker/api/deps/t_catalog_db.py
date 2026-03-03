from sqlalchemy.orm import Session
from edutracker.infrastructure.db.teacher_catalog.session import TeacherSessionLocal


def get_teacher_catalog_db():
    db: Session = TeacherSessionLocal()
    try:
        yield db
    finally:
        db.close()