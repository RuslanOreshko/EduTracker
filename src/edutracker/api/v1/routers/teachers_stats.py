from datetime import date
from fastapi import APIRouter, Depends, Query

from edutracker.api.deps.stats import get_stats_servise
from edutracker.application.services.teacher_stats_service import TeacherStatsService
from edutracker.api.v1.schemas.teachers_stats import ScheduleRecordOut

from edutracker.application.filters.subject import SubjectFilter
from edutracker.application.filters.group import GroupFilter


router = APIRouter(tags=["schedule_records"])

@router.get("/teacher", response_model=ScheduleRecordOut)
def teacher_stats(
    teacher: str = Query(..., min_length=2),
    date_from: date = Query(...),
    date_to: date = Query(...),

    subject: str | None = Query(None),
    group: str | None = Query(None),

    split_teachers_by_slash: bool = Query(True),

    service: TeacherStatsService = Depends(get_stats_servise),
):
    filters = []

    if subject:
        filters.append(SubjectFilter(subject))
    if group:
        filters.append(GroupFilter(group))

    return service.teacher_stats(
        teacher=teacher,
        date_from=date_from,
        date_to=date_to,
        split_teachers_by_slash=split_teachers_by_slash,
        filters=filters,
    )
