from application.worker import order_worker


class FakeQueue:
    def __init__(self):
        self.calls = 0

    def dequeue(self, queue_name, timeout=5):
        self.calls += 1

        if self.calls == 1:
            order_worker.handle_shutdown(15, None)

        return None


def test_worker_stops_after_shutdown_signal(monkeypatch, capsys):
    order_worker.shutdown_requested = False

    fake_queue = FakeQueue()

    monkeypatch.setattr(
        order_worker,
        "RedisQueue",
        lambda: fake_queue,
    )

    order_worker.run_worker()

    output = capsys.readouterr().out

    assert "ORDER_WORKER_STARTED" in output
    assert "ORDER_WORKER_SHUTDOWN_SIGNAL=15" in output
    assert "ORDER_WORKER_STOPPED" in output
    assert fake_queue.calls == 1

    order_worker.shutdown_requested = False
