from datetime import date, timedelta
from collections import Counter
from typing import Optional

from edutracker.application.services.teacher_stats_service import TeacherStatsService
from edutracker.api.v1.schemas.peak_load import (
    TeacherPeakLoadOut, PeakDayOut, PeakWeekOut, PeakMonthOut
)


class TeacherPeakLoadService:
    def __init__(self, stats_service: TeacherStatsService):
        self._stats = stats_service

    def peak_load(
        self,
        teacher: str,
        date_from: date,
        date_to: date,
        split_teacher_by_slash: bool = True,
    ) ->    TeacherPeakLoadOut:
        # Повертаємо статистику викладача
        stats = self._stats.teacher_stats(
            teacher=teacher,
            date_from=date_from,
            date_to=date_to,
            split_teachers_by_slash=split_teacher_by_slash,
        )

        by_date = stats.by_date
        if not by_date:
            return TeacherPeakLoadOut(
                teacher=teacher,
                date_from=date_from,
                date_to=date_to,
                peak_day=None,
                peak_week=None,
                peak_month=None,
            )
        
        # Піковий день
        peak_day_date = max(by_date, key=lambda d: by_date[d])
        peak_day_val = float(by_date[peak_day_date])

        # Піковий тиждень
        week_totals: Counter[tuple[int, int]] = Counter()
        for d, v in by_date.items():
            y, w, _ = d.isocalendar()
            week_totals[(y, w)] += float(v)

        peak_week_key = max(week_totals, key=lambda k: week_totals[k])
        peak_week_val = float(week_totals[peak_week_key])

        peak_week_year, peak_week_num = peak_week_key
        week_start = self._iso_week_start(peak_week_year, peak_week_num)
        week_end = week_start + timedelta(days=6)

        # Піковий місяць
        month_totals: Counter[tuple[int, int]] = Counter()
        for d, v in by_date.items():
            month_totals[(d.year, d.month)] += float(v)
        
        peak_month_key = max(month_totals, key=lambda m: month_totals[m])
        peak_month_val = float(month_totals[peak_month_key])
        peak_month_year, peak_month_num = peak_month_key

        return TeacherPeakLoadOut(
            teacher=teacher,
            date_from=date_from,
            date_to=date_to,
            peak_day=PeakDayOut(date=peak_day_date, total_lessons=round(peak_day_val, 2)),
            peak_week=PeakWeekOut(
                year=peak_week_year,
                week=peak_week_num,
                date_from=week_start,
                date_to=week_end,
                total_lessons=round(peak_week_val, 2),
            ),
            peak_month=PeakMonthOut(
                year=peak_month_year,
                month=peak_month_num,
                total_lessons=round(peak_month_val, 2),
            ),
        )

    def _iso_week_start(self, year: int, week: int) -> date:
        return date.fromisocalendar(year, week, 1)
