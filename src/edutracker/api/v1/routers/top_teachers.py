from datetime import date
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from edutracker.api.v1.schemas.top_teachers import TopTacherItem, TopTeachersOut
from edutracker.application.services.stats.date_default import academic_year_start
from edutracker.application.services.top_teachers_service import TopTeachersService
from edutracker.infrastructure.repositories.schedule_records import ScheduleRepository
from edutracker.api.deps.deps import get_db


router = APIRouter(prefix="/top-teacher", tags=["TopTeachers"])


@router.get("/teachers/top", response_model=TopTeachersOut)
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
    
    

