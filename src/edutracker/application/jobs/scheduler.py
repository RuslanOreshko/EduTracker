from apscheduler.schedulers.background import BackgroundScheduler
from edutracker.application.jobs.refresh_token_cleanup import run_refresh_cleanup
from edutracker.core.config import settings
from edutracker.application.jobs.schedule_sync_jobs import run_schedule_sync


scheduler = BackgroundScheduler()


def start_jobs():
    if scheduler.running:
        return

    scheduler.add_job(
        run_refresh_cleanup,
        "interval",
        hours=24,
        id="refresh_token_cleanup",
        replace_existing=True,
        max_instances=1,
        coalesce=True
    )

    if settings.SCHEDULE_SYNC_ENABLED:
        scheduler.add_job(
            run_schedule_sync,
            "interval",
            minutes=1,
            # hours=settings.SCHEDULE_SYNC_INTERVAL_HOURS,
            id="schedule_sync",
            replace_existing=True,
            max_instances=1,
            coalesce=True,
            misfire_grace_time=3600,
        )

    scheduler.start()

def stop_jobs():
    if scheduler.running:
        scheduler.shutdown(wait=False)     