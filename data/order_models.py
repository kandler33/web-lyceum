import datetime

import sqlalchemy
import sqlalchemy.orm

from .db_session import SqlAlchemyBase, create_session
from .user_models import Bascket


class Order(SqlAlchemyBase):
    __tablename__ = "orders"
    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True,
        autoincrement=True,
    )
    status = sqlalchemy.Column(
        sqlalchemy.String,
        default="created",
    )
    user_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("users.id"),
    )
    created_date = sqlalchemy.Column(
        sqlalchemy.DateTime,
        default=datetime.datetime.now,
    )
    user = sqlalchemy.orm.relationship("User")

    statuses = ("created", "preparing", "ready", "recieved")

    def set_status(self, new_status):
        if new_status not in self.statuses:
            raise ValueError("Wrong status")

        db_sess = create_session()
        self.status = new_status
        db_sess.commit()

    @classmethod
    def create_order_for_user(cls, user):
        db_sess = create_session()
        order = Order(user_id=user.id)
        db_sess.add(order)
        for b_item in db_sess.query(Bascket).filter(Bascket.user == user):
            order_item = OrderItem(
                item_id=b_item.item.id,
                order_id=order.id,
                quantity=b_item.quantity,
            )
            db_sess.delete(b_item)
            db_sess.add(order_item)
        db_sess.commit()
        return order.id


class OrderItem(SqlAlchemyBase):
    __tablename__ = "items-orders"
    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True,
        autoincrement=True,
    )
    item_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("items.id"),
    )
    order_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("orders.id"),
    )
    quantity = sqlalchemy.Column(
        sqlalchemy.Integer,
        default=0,
    )

    item = sqlalchemy.orm.relationship("Item")
    order = sqlalchemy.orm.relationship("Order")
