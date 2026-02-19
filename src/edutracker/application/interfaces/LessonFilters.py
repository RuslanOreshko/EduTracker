from __future__ import annotations
from typing import Protocol, Any
from datetime import date

class ILessonFilter(Protocol):
    def match(
        self,
        *,
        lesson: dict[str, Any],
        schedule_date: date,
        schedule_type: str | None,
        weekday: str,
    ) -> bool:
        ...