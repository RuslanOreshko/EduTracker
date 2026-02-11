from datetime import date
from sqlalchemy import ForeignKey, CheckConstraint, Integer, String, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from edutracker.infrastructure.db.base import Base



class Teachers(Base):
    __tablename__ = "teachers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    loads: Mapped[list["TeacherLoad"]] = relationship(back_populates="teacher")


class Group(Base):
    __tablename__ = "groups"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    loads: Mapped[list["TeacherLoad"]] = relationship(back_populates="group")


class Subject(Base):
    __tablename__ = "subjects"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    loads: Mapped[list["TeacherLoad"]] = relationship(back_populates="subject")




class TeacherLoad(Base):
    __tablename__ = "teacher_load"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id"), nullable=False)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"), nullable=False)
    subjects_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"), nullable=False)

    period_start: Mapped[date] = mapped_column(Date, nullable=False)
    period_end: Mapped[date] = mapped_column(Date, nullable=False)

    planned_lessons: Mapped[int] = mapped_column(Integer, nullable=False)
    done_lessons: Mapped[int] = mapped_column(Integer, nullable=False)

    teacher: Mapped["Teachers"] = relationship(back_populates="loads")
    group: Mapped["Group"] = relationship(back_populates="loads")
    subject: Mapped["Subject"] = relationship(back_populates="loads")

    __table_args__ = (
        CheckConstraint("planned_lessons >= 0", name="ck_planned_nonneg"),
        CheckConstraint("done_lessons >= 0", name="ck_done_nonneg"),
        CheckConstraint("done_lessons  <= planned_lessons", name="ck_done_le_planned"),
        CheckConstraint("period_start <=period_end", name="ck_period_order"),
    )