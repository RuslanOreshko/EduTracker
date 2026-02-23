from datetime import date
from collections import Counter

from edutracker.application.interfaces.schedule_repository import IScheduleRepository

from edutracker.application.services.stats.lesson_extractor import LessonExtractor
from edutracker.application.services.stats.teacher_matcher import TeacherMatcher
from edutracker.application.common.cleaner import ValueCleaner
from edutracker.application.services.stats.split_teacher import SplitTeacher




class TopTeachersService:
    def __init__(self, schedule_repo: IScheduleRepository):
        self._schedule_repo = schedule_repo
        self._matcher = TeacherMatcher()
        self._extractor = LessonExtractor()
        self._split_teacher = SplitTeacher(self._matcher)

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
        return [(name, round(val, 2)) for name, val in top]

    