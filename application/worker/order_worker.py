from application.queue.redis_queue import RedisQueue


def process_order_event(event):
    print("ORDER_EVENT_PROCESSED", event)


def run_worker():
    queue = RedisQueue()

    print("ORDER_WORKER_STARTED")

    while True:
        event = queue.dequeue("order_events", timeout=5)

        if event is None:
            continue

        process_order_event(event)


if __name__ == "__main__":
    run_worker()
