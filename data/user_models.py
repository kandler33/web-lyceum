import datetime

import sqlalchemy
import sqlalchemy.orm
import flask_login
from werkzeug.security import generate_password_hash, check_password_hash

from .db_session import SqlAlchemyBase, create_session


class User(SqlAlchemyBase, flask_login.UserMixin):
    __tablename__ = "users"
    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True,
        autoincrement=True,
    )
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(
        sqlalchemy.String, index=True, unique=True, nullable=True
    )
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(
        sqlalchemy.DateTime,
        default=datetime.datetime.now,
    )
    is_admin = sqlalchemy.Column(
        sqlalchemy.Boolean,
        default=False,
    )

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


class Bascket(SqlAlchemyBase):
    __tablename__ = "items-users"
    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True
    )
    item_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("items.id")
    )
    user_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id")
    )
    quantity = sqlalchemy.Column(sqlalchemy.Integer, default=0)

    item = sqlalchemy.orm.relationship("Item")
    user = sqlalchemy.orm.relationship("User")

    @classmethod
    def add_item_to_user(cls, user_id, item_id):
        db_sess = create_session()
        bascket_item = (
            db_sess.query(Bascket)
            .filter(Bascket.user_id == user_id, Bascket.item_id == item_id)
            .first()
        )

        if bascket_item:
            bascket_item.quantity += 1

        else:
            bascket_item = Bascket(
                item_id=item_id, user_id=user_id, quantity=1
            )
            db_sess.add(bascket_item)

        db_sess.commit()

    @classmethod
    def delete_item_to_user(cls, user_id, item_id):
        db_sess = create_session()
        bascket_item = (
            db_sess.query(Bascket)
            .filter(Bascket.user_id == user_id, Bascket.item_id == item_id)
            .first()
        )

        if bascket_item:
            db_sess.delete(bascket_item)
            db_sess.commit()

    @classmethod
    def delete_one_item_to_user(cls, user_id, item_id):
        db_sess = create_session()
        bascket_item = (
            db_sess.query(Bascket)
            .filter(Bascket.user_id == user_id, Bascket.item_id == item_id)
            .first()
        )

        if bascket_item:
            bascket_item.quantity -= 1

            if bascket_item.quantity == 0:
                db_sess.delete(bascket_item)

        db_sess.commit()
