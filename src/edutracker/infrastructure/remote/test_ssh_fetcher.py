from edutracker.core.config import settings
from edutracker.infrastructure.remote.ssh_file_fetcher import SshFileFetcher


def main() -> None:
    fetcher = SshFileFetcher()

    print("remote: ", settings.SCHEDULE_REMOTE_DB_PATH)
    print("local tmp: ", settings.SCHEDULE_LOCAL_TMP_PATH)

    result = fetcher.fetch(
        source_path=settings.SCHEDULE_REMOTE_DB_PATH,
        destination_path=settings.SCHEDULE_LOCAL_TMP_PATH,
    )

    print("download: ", result)


if __name__ == "__main__":
    main()
