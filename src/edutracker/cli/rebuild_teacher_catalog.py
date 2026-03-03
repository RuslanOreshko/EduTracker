from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Iterable
import logging

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError, SQLAlchemyError

from edutracker.infrastructure.db.schedule_teachers.models import ScheduleRecord

from edutracker.infrastructure.db.teacher_catalog.session import TeacherSessionLocal as TeacherCatalogSession
from edutracker.infrastructure.repositories.teachers_repository import TeachersRepository  
from edutracker.application.common.teacher_text import split_teachers, clean_display_name


from edutracker.infrastructure.db.schedule_teachers.database import create_session_local


# rebuid створений для того, що б оновлювати кількість викладачів у нормалізованій базі даних, де записані всі викладачі.
# Перед оновлення рекомендовано очистити бд (опціонально)
# Щоб виконати оновлення кількості викладачів в нормалізованій бд потрібно вести ось таку команду `python -m edutracker.cli.rebuild_teacher_catalog` із директорії src

# бд teacher_catalog застосовуєтся для зручного вибору викладача


logger = logging.getLogger("cli.rebuild_teacher_catalog")

ScheduleSession = create_session_local(readonly=True)


def extract_teachers(raw_schedule_for_teachers: str | None) -> Iterable[tuple[str, str | None]]:
    if not raw_schedule_for_teachers:
        return []

    try:
        obj = json.loads(raw_schedule_for_teachers)
    except Exception:
        return []

    seen = set()
    out: list[tuple[str, str | None]] = []

    for _, teacher_block in (obj or {}).items():
        email = None
        if isinstance(teacher_block, dict):
            email = teacher_block.get("email")

        for day_name, day in (teacher_block or {}).items():
            if day_name == "email":
                continue

            lessons = (day or {}).get("lessons") or []
            for lesson in lessons:
                tname = lesson.get("teacher_name")
                if not tname:
                    continue

                for one in split_teachers(tname):
                    key = one.strip().lower()
                    if key in seen:
                        continue
                    seen.add(key)
                    out.append((one.strip(), email))

    return out


def rebuild() -> None:
    schedule_db: Session = ScheduleSession()
    catalog_db: Session = TeacherCatalogSession()
    repo = TeachersRepository(catalog_db)

    now = datetime.now(timezone.utc)

    try:
        rows = schedule_db.execute(
            select(ScheduleRecord.schedule_for_teachers)
            .where(ScheduleRecord.schedule_for_teachers.is_not(None))
        ).all()

        unique = {}  

        for (raw,) in rows:
            for display_name, email in extract_teachers(raw):
                dn = clean_display_name(display_name)
                if not dn:
                    continue


                key = dn.lower() 
                if key in unique:
                    old_dn, old_email = unique[key]
                    if (not old_email) and email:
                        unique[key] = (old_dn, email)
                else:
                    unique[key] = (dn, email)

        for _, (dn, email) in unique.items():
            repo.upsert(display_name=dn, email=email, seen_at=now)

        catalog_db.commit()
        print(f"teachers unique={len(unique)}")

    except OperationalError as e:
        catalog_db.rollback()
        logger.exception("SQLite operational error (locked?)", exc_info=e)
        raise 
    except SQLAlchemyError as e:
        catalog_db.rollback()
        logger.exception("SQLAlchemy error", exc_info=e)
        raise
    except Exception as e:
        catalog_db.rollback()
        logger.exception("Unexpected rebuild error", exc_info=e)
        raise

    finally:
        schedule_db.close()
        catalog_db.close()


if __name__ == "__main__":
    rebuild()