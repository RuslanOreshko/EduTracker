from fastapi import Depends
from sqlalchemy.orm import Session

from edutracker.api.deps.deps import get_db
from edutracker.infrastructure.repositories.schedule_records import ScheduleRepository
from edutracker.domain.services.stats_service import StatsService



def get_schedule_repo(db: Session = Depends(get_db)) -> ScheduleRepository:
     return ScheduleRepository(db)


def get_stats_servise(
        repo: ScheduleRepository = Depends(get_schedule_repo),
) -> StatsService:
    return StatsService(repo)