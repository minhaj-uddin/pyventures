import tasks
from celery import Celery

app = Celery('bounded_app', broker='redis://127.0.0.1:6379/0')

app.autodiscover_tasks()
