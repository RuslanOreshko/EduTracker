from fastapi import APIRouter
from edutracker.api.v1.routers.health import router as health_router
from edutracker.api.v1.routers.root import router as root_router
from edutracker.api.v1.routers.teachers_stats import router as schedule_records_router
from edutracker.api.v1.routers.debug import router as debug_router
from edutracker.api.v1.routers.top_teachers import router as teacher_top_router

router = APIRouter()
router.include_router(health_router)
router.include_router(root_router)
router.include_router(schedule_records_router)
router.include_router(debug_router)
router.include_router(teacher_top_router)