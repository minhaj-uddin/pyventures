import logging
import datetime
from app import app
from billing import get_due_users, charge_user


@app.task(bind=True, max_retries=3, default_retry_delay=60)
def charge_single_user(self, user):
    try:
        charge_user(user)
        logging.info(f"✅ Charged {user['email']} successfully.")
    except Exception as exc:
        retry_count = self.request.retries
        # Exponential backoff: 1min, 4min
        delay = 60 * (2 ** retry_count)
        logging.warning(
            f"⚠️ Failed to charge {user['email']}, retrying in {delay}s...")
        raise self.retry(exc=exc, countdown=delay)


@app.task
def process_due_subscriptions():
    now = datetime.datetime.utcnow()
    due_users = get_due_users(now)

    if not due_users:
        logging.info("No users to charge at this time.")
        return "No users to charge."

    for user in due_users:
        charge_single_user.delay(user)

    return f"Dispatched billing tasks for {len(due_users)} users."
