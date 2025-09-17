from infrastructure.redis_pubsub import RedisPublisher


class RegisterUser:
    def __init__(self, event_repository, publisher: RedisPublisher):
        self.repo = event_repository
        self.publisher = publisher

    def execute(self, user_id, event_id):
        event = self.repo.get_event_by_id(event_id)
        event.register_user(user_id)
        self.repo.save(event)

        # Publish domain event
        self.publisher.publish("events", {
            "event": "user_registered",
            "data": {
                "user_id": user_id,
                "event_id": event_id
            }
        })
