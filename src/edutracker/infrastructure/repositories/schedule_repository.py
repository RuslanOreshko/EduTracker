from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from edutracker.infrastructure.db.models import ScheduleRecord
from edutracker.application.interfaces.schedule_repository import IScheduleRepository, ScheduleDayRawRow



class ScheduleRepository(IScheduleRepository):
    def __init__(self, db: Session):
        self._db = db

    def get_days_in_range(self, date_from: date, date_to: date) -> list[ScheduleDayRawRow]:
        stmt = (
            select(
                ScheduleRecord.schedule_date,
                ScheduleRecord.schedule_type,
                ScheduleRecord.schedule_for_teachers,
            )
            .where(ScheduleRecord.schedule_date.between(date_from, date_to))
            .order_by(ScheduleRecord.schedule_date.asc())
        )

        rows = (self._db.execute(stmt)).all()

        result: list[ScheduleDayRawRow] = []
        for schedule_date, schedule_type, schedule_for_teachers in rows:
            result.append(
                ScheduleDayRawRow(
                    schedule_date=schedule_date,
                    schedule_type=schedule_type,
                    schedule_for_teachers_raw=schedule_for_teachers,
                )
            )
        return result
        
        