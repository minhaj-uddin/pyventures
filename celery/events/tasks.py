from celery import Celery

app = Celery('events', broker='redis://localhost:6379/0')


@app.task
def fail_me():
    raise ValueError("Something bad happened!")
