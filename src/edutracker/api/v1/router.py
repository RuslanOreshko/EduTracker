from fastapi import APIRouter
from edutracker.api.v1.routers.health import router as health_router
from edutracker.api.v1.routers.root import router as root_router
from edutracker.api.v1.routers.debug import router as debug_router

from edutracker.api.v1.routers.teachers.top_teachers import router as teacher_top_router
from edutracker.api.v1.routers.teachers.teachers_stats import router as teacher_stats_router
from edutracker.api.v1.routers.teachers.teacher_compare import router as compare_teacher_router
from edutracker.api.v1.routers.teachers.peak_load_teacher_router import router as peak_load_teacher_router
from edutracker.api.v1.routers.teachers.average_lessons_router import router as average_lessons_router

router = APIRouter()

router.include_router(teacher_stats_router)
router.include_router(teacher_top_router)
router.include_router(compare_teacher_router)
router.include_router(peak_load_teacher_router)
router.include_router(average_lessons_router)

router.include_router(health_router)
router.include_router(root_router)
router.include_router(debug_router)
