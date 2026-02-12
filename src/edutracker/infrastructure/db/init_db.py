from pathlib import Path

from edutracker.core.config import settings
from edutracker.infrastructure.db.base import Base
from edutracker.infrastructure.db.database import build_engine

import edutracker.infrastructure.db.models  

def main() -> None:
    db_path = Path(settings.DB_PATH).resolve()
    db_path.parent.mkdir(parents=True, exist_ok=True)


    print("Registered tables:", list(Base.metadata.tables.keys()))

    engine_rw = build_engine(readonly=False)
    Base.metadata.create_all(bind=engine_rw)


if __name__ == "__main__":
    main()