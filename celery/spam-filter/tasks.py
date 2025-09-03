import time
import random
from celery import Celery

# Configure Celery app to use Redis as the message broker
app = Celery('spam_filter', broker='redis://localhost:6379/0')


@app.task(bind=True, ignore_result=True)
def check_spam(self, comment: str):
    print(f"Checking comment: {comment}")

    # Simulate some time-consuming task
    time.sleep(random.uniform(1, 3))

    # Simple spam logic (in reality, use a proper spam detection model or algorithm)
    spam_keywords = ["buy", "free", "lottery", "win", "prize", "offer"]
    is_spam = any(keyword in comment.lower() for keyword in spam_keywords)

    result = "Spam" if is_spam else "Not Spam"
    print(f"Comment is marked as: {result}")

    return result
