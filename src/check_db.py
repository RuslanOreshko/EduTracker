from edutracker.core.config import settings
from sqlalchemy import create_engine, text

engine = create_engine(f"sqlite+pysqlite:///{settings.DB_PATH.as_posix()}")

with engine.connect() as conn:
    tables = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table';")).fetchall()
    print("Tables:", tables)

print("DB_PATH: ", settings.DB_PATH)
