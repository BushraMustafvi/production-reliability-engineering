from dataclasses import dataclass


@dataclass
class Order:
    order_id: str
    customer_id: str
    amount: float
    currency: str
    status: str = "created"
