"""
Celery application configuration.
"""
from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "hiring_portal",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["app.tasks.scraping"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
)

# Periodic tasks schedule
celery_app.conf.beat_schedule = {
    "scrape-jobs-every-6-hours": {
        "task": "app.tasks.scraping.scrape_jobs_task",
        "schedule": settings.SCRAPING_INTERVAL_HOURS * 3600.0,  # Convert hours to seconds
    },
}

