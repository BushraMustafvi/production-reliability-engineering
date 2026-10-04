import time

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import Response
from pydantic import BaseModel
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

from application.database.init_db import init_db
from application.queue.redis_queue import RedisQueue
from application.services.orders import OrderService


@asynccontextmanager
async def lifespan(app):
    init_db()
    yield


app = FastAPI(
    title="Production Reliability Engineering",
    version="0.4.0",
    lifespan=lifespan,
)

order_service = OrderService()
event_queue = RedisQueue()

orders_created_total = Counter(
    "orders_created_total",
    "Total number of successfully created orders",
)

http_requests_total = Counter(
    "http_requests_total",
    "Total number of HTTP requests",
    ["method", "path", "status"],
)

http_request_duration_seconds = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "path"],
)


class CreateOrderRequest(BaseModel):
    order_id: str
    customer_id: str
    amount: float
    currency: str = "USD"


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    if request.url.path == "/metrics":
        return await call_next(request)

    start = time.perf_counter()

    try:
        response = await call_next(request)
        return response
    finally:
        duration = time.perf_counter() - start
        http_requests_total.labels(
            request.method,
            request.url.path,
            response.status_code,
        ).inc()
        http_request_duration_seconds.labels(
            request.method,
            request.url.path,
        ).observe(duration)


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
