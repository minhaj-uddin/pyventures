import json
import redis


def start_notification_listener():
    r = redis.Redis(host="localhost", port=6379, decode_responses=True)
    pubsub = r.pubsub()
    pubsub.subscribe("events")

    print("[NotificationService] Listening for events...")
    for msg in pubsub.listen():
        if msg["type"] != "message":
            continue

        event = json.loads(msg["data"])
        if event["event"] == "ticket_issued":
            data = event["data"]
            print(
                f"[Notification] Email sent to user {data['user_id']} for ticket {data['ticket_id']}")
