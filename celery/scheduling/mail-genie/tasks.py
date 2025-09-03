import datetime
from app import app

USERS = [
    {"email": "user1@example.com"},
    {"email": "user2@example.com"},
]


def send_email(to, subject, body):
    # Placeholder for real email sending logic
    print(f"[{datetime.datetime.now()}] Sending email to: {to}")
    print(f"Subject: {subject}")
    print(f"Body:\n{body}\n")


@app.task
def send_daily_digest():
    subject = "Your Daily Digest"
    body = "Here’s what’s new today...\n\n- Item 1\n- Item 2\n- ..."

    for user in USERS:
        send_email(user['email'], subject, body)

    return f"Sent daily digest to {len(USERS)} users."
