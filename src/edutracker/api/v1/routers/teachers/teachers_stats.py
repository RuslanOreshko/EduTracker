from datetime import date
from fastapi import APIRouter, Depends, Query

from edutracker.application.services.teachers import TeacherStatsService
from edutracker.api.v1.schemas import TeacherStatsOut
from edutracker.api.v1.mappers.stats_teachers_mapper import to_schema

from edutracker.api.deps.get_stats import get_stats_servise
from edutracker.application.services.stats import academic_year_start

from edutracker.application.filters.subject import SubjectFilter
from edutracker.application.filters.group import GroupFilter



router = APIRouter(prefix="/teachers",tags=["Teachers"])

@router.get("/teacher", response_model=TeacherStatsOut)
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

    return to_schema(result)  
