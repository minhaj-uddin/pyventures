import json
import redis
from application.services import TicketIssuer
from events.infrastructure.redis_pubsub import RedisPublisher


def start_ticket_listener():
    r = redis.Redis(host="localhost", port=6379, decode_responses=True)
    pubsub = r.pubsub()
    pubsub.subscribe("events")

    publisher = RedisPublisher()
    issuer = TicketIssuer(publisher)

    print("[TicketService] Listening for events...")
    for msg in pubsub.listen():
        if msg["type"] != "message":
            continue

        event = json.loads(msg["data"])
        if event["event"] == "user_registered":
            data = event["data"]
            issuer.issue_ticket(data["user_id"], data["event_id"])
