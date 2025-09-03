from celery import Celery


def setup_celery():
    celery_app = Celery(
        'celery_signals',
        broker='redis://localhost:6379/0',
        backend='redis://localhost:6379/0',
        include=['tasks']
    )

    celery_app.conf.update(
        result_expires=3600,
        task_acks_late=True,
        task_time_limit=300,
    )

    return celery_app


app = setup_celery()
