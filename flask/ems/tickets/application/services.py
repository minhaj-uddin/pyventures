from domain.entities import Ticket
from events.infrastructure.redis_pubsub import RedisPublisher


class TicketIssuer:
    def __init__(self, publisher: RedisPublisher):
        self.publisher = publisher

    def issue_ticket(self, user_id, event_id):
        ticket_id = f"{user_id}-{event_id}"
        ticket = Ticket(ticket_id, user_id, event_id)
        print(f"[TicketService] Issued ticket #{ticket}")

        self.publisher.publish("events", {
            "event": "ticket_issued",
            "data": {
                "ticket_id": ticket_id,
                "user_id": user_id,
                "event_id": event_id
            }
        })
