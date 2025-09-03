from celery import Celery

app = Celery(
    'subscription_billing',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/1',
    include=["tasks"]
)

app.config_from_object('celeryconfig')
