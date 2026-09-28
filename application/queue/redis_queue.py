import json

import redis


class RedisQueue:
    def __init__(self, url="redis://localhost:6379/0"):
        self.client = redis.Redis.from_url(
            url,
            decode_responses=True,
        )

    def enqueue(self, queue_name, payload):
        self.client.rpush(
            queue_name,
            json.dumps(payload),
        )

    def dequeue(self, queue_name, timeout=5):
        result = self.client.blpop(
            queue_name,
            timeout=timeout,
        )

        if result is None:
            return None

        _, payload = result
        return json.loads(payload)
