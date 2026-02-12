from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from edutracker.api.deps.deps import get_db
from edutracker.infrastructure.repositories.schedule_records import ScheduleRecordRepository
from edutracker.schemas.schedule_records import ScheduleRecordOut


router = APIRouter(tags=["schedule_records"])


@router.get("/schedule_records", response_model=list[ScheduleRecordOut])
def list_teacher_loads(db: Session = Depends(get_db)):
    return ScheduleRecordRepository.list(db)
    