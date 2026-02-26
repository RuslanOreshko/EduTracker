from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date

from edutracker.infrastructure.repositories import ScheduleRepository
from edutracker.application.services.teachers import AverageLessonsService
from edutracker.api.v1.schemas import AvgLessonsOut

from edutracker.api.deps.get_database import get_db
from edutracker.api.deps.permissions import required_roles
from edutracker.application.services.stats import academic_year_start
from edutracker.api.v1.mappers.average_lessons_mapper import to_schema


router = APIRouter(prefix="/teachers", tags=["Teachers"], dependencies=[Depends(required_roles("teacher", "admin"))])


@router.get("/teacher/avg-per-workday", response_model=AvgLessonsOut)
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

    result = service.average_per_workday(date_from=date_from, date_to=date_to, teacher=teacher)

    return to_schema(result)
