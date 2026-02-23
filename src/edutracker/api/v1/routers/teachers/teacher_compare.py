from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date

from edutracker.application.services.stats import academic_year_start

from edutracker.api.deps.get_database import get_db

from edutracker.api.v1.schemas import TeacherCompareOut
from edutracker.infrastructure.repositories import ScheduleRepository
from edutracker.application.services.teachers import TeacherStatsService
from edutracker.application.services.teachers import TeacherCompareService


router = APIRouter(prefix="/teachers", tags=["Teachers"])

@router.get("/teacher/compare", response_model=TeacherCompareOut)
def compare_teachers(
    teacher_a: str = Query(...),
    teacher_b: str = Query(...),
    date_from: date | None = Query(default=None),
    date_to: date | None = Query(default=None),
    top_n: int = Query(default=5, ge=1, le=20),
    db: Session = Depends(get_db),
):
    date_to = date_to or date.today()
    date_from = date_from or academic_year_start(date_to)

    repo = ScheduleRepository(db)
    stats = TeacherStatsService(repo)
    cmp_service = TeacherCompareService(stats)

    data =  cmp_service.compare(
        teacher_a=teacher_a,
        teacher_b=teacher_b,
        date_from=date_from,
        date_to=date_to,
        top_n=top_n,
    )

    return data
