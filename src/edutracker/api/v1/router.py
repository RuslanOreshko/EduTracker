from fastapi import APIRouter
from edutracker.api.v1.routers.health import router as health_router
from edutracker.api.v1.routers.root import router as root_router

router = APIRouter()
router.include_router(health_router)
router.include_router(root_router)