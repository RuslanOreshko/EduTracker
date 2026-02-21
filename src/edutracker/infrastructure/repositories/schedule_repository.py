from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from edutracker.infrastructure.db.models import ScheduleRecord
from edutracker.application.interfaces.schedule_repository import scheduleDayRow
from edutracker.application.interfaces.schedule_repository import IScheduleRepository



class ScheduleRepository(IScheduleRepository):
    def __init__(self, db: Session):
        self._db = db

    def get_days_in_range(self, date_from: date, date_to: date) -> list[scheduleDayRow]:
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

        result: list[scheduleDayRow] = []

        for schedule_date, scheduele_type, schedule_for_teachers in rows:
            if not schedule_for_teachers:
                continue

            sfg = schedule_for_teachers
            if isinstance(sfg, str):
                try:
                    sfg = json.loads(sfg)
                except json.JSONDecodeError:
                    continue

            if not isinstance(sfg, dict):
                continue

            result.append(
                scheduleDayRow(
                    schedule_date=schedule_date,
                    schedule_type=scheduele_type,
                    schedule_for_teachers=sfg,
                )
            )
        return result
        