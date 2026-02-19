from collections import Counter
from datetime import date
from typing import Any

from edutracker.application.interfaces.schedule_repository import IScheduleRepository
from edutracker.api.v1.schemas.schedule_records import ScheduleRecordOut
from edutracker.application.interfaces.LessonFilters import ILessonFilter

class StatsService:
    def __init__(self, schedule_repo: IScheduleRepository):
        self._schedule_repo = schedule_repo

    def teacher_stats(
        self,
        teacher: str,
        date_from: date,
        date_to: date,
        split_teachers_by_slash: bool = False,
        filters: list[ILessonFilter] | None = None, 
    ) -> ScheduleRecordOut:
        days = self._schedule_repo.get_days_in_range(date_from, date_to)  

        by_date = Counter()
        by_group = Counter()
        by_subject = Counter()
        schedule_type_brakdown = Counter()
        total = 0

        teacher_norm = self._norm(teacher)
        filters = filters or []

        for day in days:
            if day.schedule_type:
                schedule_type_brakdown[day.schedule_type] += 1 

            sfg = day.schedule_for_teachers or {}
            weekday = day.schedule_date.strftime("%A")

            for teacher_key, teacher_payload in sfg.items():
                if not isinstance(teacher_payload, dict):
                    continue

                day_block = teacher_payload.get(weekday)
                if not isinstance(day_block, dict):
                    continue

                lessons = day_block.get("lessons") or []
                if not lessons:
                    continue

                for lesson in lessons:
                    tneme = (lesson or{}).get("teacher_name")
                    if not tneme:
                        continue

                    share = self._calc_teacher_share(
                        teacher_field=tneme,
                        teacher_norm=teacher_norm,
                        split_by_slash=split_teachers_by_slash,
                    )

                    if share <= 0:
                        continue

                    # Місце застосування фільтрів
                    if not all(
                        f.match(
                            lesson=lesson,
                            schedule_date=day.schedule_date,
                            schedule_type=day.schedule_type,
                            weekday=weekday,
                        )
                        for f in filters
                    ):
                        continue
                    
                    total += share
                    by_date[day.schedule_date] += share
                    
                    group_name = (lesson or{}).get("group_name") or "-"
                    by_group[group_name] += share

                    subject = (lesson or {}).get("lesson_name") or "-"
                    by_subject[subject] += share


        return ScheduleRecordOut(
            teacher=teacher,
            date_from=date_from,
            date_to=date_to,
            total_lessons=round(total, 2),
            by_date=self._round_dict(dict(by_date)),
            by_group=self._round_dict(dict(by_group)),
            by_subject=self._round_dict(dict(by_subject)),
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



    # Одне зайняття може вести один із двох вчителів
    # в такому випадку буде зараховано по 0.5 балів кожному із них.
    # Метод для повернення частки уроку викладачеві.
    def _calc_teacher_share(self, teacher_field: str, teacher_norm: str, split_by_slash: bool) -> float:
        if not teacher_field:
            return 0.0

        if not split_by_slash:
            return 1.0 if self._teacher_match(teacher_field, teacher_norm, split_by_slash=False) else 0.0

        # Рахує кількість вчителів які можуть вести одну пару.
        parts = [self._norm(p) for p in teacher_field.split("/") if p.strip()]
        if not parts:
            return 0.0

        matched = any(teacher_norm == p or teacher_norm in p for p in parts)
        if not matched:
            return 0.0

        # 1 ділиться на кількість викладачів які ведуть можуть вести одну пару.
        return 1.0 / len(parts)

    # Заукруглення результату
    def _round_dict(self, d: dict, ndigits: int = 2) -> dict:
        return {k:round(v, ndigits) for k, v in d.items()}
    


