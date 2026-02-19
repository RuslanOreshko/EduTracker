from __future__ import annotations
from typing import Any
from datetime import date

from edutracker.application.interfaces.LessonFilters import ILessonFilter


class GroupFilter(ILessonFilter):
    def __init__(self, group: str):
        self._group = group.strip().lower()

    def match(
            self,
            *,
            lesson: dict[str, Any], 
            schedule_date: date, 
            schedule_type: str | None, 
            weekday: str
        ) -> bool:
        raw = (lesson.get("group_name") or "").lower()
        return self._group in raw
