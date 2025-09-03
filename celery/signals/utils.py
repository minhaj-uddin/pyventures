import logging

# Set up a logger for task-related information
logger = logging.getLogger('celery_signals')
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
logger.addHandler(console_handler)


def log_task_info(message: str) -> None:
    logger.info(message)


def send_email_notification(message: str) -> None:
    print(f"Sending Email: {message}")
