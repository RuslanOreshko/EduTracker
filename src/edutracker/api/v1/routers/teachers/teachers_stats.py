from datetime import date
from fastapi import APIRouter, Depends, Query

from edutracker.api.deps.stats import get_stats_servise
from edutracker.application.services.teachers.teacher_stats_service import TeacherStatsService
from edutracker.api.v1.schemas.teachers_stats import ScheduleRecordOut

from edutracker.application.filters.subject import SubjectFilter
from edutracker.application.filters.group import GroupFilter

from edutracker.application.services.stats.date_default import academic_year_start


router = APIRouter(prefix="/teachers",tags=["Teachers"])

@router.get("/teacher", response_model=ScheduleRecordOut)
def teacher_stats(
    teacher: str = Query(..., min_length=2),
    date_from: date | None = Query(default=None),
    date_to: date | None = Query(default=None),

    subject: str | None = Query(None),
    group: str | None = Query(None),

    split_teachers_by_slash: bool = Query(True),

    service: TeacherStatsService = Depends(get_stats_servise),
):
    # Якщо не вказана дата вручну, тоді викликається метод academic_year_start
    # Він повератє дату від початку навчального року
    date_to = date_to or date.today()
    date_from = date_from or academic_year_start(date_to)

    filters = []

    if subject:
        filters.append(SubjectFilter(subject))
    if group:
        filters.append(GroupFilter(group))

    result = service.teacher_stats(
        teacher=teacher,
        date_from=date_from,
        date_to=date_to,
        split_teachers_by_slash=split_teachers_by_slash,
        filters=filters,
    )

    return ScheduleRecordOut(
        teacher=result.teacher,
        date_from=result.date_from,
        date_to=result.date_to,
        total_lessons=result.total_lessons,
        by_date=result.by_date,
        by_group=result.by_group,
        by_subject=result.by_subject,
        schedule_type_breakdown=result.schedule_type_breakdown,
    )   
