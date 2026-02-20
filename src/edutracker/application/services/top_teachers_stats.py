
from datetime import date
from collections import Counter
from typing import Any

from edutracker.application.interfaces.schedule_repository import IScheduleRepository
from edutracker.application.services.stats.lesson_extractor import LessonExtractor
from edutracker.application.services.stats.teacher_matcher import TeacherMatcher



class TopTeachersStats:
    def __init__(self, schedule_repo: IScheduleRepository):
        self._schedule_repo = schedule_repo
        self._matcher = TeacherMatcher()
        self._extractor = LessonExtractor()

    def top_teacher(
        self,
        date_from: date,
        date_to: date,
        limit: int = 5,
    ) -> list[tuple[str, float]]:
        days = self._schedule_repo.get_days_in_range(date_from, date_to)

        totals: Counter[str] = Counter()
        seen: set[tuple] = set()

        for day in days:
            weekday = day.schedule_date.strftime("%A")

            for lesson in self._extractor.extract(day, weekday=weekday):
                if not isinstance(lesson, dict):
                    continue

                lesson_id = (
                    day.schedule_date,
                    self._clean(lesson.get("lesson_number")),
                    self._clean(lesson.get("group_name")),
                    self._clean(lesson.get("lesson_name")),
                    self._clean(lesson.get("classroom")),
                )

                if lesson_id in seen:
                    continue
                seen.add(lesson_id)

                teacher_field = lesson.get("teacher_name")
                for teacher_norm, share in self._split_teacher(teacher_field):
                    totals[teacher_norm] += share

        top = totals.most_common(limit)
        return [(name, round(val, 2)) for name, val in top]
 

    def _clean(self, v: Any) -> str:
        if v is None:
            return ""
        
        s = str(v).strip()

        if s.lower() == "none":
            return ""
        
        return s
    
    def _split_teacher(self, teacher_field: Any) -> list[tuple[str, float]]:
        if not teacher_field or not isinstance(teacher_field, str):
            return []
        
        parts_raw = [p.strip() for p in teacher_field.split("/") if p.strip()]
        if not parts_raw:
            return []
        
        parts_norm = [self._matcher.norm(p) for p in parts_raw]
        n = len(parts_norm)
        share = 1.0 / n

        out: list[tuple[str, float]] = []
        for p in parts_norm:
            out.append((p, share))
        
        return out