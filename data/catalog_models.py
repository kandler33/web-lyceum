import sqlalchemy
import sqlalchemy.orm

from .db_session import SqlAlchemyBase


class Category(SqlAlchemyBase):
    __tablename__ = "categories"
    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True
    )
    name = sqlalchemy.Column(
        sqlalchemy.String,
        unique=True,
        nullable=False,
    )
    items = sqlalchemy.orm.relationship("Item", back_populates="category")


class Item(SqlAlchemyBase):
    __tablename__ = "items"
    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True,
        autoincrement=True,
    )
    name = sqlalchemy.Column(
        sqlalchemy.String,
        nullable=False,
    )
    price = sqlalchemy.Column(
        sqlalchemy.Float,
        nullable=False,
    )
    text = sqlalchemy.Column(
        sqlalchemy.String,
        nullable=True,
    )
    category_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("categories.id"),
    )
    category = sqlalchemy.orm.relationship("Category")
