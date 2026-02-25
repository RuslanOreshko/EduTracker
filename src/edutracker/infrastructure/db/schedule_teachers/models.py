from __future__ import annotations

from datetime import date, datetime
from sqlalchemy import DateTime, Integer, String, Date, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from edutracker.infrastructure.db.schedule_teachers.base import Base



class ScheduleRecord(Base):
    __tablename__ = "schedule_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    schedule_date: Mapped[Date] = mapped_column(Date, nullable=False)
    schedule_file_id: Mapped[str] = mapped_column(String, nullable=False)
    schedule_file_name: Mapped[str] = mapped_column(String, nullable=False)

    group_emails_list: Mapped[str | None] = mapped_column(Text, nullable=True)
    teachers_emails_list: Mapped[str | None] = mapped_column(Text, nullable=True)

    schedule_type: Mapped[str | None] = mapped_column(String, nullable=True)
    bell_type: Mapped[str | None] = mapped_column(String, nullable=True)

    schedule_for_groups: Mapped[str | None] = mapped_column(Text, nullable=True)
    schedule_for_teachers: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)


class RecentUsedRequests(Base):
    __tablename__ = "recent_used_requests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    requests: Mapped[str] = mapped_column(Text, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)