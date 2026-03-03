from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session 
from sqlalchemy.exc import OperationalError

from edutracker.api.deps.t_catalog_db import get_teacher_catalog_db
from edutracker.api.deps.permissions import required_roles
from edutracker.application.common.exceptions import TeacherCatalogUnavailableError

from edutracker.infrastructure.repositories.teacher_catalog_repository import TeacherCatalogRepository
from edutracker.api.v1.schemas.catalog_teachers_out import TeacherSuggestResponseDto


router = APIRouter(prefix="/teachers", tags=["Teachers"], dependencies=[Depends(required_roles("teacher", "admin"))])


@router.get("/suggest", response_model=TeacherSuggestResponseDto)
def suggest_teachers(
    q: str = Query("", min_length=0),
    limit: int = Query(10, ge=1, le=30),
    db: Session = Depends(get_teacher_catalog_db),
):
    try:
        repo = TeacherCatalogRepository(db)
        rows = repo.suggest(q=q, limit=limit)

        return {
            "items": [{"display_name": r.display_name} for r in rows]
        }
    except OperationalError as e:
        raise TeacherCatalogUnavailableError() from e
