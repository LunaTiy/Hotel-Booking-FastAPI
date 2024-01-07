from app.tasks.celery_setup import celery_app


@celery_app.task(name="periodic_task")
def periodic_task() -> None:
    print(12345)  # noqa: T201
