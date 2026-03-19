from edutracker.core.config import settings
from edutracker.infrastructure.remote.local_file_fetcher import build_local_fetcher

fetcher = build_local_fetcher()

print("source:", settings.SCHEDULE_REMOTE_DB_PATH)
print("destination:", settings.SCHEDULE_LOCAL_TMP_PATH)

result = fetcher.fetch(
    source_path=settings.SCHEDULE_REMOTE_DB_PATH,
    destination_path=settings.SCHEDULE_LOCAL_TMP_PATH,
)

print("copied to:", result)