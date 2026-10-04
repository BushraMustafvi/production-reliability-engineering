import signal

from application.queue.redis_queue import RedisQueue


shutdown_requested = False


def handle_shutdown(signum, frame):
    global shutdown_requested
    shutdown_requested = True
    print(
        f"ORDER_WORKER_SHUTDOWN_SIGNAL={signum}",
        flush=True,
    )


def process_order_event(event):
    print("ORDER_EVENT_PROCESSED", event, flush=True)


def run_worker():
    global shutdown_requested

    signal.signal(signal.SIGTERM, handle_shutdown)
    signal.signal(signal.SIGINT, handle_shutdown)

    queue = RedisQueue()

    print("ORDER_WORKER_STARTED", flush=True)

    while not shutdown_requested:
        event = queue.dequeue("order_events", timeout=5)

        if event is None:
            continue

        process_order_event(event)

    print("ORDER_WORKER_STOPPED", flush=True)


if __name__ == "__main__":
    run_worker()
