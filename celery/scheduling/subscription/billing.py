import random
import datetime

USERS = [
    {
        "id": 1,
        "email": "user1@example.com",
        "next_billing_date": datetime.datetime(2025, 9, 2, 8, 0),
        "plan": "Pro",
        "active": True
    },
    {
        "id": 2,
        "email": "user2@example.com",
        "next_billing_date": datetime.datetime(2025, 9, 2, 7, 0),
        "plan": "Basic",
        "active": True
    },
]


def get_due_users(now=None):
    now = now or datetime.datetime.utcnow()
    return [u for u in USERS if u["active"] and u["next_billing_date"] <= now]


def charge_user(user):
    # Simulate failures
    if random.random() < 0.5:
        raise ConnectionError(f"Payment gateway failed for {user['email']}")

    print(f"Charging {user['email']} for plan {user['plan']}")
    user["next_billing_date"] += datetime.timedelta(days=30)
    return True
