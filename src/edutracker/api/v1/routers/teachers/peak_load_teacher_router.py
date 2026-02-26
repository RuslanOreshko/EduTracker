from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date

from edutracker.infrastructure.repositories import ScheduleRepository
from edutracker.application.services.teachers import TeacherPeakLoadService
from edutracker.application.services.teachers import TeacherStatsService
from edutracker.api.v1.schemas import TeacherPeakLoadOut
from edutracker.api.v1.mappers.peak_load_mapper import to_schema

from edutracker.api.deps.get_database import get_db
from edutracker.api.deps.permissions import required_roles
from edutracker.application.services.stats import academic_year_start


router = APIRouter(prefix="/teachers", tags=["Teachers"], dependencies=[Depends(required_roles("teacher", "admin"))])

@router.get("/teacher/peak-load", response_model=TeacherPeakLoadOut)
def teacher_peak_load(
    teacher: str = Query(..., min_length=2),

    date_from: date | None = Query(default=None),
    date_to: date | None = Query(default=None),

    db: Session = Depends(get_db)
) -> TeacherPeakLoadOut:
    date_to = date_to or date.today()
    date_from = date_from or academic_year_start(date_to)

    repo = ScheduleRepository(db)
    stats = TeacherStatsService(repo)
    service = TeacherPeakLoadService(stats)

    result = service.peak_load(
        teacher=teacher,
        date_from = date_from,
        date_to = date_to,
        split_teacher_by_slash=True,
    )
    return to_schema(result)
