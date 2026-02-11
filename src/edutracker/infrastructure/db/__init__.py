# intentionally empty

# from pathlib import Path

# from sqlalchemy.orm import Session

# from edutracker.core.config import settings
# from edutracker.infrastructure.db.base import Base
# from edutracker.infrastructure.db.database import build_engine



# def main() -> None:
#     Path(settings.DB_PATH).parent.mkdir(parents=True, exist_ok=True)

#     engine_rw = build_engine(readonly=False)

#     Base.metadata.create_all(bind=engine_rw)

#     print(f"DB initialized: {settings.DB_PATH}")



# if __name__ == "__main__":
#     main()