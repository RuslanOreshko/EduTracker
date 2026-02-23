from datetime import date
from collections import Counter

from edutracker.application.interfaces.schedule_repository import IScheduleRepository
from edutracker.application.dto.teacher_stats_result import TeacherStatsResult
from edutracker.application.interfaces.LessonFilters import ILessonFilter

from edutracker.application.services.stats.teacher_matcher import TeacherMatcher
from edutracker.application.services.stats.stats_aggregator import StatsAggregator
from edutracker.application.services.stats.lesson_extractor import LessonExtractor
from edutracker.application.services.stats.teacher_share_calculator import TeacherShareCalculator

from edutracker.application.services.stats.schedule_days_provider import ScheduleDayProvider
from edutracker.infrastructure.parsers.schedule_json_parser import ScheduleJsonParser

from edutracker.application.common.cleaner import ValueCleaner


class TeacherStatsService:
    def __init__(self, schedule_repo: IScheduleRepository):
        self._repo = schedule_repo
        self._parser = ScheduleJsonParser()
        self._days = ScheduleDayProvider(self._repo, self._parser)

        self._schedule_repo = schedule_repo
        self._matcher = TeacherMatcher()
        self._share_calc = TeacherShareCalculator(self._matcher)
        self._extractor = LessonExtractor()

    def teacher_stats(
        self,
        teacher: str,
        date_from: date,
        date_to: date,
        split_teachers_by_slash: bool = True,
        filters: list[ILessonFilter] | None = None 
    ) -> TeacherStatsResult:
        days = self._days.get_days(date_from, date_to)

        schedule_type_breakdown = Counter()
        agg = StatsAggregator(by_date=Counter(), by_group=Counter(), by_subject=Counter())
        teacher_norm = self._matcher.norm(teacher)
        filters = filters or []

        seen: set[tuple] = set()

        for day in days:
            if day.schedule_type:
                schedule_type_breakdown[day.schedule_type] += 1

            weekday = day.schedule_date.strftime("%A")

            for lesson in self._extractor.extract(day, weekday=weekday):
                teacher_field = (lesson or{}).get("teacher_name") or ""

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

                share = self._share_calc.calc(
                    teacher_field=teacher_field,
                    teacher_norm=teacher_norm,
                    split_by_slash=split_teachers_by_slash,
                )
                if share <= 0:
                    continue

                if not all(
                    f.match(
                        lesson=lesson,
                        schedule_date=day.schedule_date,
                        schedule_type=day.schedule_type,
                        weekday=weekday
                    )
                    for f in filters
                ):
                    continue

                agg.add(day.schedule_date, lesson, share)

        return TeacherStatsResult(
            teacher=teacher,
            date_from=date_from,
            date_to=date_to,
            total_lessons=round(agg.total, 2),
            by_date=self._round_dict(dict(agg.by_date)),
            by_group=self._round_dict(dict(agg.by_group)),
            by_subject=self._round_dict(dict(agg.by_subject)),
            schedule_type_breakdown=dict(schedule_type_breakdown) if schedule_type_breakdown else None
        )
    

    def _round_dict(self, d: dict, ndigits: int = 2) -> dict:
        return {k: round(v, ndigits) for k, v in d.items()}
