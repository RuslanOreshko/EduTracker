from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date

from edutracker.api.deps.get_database import get_db
from edutracker.application.services.stats.date_default import academic_year_start
from edutracker.infrastructure.repositories.schedule_repository import ScheduleRepository

from edutracker.application.services.teachers.peak_load_teacher_service import TeacherPeakLoadService
from edutracker.application.services.teachers.teacher_stats_service import TeacherStatsService
from edutracker.api.v1.schemas.peak_load import TeacherPeakLoadOut


router = APIRouter(prefix="/teachers", tags=["Teachers"])

@router.get("/teacher/peak-load", response_model=TeacherPeakLoadOut)
def teacher_peak_load(
    teacher: str = Query(...),

    date_from: date | None = Query(default=None),
    date_to: date | None = Query(default=None),

    db: Session = Depends(get_db)
) -> TeacherPeakLoadOut:
    date_to = date_to or date.today()
    date_from = date_from or academic_year_start(date_to)

    repo = ScheduleRepository(db)
    stats = TeacherStatsService(repo)
    service = TeacherPeakLoadService(stats)

    return service.peak_load(
        teacher=teacher,
        date_from = date_from,
        date_to = date_to,
        split_teacher_by_slash=True,
    )
