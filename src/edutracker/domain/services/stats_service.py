from collections import Counter, defaultdict
from datetime import date
from typing import Optional

from edutracker.infrastructure.repositories.schedule_records import ScheduleRepository
from edutracker.schemas.schedule_records import ScheduleRecordOut

class StatsService:
    def __init__(self, schedule_repo: ScheduleRepository):
        self._schedule_repo = schedule_repo

    def teacher_stats(
        self,
        teacher: str,
        date_from: date,
        date_to: date,
        split_teachers_by_slash: bool = False,
    ) -> ScheduleRecordOut:
        days = self._schedule_repo.get_days_in_range(date_from, date_to)  

        by_date = Counter()
        by_group = Counter()
        by_subject = Counter()
        schedule_type_brakdown = Counter()
        total = 0

        teacher_norm = self._norm(teacher)

        for day in days:
            if day.schedule_type:
                schedule_type_brakdown[day.schedule_type] += 1 

            sfg = day.schedule_for_groups

            for group_key, group_payload in (sfg or {}).items():
                for weekday, wd_payload in (group_payload or {}).items():
                    if weekday == "email":
                        continue
                    lessons = (wd_payload or {}).get("lessons") or []

                    for lesson in lessons:
                        tname = (lesson or {}).get("teacher_name")
                        if not tname:
                            continue

                        if self._teacher_match(tname, teacher_norm, split_teachers_by_slash):
                            total += 1
                            by_date[day.schedule_date] += 1

                            group_name = (lesson or {}).get("group_name") or group_key
                            by_group[group_name] += 1

                            subject = (lesson or {}).get("lesson_name") or "—"
                            by_subject[subject] += 1

        return ScheduleRecordOut(
            teacher=teacher,
            date_from=date_from,
            date_to=date_to,
            total_lessons=total,
            by_date=dict(by_date),
            by_group=dict(by_group),
            by_subject=dict(by_subject),
            schedule_type_breakdown=dict(schedule_type_brakdown) if schedule_type_brakdown else None,
        )

    def _norm(self, s: str) -> str:
        return " ".join(s.lower().replace("’", "'").split())

    def _teacher_match(self, raw_teacher_name: str, teacher_norm: str, split_by_slash: bool) -> bool:
        raw_norm = self._norm(raw_teacher_name)
        if not split_by_slash:
            return teacher_norm == raw_norm or teacher_norm in raw_norm

        parts = [self._norm(p) for p in raw_teacher_name.split("/") if p.strip()]
        return any(teacher_norm == p or teacher_norm in p for p in parts)
