from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from edutracker.infrastructure.db.models import ScheduleRecord

class ScheduleRecordRepository:
    @staticmethod
    def list(db: Session) -> list[ScheduleRecord]:
        stmt = select(ScheduleRecord).order_by(ScheduleRecord.id)
        return db.execute(stmt).scalars().all()