from typing import List, Optional

from application.common.orders import Order
from application.database.orders import OrderRepository


class OrderService:
    def __init__(self, repository: Optional[OrderRepository] = None):
        self.repository = repository or OrderRepository()

    def create_order(
        self,
        order_id: str,
        customer_id: str,
        amount: float,
        currency: str = "USD",
    ) -> Order:
        if self.repository.get(order_id) is not None:
            raise ValueError("order already exists")

        if amount <= 0:
            raise ValueError("amount must be greater than zero")

        order = Order(
            order_id=order_id,
            customer_id=customer_id,
            amount=amount,
            currency=currency,
        )

        return self.repository.save(order)

    def get_order(self, order_id: str) -> Optional[Order]:
        return self.repository.get(order_id)

    def list_orders(self) -> List[Order]:
        return self.repository.list_all()
