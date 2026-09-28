from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from application.common.orders import Order
from application.database.engine import engine
from application.database.models import OrderRecord


class OrderRepository:
    def save(self, order: Order) -> Order:
        with Session(engine) as session:
            record = OrderRecord(
                order_id=order.order_id,
                customer_id=order.customer_id,
                amount=order.amount,
                currency=order.currency,
                status=order.status,
            )

            session.add(record)
            session.commit()

        return order

    def get(self, order_id: str) -> Optional[Order]:
        with Session(engine) as session:
            record = session.get(OrderRecord, order_id)

            if record is None:
                return None

            return Order(
                order_id=record.order_id,
                customer_id=record.customer_id,
                amount=record.amount,
                currency=record.currency,
                status=record.status,
            )

    def list_all(self) -> List[Order]:
        with Session(engine) as session:
            records = session.scalars(
                select(OrderRecord)
            ).all()

            return [
                Order(
                    order_id=record.order_id,
                    customer_id=record.customer_id,
                    amount=record.amount,
                    currency=record.currency,
                    status=record.status,
                )
                for record in records
            ]
