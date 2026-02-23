from __future__ import annotations

from datetime import date
from typing import Protocol

from edutracker.application.dto.schedule_day import ScheduleDayRawRow

class IScheduleRepository(Protocol):
    def get_days_in_range(
            self, 
            date_from: date, 
            date_to: date
        ) -> list[ScheduleDayRawRow]:
        ...