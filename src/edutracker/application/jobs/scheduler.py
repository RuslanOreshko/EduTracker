from apscheduler.schedulers.background import BackgroundScheduler
from edutracker.application.jobs.refresh_token_cleanup import run_refresh_cleanup

scheduler = BackgroundScheduler()


def start_jobs():
    if not scheduler.running:
        scheduler.add_job(
            run_refresh_cleanup,
            "interval",
            hours=24,
            id="refresh_token_cleanup",
            replace_existing=True,
        )
        scheduler.start()

def stop_jobs():
    if scheduler.running:
        scheduler.shutdown(wait=False)     