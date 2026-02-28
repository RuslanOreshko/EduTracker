from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from pathlib import Path

from edutracker.api.v1.router import router as v1_router
from edutracker.core.config import settings
from edutracker.core.logging import setup_logging

from edutracker.api.middleware.logging_middleware import logging_middleware
from edutracker.api.middleware.exception_handlers import register_exception_handlers

from edutracker.application.jobs.scheduler import start_jobs, stop_jobs

setup_logging(settings.DEBUG)

app = FastAPI(title="EduTracker")

app.include_router(v1_router, prefix="/api/v1")

app.middleware("http")(logging_middleware)

BASE_DIR = Path(__file__).resolve().parent
UI_DIR = BASE_DIR / "ui"

app.mount(
    "/ui", 
    StaticFiles(directory=BASE_DIR / "ui", 
    html=True), 
    name="ui"
)

@app.get("/ui/{full_path:path}")
def ui_spa_fallback(full_path: str):
    return FileResponse(UI_DIR / "index.html")

@app.on_event("startup")
def start_scheduler():
    start_jobs()

@app.on_event("shutdown")
def on_shutdown():
    stop_jobs()

register_exception_handlers(app)