from celery import Celery

app = Celery(
    'db_backup',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/1',
)

app.config_from_object('celeryconfig')
