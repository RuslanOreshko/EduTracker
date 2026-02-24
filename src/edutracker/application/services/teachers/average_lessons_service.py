from collections import Counter
from datetime import date
from typing import Optional

import logging

from edutracker.application.interfaces.schedule_repository import IScheduleRepository

from edutracker.application.services.stats.lesson_extractor import LessonExtractor
from edutracker.application.services.stats.teacher_matcher import TeacherMatcher
from edutracker.application.common.split_teacher import SplitTeacher

from edutracker.application.services.stats.schedule_days_provider import ScheduleDayProvider
from edutracker.infrastructure.parsers.schedule_json_parser import ScheduleJsonParser

logger = logging.getLogger(__name__)

WORKDAYS = {"Monday", "Tuesday", "Wednesday", "Thursday", "Friday"}

class AverageLessonsService:
    def __init__(self, schedule_repo: IScheduleRepository):
        self._repo = schedule_repo
        self._parser = ScheduleJsonParser()
        self._days = ScheduleDayProvider(self._repo, self._parser)

        self._extractor = LessonExtractor()
        self._matcher = TeacherMatcher()
        self._split_teacher = SplitTeacher(self._matcher)

    def average_per_workday(
        self,
        date_from: date,
        date_to: date,
        teacher: Optional[str] = None,
    ) -> dict:
        # лог про початок роботи сервісу
        logger.info(
            "Average lessons requested",
            extra={
                "teacher": teacher,
                "date_from": str(date_from),
                "date_to": str(date_to),
            },
        )

        days = self._days.get_days(date_from, date_to)

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
            logger.info(
                "Average lessons break",
                extra={
                    "teacher": teacher,
                    "avg_lessons": 0.0,
                },
            )

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
            logger.info(
                "Average lessons break",
                extra={
                    "teacher": teacher,
                    "avg_lessons": 0.0,
                },
            )

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
            logger.info(
                "Average lessons break",
                extra={
                    "teacher": teacher,
                    "avg_lessons": 0.0,
                },
            )

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

        logger.info(
            "Average lessons computed",
            extra={
                "teacher": teacher,
                "avg_lessons": avg_all,
                "workdays": workdays_seen,
            },
        )

        return {
            "date_from": date_from,
            "date_to": date_to,
            "teacher": None,
            "awg_lessons_per_workday": round(avg_all, 2),
            "workdays_count": wd_count,
            "total": round(total_all, 2),
        }
