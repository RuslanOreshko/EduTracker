from fastapi import APIRouter
from edutracker.api.v1.routers.health import router as health_router
from edutracker.api.v1.routers.root import router as root_router
from edutracker.api.v1.routers.debug import router as debug_router

from edutracker.api.v1.routers.teachers import (
    compare_router,
    stats_router,
    top_teacher_router,
    peak_load_router,
    avg_router,
)


router = APIRouter()

router.include_router(stats_router)
router.include_router(top_teacher_router)
router.include_router(compare_router)
router.include_router(peak_load_router)
router.include_router(avg_router)

router.include_router(health_router)
router.include_router(root_router)
router.include_router(debug_router)
