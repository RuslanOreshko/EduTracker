from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from edutracker.core.config import settings


engine = create_engine(
    f"sqlite:///{settings.TEACHER_CATALOG_DB_PATH}",
    connect_args={"check_same_thread": False},
)

TeacherSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

