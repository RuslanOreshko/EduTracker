from edutracker.core.config import settings
from edutracker.infrastructure.remote.sqlite_file_validator import SQLiteFileValidator

validator = SQLiteFileValidator()

validator.validate(settings.SCHEDULE_LOCAL_TMP_PATH)

print("SQLite tmp file is valid.")