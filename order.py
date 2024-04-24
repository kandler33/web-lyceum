import flask
import flask_login

from data import db_session
from data.order_models import Order, OrderItem


@flask_login.login_required
def create_order():
    order_id = Order.create_order_for_user(flask_login.current_user)

    return flask.redirect(f"/order/{order_id}")


@flask_login.login_required
def order_detail(pk):
    db_sess = db_session.create_session()
    order = db_sess.get(Order, pk)
    if not order or order.user != flask_login.current_user:
        return flask.abort(404)

    items = db_sess.query(OrderItem).filter(OrderItem.order == order)

    return flask.render_template("order.html", order=order, items=items)
