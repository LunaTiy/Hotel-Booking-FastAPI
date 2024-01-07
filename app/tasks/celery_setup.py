from celery import Celery

from app.config import settings

celery_app = Celery(
    "tasks",
    broker=settings.redis_url,
    include=["app.tasks.tasks", "app.tasks.scheduled_tasks"]
)

celery_app.conf.beat_schedule = {
    "every-5-seconds": {
        "task": "periodic_task",
        # "schedule": crontab(minute="30", hour="15")
        "schedule": 5
    }
}
