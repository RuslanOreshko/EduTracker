from collections import Counter
from datetime import date
from typing import Optional

from edutracker.application.interfaces.schedule_repository import IScheduleRepository

from edutracker.application.services.stats.lesson_extractor import LessonExtractor
from edutracker.application.services.stats.teacher_matcher import TeacherMatcher
from edutracker.application.services.stats.split_teacher import SplitTeacher

WORKDAYS = {"Monday", "Tuesday", "Wednesday", "Thursday", "Friday"}

class AverageLessonsService:
    def __init__(self, schedule_repo: IScheduleRepository):
        self._repo = schedule_repo
        self._extractor = LessonExtractor()
        self._matcher = TeacherMatcher()
        self._split_teacher = SplitTeacher(self._matcher)

    def average_per_workday(
        self,
        date_from: date,
        date_to: date,
        teacher: Optional[str] = None,
    ) -> dict:
        days = self._repo.get_days_in_range(date_from, date_to)

        totals = Counter()
        workdays_seen: set[date] = set()

        seen: set[tuple] = set()

        for day in days:
            weekday = day.schedule_date.strftime("%A")
            if weekday not in WORKDAYS:
                continue

            workdays_seen.add(day.schedule_date)

            for lesson in self._extractor.extract(day, weekday=weekday):
                lesson_id = (
                    day.schedule_date,
                    str((lesson or {}).get("lesson_number") or "").strip(),
                    str((lesson or {}).get("group_name") or "").strip(),
                    str((lesson or {}).get("lesson_name") or "").strip(),
                    str((lesson or {}).get("classroom") or "").strip(),
                )

                if lesson_id in seen:
                    continue
                seen.add(lesson_id)

                teacher_field = (lesson or {}).get("teacher_name")
                for t_norm, share in self._split_teacher.split_teacher(teacher_field):
                    totals[t_norm] += share

        wd_count = len(workdays_seen)

        if wd_count == 0:
            return{
                "date_from": date_from,
                "date_to": date_to,
                "teacher": teacher,
                "awg_lessons_per_workday": 0.0,
                "workdays_count": 0,
                "total": 0.0,
            }
        
        # Якщо користувач вказав ім'я викладача, то поверне його статистику
        if teacher:
            t_norm = self._matcher.norm(teacher)
            total = float(totals.get(t_norm, 0.0))
            avg = total / wd_count
            return{
                "date_from": date_from,
                "date_to": date_to,
                "teacher": teacher,
                "awg_lessons_per_workday": round(avg, 2),
                "workdays_count": wd_count,
                "total": round(total, 2),
            }
        
        if not totals:
            return{
                "date_from": date_from,
                "date_to": date_to,
                "teacher": None,
                "awg_lessons_per_workday": 0.0,
                "workdays_count": wd_count,
                "total": 0.0,
            }
        
        per_teacher_avgs = [float(total) / wd_count for total in totals.values()]
        avg_all = sum(per_teacher_avgs) /  len(per_teacher_avgs)

        total_all = sum(float(x) for x in totals.values())

        return {
            "date_from": date_from,
            "date_to": date_to,
            "teacher": None,
            "awg_lessons_per_workday": round(avg_all, 2),
            "workdays_count": wd_count,
            "total": round(total_all, 2),
        }
