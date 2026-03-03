from dataclasses import dataclass
from sqlalchemy import select, or_
from sqlalchemy.orm import Session

from edutracker.infrastructure.db.teacher_catalog.model import Teacher


@dataclass(frozen=True)
class TeacherSuggastRow:
    display_name: str


class TeacherCatalogRepository:
    def __init__(self, db: Session):
        self._db = db

    def suggest(self, q: str, limit: int = 10) -> list[TeacherSuggastRow]:
        q = (q or "").strip().lower()
        if len(q) < 2:
            return []
        
        stmt = (
            select(Teacher.display_name)
            .where(
                or_(
                    Teacher.name_norm.like(f"%{q}%"),
                    Teacher.search_key.like(f"%{q}%"),
                )
            )
            .order_by(Teacher.last_seen_at.desc())
            .limit(limit)
        )

        rows = self._db.execute(stmt).scalars().all()
        return [TeacherSuggastRow(display_name=dn) for dn in rows]