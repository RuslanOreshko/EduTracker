from fastapi import Depends
from sqlalchemy.orm import Session

from edutracker.api.deps.deps import get_db
from edutracker.infrastructure.repositories.schedule_records import ScheduleRepository
from edutracker.application.services.teacher_stats_service import TeacherStatsService



def get_schedule_repo(db: Session = Depends(get_db)) -> ScheduleRepository:
     return ScheduleRepository(db)


def get_stats_servise(
        repo: ScheduleRepository = Depends(get_schedule_repo),
) -> TeacherStatsService:
    return TeacherStatsService(repo)