import time
from celery import Celery

app = Celery(
    "event_listener",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

app.config_from_object("celeryconfig")


@app.task(bind=True)
def sample_task(self, n: int) -> int:
    time.sleep(2)
    return n * n
