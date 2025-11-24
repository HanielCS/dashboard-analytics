import os
from celery import Celery

BROKER_URL = os.getenv("CELERY_BROKER_URL", "amqp://guest:guest@localhost:5672//")
BACKEND_URL = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

celery_app = Celery(
    "dashboard_tasks",
    broker=BROKER_URL,
    backend=BACKEND_URL
)

celery_app.conf.task_routes = {
    "tasks.processar_importacao_csv": "main-queue"
}

import tasks