from edutracker.infrastructure.db.teacher_catalog.session import TeacherSessionLocal


def get_teacher_db():
    db = TeacherSessionLocal()
    try:
        yield db
    finally:
        db.close()