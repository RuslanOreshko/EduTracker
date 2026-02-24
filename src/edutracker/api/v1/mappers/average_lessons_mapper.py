from edutracker.application.dto.average_lessons_result import AverageLessonsResult
from edutracker.api.v1.schemas.avg_lessons_out import AvgLessonsOut


def to_schema(result: AverageLessonsResult) -> AvgLessonsOut:
    return AvgLessonsOut(
        date_from=result.date_from,
        date_to=result.date_to,
        teacher=result.teacher,
        awg_lessons_per_workday=result.avg_lessons_per_workday,
        workdays_count=result.workdays_count,
        total_lessons=result.total_lessons,
    )