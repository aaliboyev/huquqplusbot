from celery import Celery
from src.config.settings import settings
from src.app.timeutils import tz

celery_app = Celery("worker", broker=settings.redis_url, backend=settings.redis_url)
main_queue = f"{settings.STACK_NAME}-queue"

celery_app.conf.update(
    timezone=tz,
    enable_utc=True,
    broker_connection_retry_on_startup=True,
    task_default_queue=main_queue,
    task_default_exchange=main_queue,
    task_default_routing_key=main_queue
)
