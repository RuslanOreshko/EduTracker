from edutracker.application.dto.peak_day_result import TeacherPeakLoadResult
from edutracker.api.v1.schemas.peak_load import TeacherPeakLoadOut, PeakDayOut, PeakWeekOut, PeakMonthOut


def to_schema(result: TeacherPeakLoadResult) -> TeacherPeakLoadOut:
    return TeacherPeakLoadOut(
        teacher=result.teacher,
        date_from=result.date_from,
        date_to=result.date_to,
        peak_day=PeakDayOut(date=result.peak_day.date, total_lessons=result.peak_day.total_lessons) if result.peak_day else None,
        peak_week=PeakWeekOut(
            year=result.peak_week.year,
            week=result.peak_week.week,
            date_from=result.peak_week.date_from,
            date_to=result.peak_week.date_to,
            total_lessons=result.peak_week.total_lessons,
        ) if result.peak_week else None,
        peak_month=PeakMonthOut(
            year=result.peak_month.year,
            month=result.peak_month.month,
            total_lessons=result.peak_month.total_lessons,
        ) if result.peak_month else None,
    )