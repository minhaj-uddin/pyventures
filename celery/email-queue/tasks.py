from celery import Celery

# Celery configuration
celery = Celery(
    "email_tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)


@celery.task
def send_email_notification(to_email: str, message: str):
    print(f"[EMAIL TASK] Sending email to {to_email}: {message}")

    try:
        import time
        time.sleep(3)  # simulate network/email delay
        print(f"[EMAIL TASK] Email successfully sent to {to_email}")
    except Exception as e:
        print(f"[EMAIL TASK] Failed to send email: {e}")
        raise
