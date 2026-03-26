from fastapi import FastAPI

import logging 

from edutracker.api.v1.router import router as v1_router
from edutracker.core.config import settings
from edutracker.core.logging import setup_logging

from edutracker.application.services.schedule_sync_service import ScheduleSyncService
from edutracker.infrastructure.remote.ssh_file_fetcher import SshFileFetcher
from edutracker.infrastructure.remote.sqlite_file_validator import SQLiteFileValidator

from edutracker.api.middleware.logging_middleware import logging_middleware
from edutracker.api.middleware.exception_handlers import register_exception_handlers

from edutracker.application.jobs.scheduler import start_jobs, stop_jobs
from edutracker.application.jobs.schedule_sync_jobs import build_schedule_sync_service

logger = logging.getLogger(__name__)


setup_logging(settings.DEBUG)

app = FastAPI(title="EduTracker")

app.include_router(v1_router, prefix="/api/v1")
app.middleware("http")(logging_middleware)


@app.on_event("startup")
def startup_sync_schedule():
    if not settings.SCHEDULE_SYNC_ENABLED:
        return
    
    service = build_schedule_sync_service()

    try:
        service.ensure_fresh_copy()
    except Exception:
        if service.has_valid_current_copy():
            logger.exception(
                "Startup schedule sync failed, using existing local cache"
            )
            return
        
        logger.exception(
            "Startup schedule sync failed and no valid local cache exists"
        )
        raise



@app.on_event("startup")
def start_scheduler():
    start_jobs()

@app.on_event("shutdown")
def on_shutdown():
    stop_jobs()


register_exception_handlers(app)