from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from edutracker.infrastructure.db.models import ScheduleRecord

@dataclass(frozen=True)
class scheduleDayRow:
    schedule_date: date
    schedule_type: Optional[str]
    schedule_for_groups: dict


class ScheduleRepository:
    def __init__(self, db: Session):
        self._db = db

    def get_days_in_range(self, date_from: date, date_to: date) -> list[scheduleDayRow]:
        stmt = (
            select(
                ScheduleRecord.schedule_date,
                ScheduleRecord.schedule_type,
                ScheduleRecord.schedule_for_groups,
            )
            .where(ScheduleRecord.schedule_date.between(date_from, date_to))
            .order_by(ScheduleRecord.schedule_date.asc())
        )

        rows = (self._db.execute(stmt)).all()

        result: list[scheduleDayRow] = []

        for schedule_date, scheduele_type, schedule_for_groups in rows:
            if not schedule_for_groups:
                continue

            sfg = schedule_for_groups
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
                    schedule_for_groups=sfg,
                )
            )
        return result
        