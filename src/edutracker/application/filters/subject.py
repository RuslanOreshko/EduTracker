from __future__ import annotations
from typing import Any
from datetime import date

from edutracker.application.interfaces.LessonFilters import ILessonFilter


class SubjectFilter(ILessonFilter):
    def __init__(self, subject: str):
        self._subject = subject.strip().lower()

    def match(
            self,
            *,
            lesson: dict[str, Any], 
            schedule_date: date, 
            schedule_type: str | None, 
            weekday: str
        ) -> bool:
        name = (lesson.get("lesson_name") or "").strip().lower()
        return name == self._subject
