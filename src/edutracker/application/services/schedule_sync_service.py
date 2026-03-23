from pathlib import Path
from datetime import timedelta, datetime, timezone

from edutracker.core.config import settings
from edutracker.infrastructure.remote.ssh_file_fetcher import SshFileFetcher
from edutracker.infrastructure.remote.sqlite_file_validator import SQLiteFileValidator

class ScheduleSyncService:
    def __init__(
        self, 
        fetcher: SshFileFetcher,
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