from edutracker.application.dto.teacher_stats_result import TeacherStatsResult
from edutracker.api.v1.schemas.teachers_stats import TeacherStatsOut


def to_schema(result: TeacherStatsResult) -> TeacherStatsOut:
    return TeacherStatsOut(
        teacher=result.teacher,
        date_from=result.date_from,
        date_to=result.date_to,
        total_lessons=result.total_lessons,
        by_date=result.by_date,
        by_group=result.by_group,
        by_subject=result.by_subject,
        schedule_type_breakdown=result.schedule_type_breakdown,
    )