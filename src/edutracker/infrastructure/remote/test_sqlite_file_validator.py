from edutracker.core.config import settings
from edutracker.infrastructure.remote.sqlite_file_validator import SQLiteFileValidator


def main() -> None:
    validator = SQLiteFileValidator()

    validator.validate(settings.SCHEDULE_LOCAL_TMP_PATH)

    print("SQLite tmp file is valid.")


if __name__ == "__main__":
    main()
