from flask import Flask
import flask_login

import homepage
import user_views
import catalog
import order
import admin
from data import db_session
from data.user_models import User

app = Flask(__name__)
app.config["SECRET_KEY"] = "not_so_secret"

login_manager = flask_login.LoginManager()
login_manager.init_app(app)


def main():
    global login_manager
    db_session.global_init("db/db.sqlite")
    app.run()


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


app.route("/")(homepage.index)

app.route("/user/signup", methods=("GET", "POST"))(user_views.signup)
app.route("/user/login", methods=("GET", "POST"))(user_views.login)
app.route("/user/logout")(user_views.logout)
app.route("/user")(user_views.profile)
app.route("/user/bascket", methods=("GET", "POST"))(user_views.bascket)

app.route("/catalog/items", methods=("GET", "POST"))(catalog.item_list)
app.route("/catalog/item/<pk>", methods=("GET", "POST"))(catalog.item_detail)

app.route("/order/<pk>")(order.order_detail)
app.route("/order/create")(order.create_order)

app.route("/admin")(admin.admin_index)
app.route("/admin/items")(admin.admin_item_list)
app.route("/admin/item/create", methods=("GET", "POST"))(admin.create_item)
app.route("/admin/item/<pk>", methods=("GET", "POST"))(admin.edit_item)
app.route("/admin/categories")(admin.admin_category_list)
app.route("/admin/category/create", methods=("GET", "POST"))(
    admin.create_category
)
app.route("/admin/category/<pk>", methods=("GET", "POST"))(admin.edit_category)
app.route("/admin/orders")(admin.admin_order_list)
app.route("/admin/order/<pk>", methods=("GET", "POST"))(
    admin.admin_order_detail
)


if __name__ == "__main__":
    main()
