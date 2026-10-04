import json
import os

import redis


class RedisQueue:
    def __init__(self, url=None):
        self.url = url or os.getenv(
            "REDIS_URL",
            "redis://localhost:6379/0",
        )
        self.client = redis.Redis.from_url(
            self.url,
            decode_responses=True,
        )

    def check_connection(self):
        return self.client.ping()

    def enqueue(self, queue_name, payload):
        self.client.rpush(queue_name, json.dumps(payload))

    def dequeue(self, queue_name, timeout=5):
        result = self.client.blpop(queue_name, timeout=timeout)

        if result is None:
            return None

        _, payload = result
        return json.loads(payload)
