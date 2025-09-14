import json
import redis
import threading


class RedisEventBus:
    def __init__(self):
        self.redis = redis.Redis(
            host='localhost', port=6379, decode_responses=True)
        self.subscribers = {}

    def subscribe(self, event_type: str, handler):
        if event_type not in self.subscribers:
            threading.Thread(target=self._listen, args=(
                event_type, handler), daemon=True).start()

    def _listen(self, event_type, handler):
        pubsub = self.redis.pubsub()
        pubsub.subscribe(event_type)
        for message in pubsub.listen():
            if message['type'] == 'message':
                data = json.loads(message['data'])
                print(f"Event Received: {event_type} | Data: {data}")
                handler(data)

    def publish(self, event_type: str, data: dict):
        print(f"Event Published: {event_type} | Data: {data}")
        self.redis.publish(event_type, json.dumps(data))
