from edutracker.application.services.schedule_sync_service import ScheduleSyncService
from edutracker.infrastructure.remote.ssh_file_fetcher import SshFileFetcher
from edutracker.infrastructure.remote.sqlite_file_validator import SQLiteFileValidator

service = ScheduleSyncService(
    fetcher=SshFileFetcher(),
    validator=SQLiteFileValidator(),
)


result = service.sync_now()
print("current: ", result)