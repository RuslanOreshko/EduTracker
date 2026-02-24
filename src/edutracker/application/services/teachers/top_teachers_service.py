from datetime import date
from collections import Counter
import logging

from edutracker.application.interfaces.schedule_repository import IScheduleRepository

from edutracker.application.services.stats import LessonExtractor, TeacherMatcher
from edutracker.application.common.cleaner import ValueCleaner
from edutracker.application.common.split_teacher import SplitTeacher

from edutracker.application.services.stats import ScheduleDayProvider
from edutracker.infrastructure.parsers.schedule_json_parser import ScheduleJsonParser

from edutracker.application.dto.top_teachers_result import TopTeachersResult, TopTacherItem

from edutracker.application.common.logging_utils import log_requested, log_computed

logger = logging.getLogger(__name__)


class TopTeachersService:
    def __init__(self, schedule_repo: IScheduleRepository):
        self._repo = schedule_repo
        self._parser = ScheduleJsonParser()
        self._days = ScheduleDayProvider(self._repo, self._parser)

        self._matcher = TeacherMatcher()
        self._extractor = LessonExtractor()
        self._split_teacher = SplitTeacher(self._matcher)

    def top_teacher(
        self,
        date_from: date,
        date_to: date,
        limit: int = 5,
    ) -> list[tuple[str, float]]:
        # Лог про початок роботи сервісу
        log_requested(logger, "Top teacher", date_from=str(date_from), limit=limit)

        days = self._days.get_days(date_from, date_to)

        totals: Counter[str] = Counter()
        seen: set[tuple] = set()

        for day in days:
            weekday = day.schedule_date.strftime("%A")

            for lesson in self._extractor.extract(day, weekday=weekday):
                if not isinstance(lesson, dict):
                    continue

                lesson_id = (
                    day.schedule_date,
                    ValueCleaner.clean(lesson.get("lesson_number")),
                    ValueCleaner.clean(lesson.get("group_name")),
                    ValueCleaner.clean(lesson.get("lesson_name")),
                    ValueCleaner.clean(lesson.get("classroom")),
                )

                if lesson_id in seen:
                    continue
                seen.add(lesson_id)

                teacher_field = lesson.get("teacher_name")
                for teacher_norm, share in self._split_teacher.split_teacher(teacher_field):
                    totals[teacher_norm] += share


        top = totals.most_common(limit)

        # Лог про закінчення роботи сервісу
        log_computed(logger, "Top teacher", date_from=str(date_from), limit=limit)

        result = TopTeachersResult(
            date_from=date_from,
            date_to=date_to,
            top=[
                TopTacherItem(teacher=name, total_lessons=round(float(val), 2))
                for name, val in top
            ],
        )

        return result

    