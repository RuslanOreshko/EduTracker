"""Utilities for downloading a remote file over SSH/SFTP."""

from pathlib import Path

import paramiko

from edutracker.core.config import settings


class SshFileFetcher:
    """Fetch a file from a remote host using credentials from app settings."""

    def fetch(self, source_path: Path, destination_path: Path) -> Path:
        """Download ``source_path`` from the remote host into ``destination_path``."""
        source_path = str(source_path)
        destination_path = Path(destination_path).resolve()

        if not settings.SCHEDULE_SSH_HOST:
            raise ValueError("SCHEDULE_SSH_HOST is not configured")

        if not settings.SCHEDULE_SSH_USER:
            raise ValueError("SCHEDULE_SSH_USER is not configured")

        destination_path.parent.mkdir(parents=True, exist_ok=True)

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            self._connect(client)

            sftp = client.open_sftp()
            try:
                sftp.get(source_path, str(destination_path))

            finally:
                sftp.close()

        finally:
            client.close()

        return destination_path

    def _connect(self, client: paramiko.SSHClient) -> None:
        """Open an SSH connection using either a private key or a password."""
        if settings.SCHEDULE_SSH_KEY_PATH:
            private_key = paramiko.RSAKey.from_private_key_file(
                str(settings.SCHEDULE_SSH_KEY_PATH)
            )
            client.connect(
                hostname=settings.SCHEDULE_SSH_HOST,
                port=settings.SCHEDULE_SSH_PORT,
                username=settings.SCHEDULE_SSH_USER,
                pkey=private_key,
                timeout=10,
            )
            return

        if settings.SCHEDULE_SSH_PASSWORD:
            client.connect(
                hostname=settings.SCHEDULE_SSH_HOST,
                port=settings.SCHEDULE_SSH_PORT,
                username=settings.SCHEDULE_SSH_USER,
                password=settings.SCHEDULE_SSH_PASSWORD,
                timeout=10,
            )
            return

        raise ValueError(
            "Neither SCHEDULE_SSH_KEY_PATH nor SCHEDULE_SSH_PASSWORD is configured"
        )
