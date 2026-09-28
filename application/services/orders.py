from dataclasses import dataclass
from typing import Optional


@dataclass
class Order:
    order_id: str
    customer_id: str
    amount: float
    currency: str
    status: str = "created"


class OrderService:
    def __init__(self):
        self._orders = {}

    def create_order(
        self,
        order_id: str,
        customer_id: str,
        amount: float,
        currency: str = "USD",
    ) -> Order:
        if order_id in self._orders:
            raise ValueError("order already exists")

        if amount <= 0:
            raise ValueError("amount must be greater than zero")

        order = Order(
            order_id=order_id,
            customer_id=customer_id,
            amount=amount,
            currency=currency,
        )

        self._orders[order_id] = order
        return order

    def get_order(self, order_id: str) -> Optional[Order]:
        return self._orders.get(order_id)

    def list_orders(self):
        return list(self._orders.values())
