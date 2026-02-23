from fastapi import FastAPI
from edutracker.api.v1.router import router as v1_router
from edutracker.core.config import settings
from edutracker.core.logging import setup_logging

setup_logging(settings.DEBUG)

app = FastAPI(title="EduTracker")

app.include_router(v1_router, prefix="/api/v1")