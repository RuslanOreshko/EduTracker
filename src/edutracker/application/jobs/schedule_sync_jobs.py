import logging

from edutracker.application.services.schedule_sync_service import ScheduleSyncService
from edutracker.infrastructure.remote.init import build_schedule_fetcher
from edutracker.infrastructure.remote.sqlite_file_validator import SQLiteFileValidator

logger = logging.getLogger(__name__)


def build_schedule_sync_service() -> ScheduleSyncService:
    return ScheduleSyncService(
        fetcher=build_schedule_fetcher(),
        validator=SQLiteFileValidator(),
    )


def run_schedule_sync() -> None:
    service = build_schedule_sync_service()

    try:
        service.ensure_fresh_copy()
    except Exception:
        logger.exception("Background schedule sync failed")
