from datetime import date
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from edutracker.api.v1.schemas import TopTacherItem, TopTeachersOut
from edutracker.application.services.stats import academic_year_start
from edutracker.api.deps.get_database import get_db

from edutracker.application.services.teachers import TopTeachersService
from edutracker.infrastructure.repositories import ScheduleRepository


router = APIRouter(prefix="/teachers", tags=["Teachers"])


@router.get("/teacher/top", response_model=TopTeachersOut)
def top_teachers(
    date_from: date | None = Query(default=None),
    date_to: date | None = Query(default=None),
    limit: int = Query(default=5, ge=1, le=50),
    db: Session = Depends(get_db)
) -> TopTeachersOut:
    date_to = date_to or date.today()
    date_from = date_from or academic_year_start(date_to)

    repo = ScheduleRepository(db)
    service = TopTeachersService(repo)

    top = service.top_teacher(date_from=date_from, date_to=date_to, limit=limit)

    return TopTeachersOut(
        date_from=date_from,
        date_to=date_to,
        top=[TopTacherItem(teacher=name, total_lessons=total) for name, total in top]
    )
    
    

