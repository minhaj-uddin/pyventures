import time
from config import app
from celery.signals import task_prerun, task_postrun, task_failure, task_success
from utils import log_task_info, send_email_notification


@app.task
def process_data(data):
    if data == "bad_data":
        raise ValueError("Data is invalid")
    time.sleep(2)
    return f"Processed: {data}"


@app.task
def fetch_data():
    time.sleep(3)
    return "Fetched data successfully"


@task_prerun.connect
def on_task_prerun(sender=None, task=None, **kwargs):
    log_task_info(
        f"Task {task.name} is about to start. Task ID: {task.request.id}")
    send_email_notification(f"Task {task.name} is starting...")


@task_postrun.connect
def on_task_postrun(sender=None, task=None, **kwargs):
    log_task_info(f"Task {task.name} finished. Task ID: {task.request.id}")
    send_email_notification(f"Task {task.name} has completed.")


@task_failure.connect
def on_task_failure(sender=None, task=None, exception=None, **kwargs):
    log_task_info(f"Task {task.name} failed. Exception: {exception}")
    send_email_notification(
        f"Task {task.name} failed with exception: {exception}")


@task_success.connect
def on_task_success(sender=None, task=None, result=None, **kwargs):
    log_task_info(f"Task {task.name} succeeded. Result: {result}")
    send_email_notification(
        f"Task {task.name} completed successfully with result: {result}")
