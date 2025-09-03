from celery import Celery

app = Celery(
    'daily_digest',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/1',
    include=["tasks"]
)

# Load periodic task settings
app.config_from_object('celeryconfig')
