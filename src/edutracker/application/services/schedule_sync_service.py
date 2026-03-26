from pathlib import Path
from datetime import timedelta, datetime, timezone
from typing import Protocol
import logging

from edutracker.core.config import settings
from edutracker.infrastructure.remote.ssh_file_fetcher import SshFileFetcher
from edutracker.infrastructure.remote.sqlite_file_validator import SQLiteFileValidator

logger = logging.getLogger(__name__)


class ScheduleFileFetcher(Protocol):
    def fetch(self, source_path: Path, destination_path: Path) -> Path:
        ...


class ScheduleSyncService:
    def __init__(
        self, 
        fetcher: ScheduleFileFetcher,
        validator: SQLiteFileValidator
    ):
        self._fetcher = fetcher
        self._validator = validator

        self._remote_path = Path(settings.SCHEDULE_REMOTE_DB_PATH)
        self._current_path = Path(settings.SCHEDULE_LOCAL_CACHE_PATH)
        self._prev_path = Path(settings.SCHEDULE_LOCAL_PREV_PATH)
        self._tmp_path = Path(settings.SCHEDULE_LOCAL_TMP_PATH)

    def should_sync(self) -> bool:
        if not self._current_path.exists():
            logger.info("Schedule cache missing, sync required")
            return True
        
        if not self._is_valid_sqlite(self._current_path):
            logger.warning(
                "Current schedule cache is invalid, sync required",
                extra={"path": str(self._current_path)},
            )
            return True

        max_age = timedelta(hours=settings.SCHEDULE_SYNC_INTERVAL_HOURS)

        file_mtime = datetime.fromtimestamp(
            self._current_path.stat().st_mtime,
            tz=timezone.utc
        )

        now = datetime.now(timezone.utc)

        return (now - file_mtime) >= max_age

    

    def ensure_fresh_copy(self) -> Path:
        if self.should_sync():
            return self.sync_now()
        
        return self._current_path


    def has_valid_current_copy(self) -> bool:
        if not self._current_path.exists():
            return False
        
        return self._is_valid_sqlite(self._current_path)


    def sync_now(self) -> Path:
        logger.info(
            "Schedule sync started",
            extra={
                "remote_path": str(self._remote_path),
                "tmp_path": str(self._tmp_path),
                "current_path": str(self._current_path),
            },
        )

        self._cleanup_tmp_if_exists()

        try:
            self._fetcher.fetch(
                source_path=self._remote_path,
                destination_path=self._tmp_path
            )

            self._validator.validate(self._tmp_path)

            self._activate_valid_tmp()

            logger.info(
                "Schedule sync completed",
                extra={"current_path": str(self._current_path)},
            )

            return self._current_path
        
        except Exception:
            logger.exception("Schedule sync failed")
            self._cleanup_tmp_if_exists()
            raise
    


    def _is_valid_sqlite(self, path: Path) -> bool:
        try:
            self._validator.validate(path)
            return True
        except Exception:
            logger.exception("SQLite validation failed", extra={"path": str(path)})
            return False
    


    def _cleanup_tmp_if_exists(self) -> None:
        if self._tmp_path.exists():
            self._tmp_path.unlink()



    def _activate_valid_tmp(self) -> None:
        self._current_path.parent.mkdir(parents=True, exist_ok=True)

        if self._prev_path.exists():
            self._prev_path.unlink()

        moved_current_to_prev = False

        try:
            if self._current_path.exists():
                self._current_path.replace(self._prev_path)
                moved_current_to_prev = True

            self._tmp_path.replace(self._current_path)

        except Exception:
            if(
                moved_current_to_prev
                and self._prev_path.exists()
                and not self._current_path.exists()
            ):
                try:
                    self._prev_path.replace(self._current_path)
                    logger.warning("Schedule sync rollback completed")
                except Exception:
                    logger.exception("Schedule sync rollback failed")


            raise