from pathlib import Path
import sqlite3


class SQLiteFileValidator:
    def validate(self, db_path: Path, required_table: str = "schedule_records") -> None:
        db_path = Path(db_path).resolve()

        if not db_path.exists():
            raise FileNotFoundError(f"SQLite file not found: {db_path}")

        if not db_path.is_file():
            raise ValueError(f"Path is not a file: {db_path}")

        if db_path.stat().st_size == 0:
            raise ValueError(f"SQLite file is empty: {db_path}")
        
        conn = None
        try:
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT name
                FROM sqlite_master
                WHERE type='table' AND name=?
                """,
                (required_table,),
            )

            row = cursor.fetchone()

            if row is None:
                    raise ValueError(
                        f"Required table '{required_table}' not found in SQLite file: {db_path}"
                    )
            
        except sqlite3.Error as exc:
            raise ValueError(f"Invalid SQLite file: {db_path}") from exc
        
        finally: 
            if conn is not None:
                conn.close()
