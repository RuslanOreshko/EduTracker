from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import Session 

from edutracker.infrastructure.db.teacher_catalog.model import Teacher
from edutracker.application.common.teacher_text import norm_name, search_key


class TeachersRepository:
    def __init__(self, db: Session):
        self._db = db

    def upsert(self, display_name: str, email: str | None, seen_at: datetime) -> None:
        display_name = (display_name or "").strip()
        if not display_name:
            return
        
        existing = self._db.execute(
            select(Teacher).where(Teacher.display_name == display_name)
        ).scalar_one_or_none()

        if existing:
            existing.name_norm = norm_name(display_name)
            existing.search_key = search_key(display_name)
            existing.last_seen_at = seen_at
            if email:
                existing.email = email

            return 
        
        self._db.add(
            Teacher(
                display_name=display_name,
                name_norm=norm_name(display_name),
                search_key=search_key(display_name),
                email=email,
                last_seen_at=seen_at,
            )
        )

    def exists(self, teacher: str) -> bool:
        t = norm_name(teacher)
        if len(t) < 2:
            return False
        
        row = self._db.execute(
            select(Teacher.id).where(Teacher.name_norm == t).limit(1)
        ).first()

        return row is not None
    
    def suggest(self, query: str, limit: int = 10) -> list[str]:
        q = search_key(query)
        if len(q) < 2:
            return []
        
        rows = self._db.execute(
            select(Teacher.display_name)
            .where(Teacher.search_key.like(f"{q}%"))
            .order_by(Teacher.display_name.asc())
            .limit(limit)
        ).all()

        return [r[0] for r in rows]