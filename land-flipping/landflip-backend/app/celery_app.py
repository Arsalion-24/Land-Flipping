from celery import Celery
import os

broker_url = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
backend_url = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/1")

celery_app = Celery("landflip", broker=broker_url, backend=backend_url)

@celery_app.task
def ping():
    return "pong"
