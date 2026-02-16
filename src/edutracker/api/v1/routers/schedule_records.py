from datetime import date
from fastapi import APIRouter, Depends, Query

from edutracker.api.deps.stats import get_stats_servise
from edutracker.domain.services.stats_service import StatsService
from edutracker.schemas.schedule_records import ScheduleRecordOut

router = APIRouter(tags=["schedule_records"])

@router.get("/teacher", response_model=ScheduleRecordOut)
def teacher_stats(
    teacher: str = Query(..., min_length=2),
    date_from: date = Query(...),
    date_to: date = Query(...),
    service: StatsService = Depends(get_stats_servise),
):
    return service.teacher_stats(
        teacher=teacher,
        date_from=date_from,
        date_to=date_to,
    )
