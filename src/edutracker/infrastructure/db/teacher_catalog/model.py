from datetime import datetime
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from edutracker.infrastructure.db.teacher_catalog.base import TeacherBase


class Teacher(TeacherBase):
    __tablename__ = "teachers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    display_name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    name_norm: Mapped[str] = mapped_column(String, nullable=False, index=True)
    search_key: Mapped[str] = mapped_column(String, nullable=False, index=True)
    email: Mapped[str | None] = mapped_column(String, nullable=True)
    last_seen_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)