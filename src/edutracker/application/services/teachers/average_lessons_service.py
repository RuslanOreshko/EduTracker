from collections import Counter
from datetime import date
from typing import Optional

import logging

from edutracker.application.interfaces.schedule_repository import IScheduleRepository
from edutracker.application.services.stats import LessonExtractor, TeacherMatcher, TeacherShareCalculator
from edutracker.application.common.split_teacher import SplitTeacher

from edutracker.application.services.stats import ScheduleDayProvider
from edutracker.infrastructure.parsers.schedule_json_parser import ScheduleJsonParser

from edutracker.application.dto.average_lessons_result import AverageLessonsResult

from edutracker.application.common.logging_utils import log_requested, log_computed

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
        self._share_calc = TeacherShareCalculator(self._matcher)

    def average_per_workday(
        self,
        date_from: date,
        date_to: date,
        teacher: Optional[str] = None,
        split_teachers_by_slash: bool = True, 
    ) -> AverageLessonsResult:
        action = "Average lessons per workday"

        log_requested(
            logger,
            action,
            date_from=str(date_from),
            date_to=str(date_to),
            teacher=teacher,
            split_by_slash=split_teachers_by_slash,
        )

        days = self._days.get_days(date_from, date_to)

        workdays_seen: set[date] = set()
        seen: set[tuple] = set()

        lessons_scanned = 0
        lessons_after_dedup = 0

        if teacher:
            teacher_norm = self._matcher.norm(teacher)
            total = 0.0

            for day in days:
                weekday = day.schedule_date.strftime("%A")
                if weekday not in WORKDAYS:
                    continue

                workdays_seen.add(day.schedule_date)

                for lesson in self._extractor.extract(day, weekday=weekday):
                    lessons_scanned += 1

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
                    lessons_after_dedup += 1

                    teacher_field = (lesson or {}).get("teacher_name") or ""
                    share = self._share_calc.calc(
                        teacher_field=teacher_field,
                        teacher_norm=teacher_norm,
                        split_by_slash=split_teachers_by_slash,
                    )
                    if share <= 0:
                        continue

                    total += share

            wd_count = len(workdays_seen)
            avg = (total / wd_count) if wd_count else 0.0

            log_computed(
                logger,
                action,
                date_from=str(date_from),
                date_to=str(date_to),
                teacher=teacher,
                workdays_count=wd_count,
                lessons_scanned=lessons_scanned,
                lessons_after_dedup=lessons_after_dedup,
                total=round(total, 2),
                avg_lessons=round(avg, 2),
            )

            return AverageLessonsResult(
                date_from=date_from,
                date_to=date_to,
                teacher=teacher,
                avg_lessons_per_workday=round(avg, 2),
                workdays_count=wd_count,
                total_lessons=round(total, 2),
            )

        totals = Counter()

        for day in days:
            weekday = day.schedule_date.strftime("%A")
            if weekday not in WORKDAYS:
                continue

            workdays_seen.add(day.schedule_date)

            for lesson in self._extractor.extract(day, weekday=weekday):
                lessons_scanned += 1

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
                lessons_after_dedup += 1

                teacher_field = (lesson or {}).get("teacher_name")
                for t_norm, share in self._split_teacher.split_teacher(teacher_field):
                    totals[t_norm] += share

        wd_count = len(workdays_seen)

        if wd_count == 0 or not totals:
            log_computed(
                logger,
                action,
                date_from=str(date_from),
                date_to=str(date_to),
                teacher=None,
                workdays_count=wd_count,
                lessons_scanned=lessons_scanned,
                lessons_after_dedup=lessons_after_dedup,
                total=0.0,
                avg_lessons=0.0,
            )
            return AverageLessonsResult(
                date_from=date_from,
                date_to=date_to,
                teacher=None,
                avg_lessons_per_workday=0.0,
                workdays_count=wd_count,
                total_lessons=0.0,
            )

        per_teacher_avgs = [float(total) / wd_count for total in totals.values()]
        avg_all = sum(per_teacher_avgs) / len(per_teacher_avgs)
        total_all = sum(float(x) for x in totals.values())

        log_computed(
            logger,
            action,
            date_from=str(date_from),
            date_to=str(date_to),
            teacher=None,
            workdays_count=wd_count,
            lessons_scanned=lessons_scanned,
            lessons_after_dedup=lessons_after_dedup,
            total=round(total_all, 2),
            avg_lessons=round(avg_all, 2),
        )

        return AverageLessonsResult(
            date_from=date_from,
            date_to=date_to,
            teacher=None,
            avg_lessons_per_workday=round(avg_all, 2),
            workdays_count=wd_count,
            total_lessons=round(total_all, 2),
        )   