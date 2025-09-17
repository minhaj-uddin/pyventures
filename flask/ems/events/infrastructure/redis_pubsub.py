import json
import redis


class RedisPublisher:
    def __init__(self):
        self.redis = redis.Redis(
            host="localhost", port=6379, decode_responses=True)

    def publish(self, channel, message):
        self.redis.publish(channel, json.dumps(message))
