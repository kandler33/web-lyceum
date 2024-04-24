import flask
import flask_wtf
import flask_login
import wtforms

from data import db_session
from data.user_models import User, Bascket
from data.catalog_models import Item, Category


def item_list():
    db_sess = db_session.create_session()
    items = db_sess.query(Item)

    categories = db_sess.query(Category)

    category = flask.request.args.get("category", None)
    if category:
        items = items.filter(Item.category_id == category)

    if flask.request.form and flask_login.current_user.is_authenticated:
        if flask.request.form.get("add_item"):
            Bascket.add_item_to_user(
                user_id=flask_login.current_user.id,
                item_id=flask.request.form.get("add_item"),
            )

        elif flask.request.form.get("delete_item"):
            Bascket.delete_one_item_to_user(
                user_id=flask_login.current_user.id,
                item_id=flask.request.form.get("delete_item"),
            )

    return flask.render_template(
        "item_list.html",
        items=items,
        categories=categories,
    )


def item_detail(pk):
    db_sess = db_session.create_session()

    item = db_sess.get(Item, pk)

    if not item:
        flask.abort(404)

    if flask.request.form and flask_login.current_user.is_authenticated:
        if flask.request.form.get("add_item"):
            Bascket.add_item_to_user(
                user_id=flask_login.current_user.id,
                item_id=flask.request.form.get("add_item"),
            )

        elif flask.request.form.get("delete_item"):
            Bascket.delete_one_item_to_user(
                user_id=flask_login.current_user.id,
                item_id=flask.request.form.get("delete_item"),
            )

    return flask.render_template(
        "item_detail.html",
        item=item,
    )
