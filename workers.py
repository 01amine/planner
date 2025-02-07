from celery import Celery
from services import monitor_stock

celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

@celery_app.task
def run_monitoring():
    monitor_stock()
