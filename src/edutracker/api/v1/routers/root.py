from fastapi import APIRouter

router = APIRouter(tags=["root"])

@router.get("/")
def root():
    return {
        "service": "EduTracker",
        "version": "v1",
        "docs": "/docs",
        "health": "/api/v1/health"
    }