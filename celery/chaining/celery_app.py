from celery import Celery

app = Celery(
    'task_chaining',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0',
    include=['etl_tasks']
)

app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='UTC',
    enable_utc=True,
)
