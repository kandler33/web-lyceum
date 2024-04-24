import flask
import flask_wtf
import flask_login
import wtforms

from data import db_session
from data.order_models import Order, OrderItem
from data.catalog_models import Item, Category


class ItemForm(flask_wtf.FlaskForm):
    name = wtforms.StringField(
        "Название",
        validators=[wtforms.validators.DataRequired()],
    )
    price = wtforms.FloatField(
        "Цена",
        validators=[
            wtforms.validators.DataRequired(),
            wtforms.validators.NumberRange(min=0),
        ],
    )
    text = wtforms.TextAreaField("Описание")
    category = wtforms.SelectField(
        "Категория",
        coerce=int,
        validators=[wtforms.validators.DataRequired()],
    )
    submit = wtforms.SubmitField("Создать")


class CategoryForm(flask_wtf.FlaskForm):
    name = wtforms.StringField(
        "Название",
        validators=[wtforms.validators.DataRequired()],
    )
    submit = wtforms.SubmitField("Создать")


class OrderStatusForm(flask_wtf.FlaskForm):
    status = wtforms.SelectField(
        "Статус",
        validators=[wtforms.validators.DataRequired()],
    )
    submit = wtforms.SubmitField("Изменить")


@flask_login.login_required
def create_item():
    if not flask_login.current_user.is_admin:
        flask.abort(404)

    db_sess = db_session.create_session()
    categories = db_sess.query(Category)
    choices = [(category.id, category.name) for category in categories]
    form = ItemForm()
    form.category.choices = choices

    if form.validate_on_submit():
        item = Item(
            name=form.name.data,
            price=form.price.data,
            text=form.text.data,
            category_id=form.category.data,
        )
        db_sess.add(item)
        db_sess.commit()

        return flask.redirect(f"/item/{item.id}")

    return flask.render_template("item_form.html", form=form)


@flask_login.login_required
def edit_item(pk):
    if not flask_login.current_user.is_admin:
        flask.abort(404)

    db_sess = db_session.create_session()

    item = db_sess.get(Item, pk)

    if not item:
        flask.abort(404)

    categories = db_sess.query(Category)
    choices = [(category.id, category.name) for category in categories]
    form = ItemForm()
    form.category.choices = choices

    form.name.data = item.name
    form.text.data = item.text
    form.price.data = item.price
    form.category.data = item.category_id

    if form.validate_on_submit():
        item.name = form.name.data
        item.price = form.price.data
        item.text = form.text.data
        item.category_id = form.category.data

        db_sess.commit()

        return flask.redirect(f"/item/{item.id}")

    return flask.render_template("item_form.html", form=form)


@flask_login.login_required
def create_category():
    if not flask_login.current_user.is_admin:
        flask.abort(404)

    db_sess = db_session.create_session()
    form = CategoryForm()

    if form.validate_on_submit():
        category = Category(name=form.name.data)
        db_sess.add(category)
        db_sess.commit()

        return flask.redirect("/")

    return flask.render_template("category_form.html", form=form)


@flask_login.login_required
def edit_category(pk):
    if not flask_login.current_user.is_admin:
        flask.abort(404)

    db_sess = db_session.create_session()

    category = db_sess.get(Category, pk)
    if not category:
        flask.abort(404)

    form = CategoryForm()

    form.name.data = category.name

    if form.validate_on_submit():
        category.name = form.name.data

        db_sess.commit()

        return flask.redirect("/")

    return flask.render_template("category_form.html", form=form)


@flask_login.login_required
def admin_item_list():
    if not flask_login.current_user.is_admin:
        flask.abort(404)

    db_sess = db_session.create_session()
    items = db_sess.query(Item)

    categories = db_sess.query(Category)

    category = flask.request.args.get("category", None)
    if category:
        items = items.filter(Item.category_id == category)

    return flask.render_template(
        "admin_item_list.html",
        items=items,
        categories=categories,
    )


@flask_login.login_required
def admin_category_list():
    if not flask_login.current_user.is_admin:
        flask.abort(404)

    db_sess = db_session.create_session()
    categories = db_sess.query(Category)

    return flask.render_template(
        "admin_category_list.html",
        categories=categories,
    )


@flask_login.login_required
def admin_order_detail(pk):
    if not flask_login.current_user.is_admin:
        flask.abort(404)

    db_sess = db_session.create_session()
    order = db_sess.get(Order, pk)

    if not order:
        flask.abort(404)

    choices = [(status, status) for status in Order.statuses]
    form = OrderStatusForm()
    form.status.choices = choices

    items = db_sess.query(OrderItem).filter(OrderItem.order == order)

    message = None

    if form.validate_on_submit:
        order.status = form.status.data

        db_sess.commit()

        message = "Статус успешно изменен"

    return flask.render_template(
        "admin_order_detail.html",
        order=order,
        items=items,
        form=form,
        message=message,
    )


@flask_login.login_required
def admin_order_list():
    if not flask_login.current_user.is_admin:
        flask.abort(404)

    db_sess = db_session.create_session()
    orders = db_sess.query(Order)

    statuses = Order.statuses

    status = flask.request.args.get("status", None)
    if status:
        orders = orders.filter(Order.status == status)

    return flask.render_template(
        "admin_order_list.html",
        orders=orders,
        statuses=statuses,
    )


@flask_login.login_required
def admin_index():
    if not flask_login.current_user.is_admin:
        flask.abort(404)

    return flask.render_template("admin_index.html")
