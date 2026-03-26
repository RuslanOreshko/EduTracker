from edutracker.core.config import settings
from edutracker.infrastructure.remote.local_file_fetcher import LocalFileFetcher
from edutracker.infrastructure.remote.ssh_file_fetcher import SshFileFetcher


def build_schedule_fetcher():
    mode = settings.SCHEDULE_SOURCE_MODE.lower().strip()

    if mode == "local":
        return LocalFileFetcher()
    
    if mode == "ssh":
        return SshFileFetcher()
    
    raise ValueError(
        f"Unsupported SCHEDULE_SOURCE_MODE: {settings.SCHEDULE_SOURCE_MODE}"
    )