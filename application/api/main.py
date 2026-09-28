from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel
from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest

from application.queue.redis_queue import RedisQueue
from application.services.orders import OrderService


app = FastAPI(
    title="Production Reliability Engineering",
    version="0.4.0",
)

order_service = OrderService()
event_queue = RedisQueue()

orders_created_total = Counter(
    "orders_created_total",
    "Total number of successfully created orders",
)


class CreateOrderRequest(BaseModel):
    order_id: str
    customer_id: str
    amount: float
    currency: str = "USD"


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/ready")
def ready():
    return {"status": "ready"}


@app.get("/version")
def version():
    return {"version": app.version}


@app.get("/metrics")
def metrics():
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )


@app.post("/orders", status_code=201)
def create_order(request: CreateOrderRequest):
    try:
        order = order_service.create_order(
            order_id=request.order_id,
            customer_id=request.customer_id,
            amount=request.amount,
            currency=request.currency,
        )
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc

    event_queue.enqueue(
        "order_events",
        {
            "event": "order_created",
            "order_id": order.order_id,
            "customer_id": order.customer_id,
            "amount": order.amount,
            "currency": order.currency,
        },
    )

    orders_created_total.inc()

    return {
        "order_id": order.order_id,
        "customer_id": order.customer_id,
        "amount": order.amount,
        "currency": order.currency,
        "status": order.status,
    }


@app.get("/orders/{order_id}")
def get_order(order_id: str):
    order = order_service.get_order(order_id)

    if order is None:
        raise HTTPException(status_code=404, detail="order not found")

    return {
        "order_id": order.order_id,
        "customer_id": order.customer_id,
        "amount": order.amount,
        "currency": order.currency,
        "status": order.status,
    }


@app.get("/orders")
def list_orders():
    return [
        {
            "order_id": order.order_id,
            "customer_id": order.customer_id,
            "amount": order.amount,
            "currency": order.currency,
            "status": order.status,
        }
        for order in order_service.list_orders()
    ]
