from edutracker.infrastructure.db.Auth.auth_base import AuthBase
from edutracker.infrastructure.db.Auth.auth_database import engine

from edutracker.infrastructure.db.Auth import AuthUser, RefreshToken

from sqlalchemy import create_engine
from edutracker.core.config import settings


def main() -> None:
    AuthBase.metadata.create_all(engine)
    print()


if __name__ == "__main__":
    main()