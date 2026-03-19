from pathlib import Path

from edutracker.core.config import settings
from edutracker.infrastructure.remote.local_file_fetcher import LocalFileFetcher
from edutracker.infrastructure.remote.sqlite_file_validator import SQLiteFileValidator

class ScheduleSyncService:
    def __init__(
        self, 
        fetcher: LocalFileFetcher,
        validator: SQLiteFileValidator
    ):
        self._fetcher = fetcher
        self._validator = validator

        self._remote_path = Path(settings.SCHEDULE_REMOTE_DB_PATH)
        self._current_path = Path(settings.SCHEDULE_LOCAL_CACHE_PATH)
        self._prev_path = Path(settings.SCHEDULE_LOCAL_PREV_PATH)
        self._tmp_path = Path(settings.SCHEDULE_LOCAL_TMP_PATH)

    def sync_now(self) -> Path:
        
        self._cleanup_tmp_if_exist()

        self._fetcher.fetch(
            source_path=self._remote_path,
            destination_path=self._tmp_path,
        )

        self._rotate_files()

        return self._current_path
    
    def _cleanup_tmp_if_exist(self) -> None:
        if self._tmp_path.exists():
            self._tmp_path.unlink()

    def _rotate_files(self) -> None:
        self._current_path.parent.mkdir(parents=True, exist_ok=True)

        if self._prev_path.exists():
            self._prev_path.unlink()

        if self._current_path.exists():
            self._current_path.replace(self._prev_path)

        self._tmp_path.replace(self._current_path)