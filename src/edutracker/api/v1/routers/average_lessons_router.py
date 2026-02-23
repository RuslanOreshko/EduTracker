from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date

from edutracker.infrastructure.repositories.schedule_repository import ScheduleRepository

from edutracker.api.deps.get_database import get_db
from edutracker.application.services.stats.date_default import academic_year_start
from edutracker.api.v1.schemas.avg_lessons_out import AvgLessonsOut

from edutracker.application.services.average_lessons_service import AverageLessonsService


router = APIRouter(prefix="/teachers", tags=["Teachers"])

@router.get("/teacher/avg-per-workday")
def avg_per_workday(
    teacher: str | None = Query(default=None),
    date_from: date | None = Query(default=None),
    date_to: date | None = Query(default=None),
    db: Session = Depends(get_db)
) -> AvgLessonsOut:
    date_to = date_to or date.today()
    date_from = date_from or academic_year_start(date_to)

    repo = ScheduleRepository(db)
    service = AverageLessonsService(repo)

    data = service.average_per_workday(date_from=date_from, date_to=date_to, teacher=teacher)

    return AvgLessonsOut(
        date_from=data["date_from"],
        date_to=data["date_to"],
        teacher=data["teacher"],
        awg_lessons_per_workday=data["awg_lessons_per_workday"],
        workdays_count=data["workdays_count"],
        total_lessons=data["total"],
    )
