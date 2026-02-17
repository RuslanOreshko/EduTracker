from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Optional, Protocol   


@dataclass(frozen=True)
class scheduleDayRow:
    schedule_date: date
    schedule_type: Optional[str]
    schedule_for_teachers: dict


class IScheduleRepository(Protocol):
    def get_days_in_range(self, date_from: date, date_to: date) -> list[scheduleDayRow]:
        ...