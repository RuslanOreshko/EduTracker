from fastapi import APIRouter
from edutracker.core.config import settings

router = APIRouter(tags=["dubug"])
@router.get("/debug/db_path")
def debug_db_path():
    return {"db_path": str(settings.DB_PATH)}