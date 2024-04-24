import flask
import flask_wtf
import flask_login
import wtforms

from data import db_session
from data.user_models import User, Bascket
from data.order_models import Order


class LoginForm(flask_wtf.FlaskForm):
    email = wtforms.EmailField(
        "Почта", validators=[wtforms.validators.DataRequired()]
    )
    password = wtforms.PasswordField(
        "Пароль", validators=[wtforms.validators.DataRequired()]
    )
    remember_me = wtforms.BooleanField("Запомнить меня")
    submit = wtforms.SubmitField("Войти")


class SignupForm(flask_wtf.FlaskForm):
    email = wtforms.EmailField(
        "Почта", validators=[wtforms.validators.DataRequired()]
    )
    password = wtforms.PasswordField(
        "Пароль", validators=[wtforms.validators.DataRequired()]
    )
    password_again = wtforms.PasswordField(
        "Повторите пароль", validators=[wtforms.validators.DataRequired()]
    )
    name = wtforms.StringField(
        "Имя пользователя", validators=[wtforms.validators.DataRequired()]
    )
    submit = wtforms.SubmitField("Войти")


def signup():
    form = SignupForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = (
            db_sess.query(User).filter(User.email == form.email.data).first()
        )

        if not user:
            new_user = User(name=form.name.data, email=form.email.data)
            new_user.set_password(form.password.data)
            db_sess.add(new_user)
            db_sess.commit()
            return flask.redirect("/user/login")

        return flask.render_template(
            "login.html",
            message="Пользователь уже существует",
            form=form,
        )
    return flask.render_template("signup.html", form=form)


def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = (
            db_sess.query(User).filter(User.email == form.email.data).first()
        )
        if user and user.check_password(form.password.data):
            flask_login.login_user(user, remember=form.remember_me.data)
            return flask.redirect("/")
        return flask.render_template(
            "login.html",
            message="Неправильный логин или пароль",
            form=form,
        )

    return flask.render_template("login.html", title="Авторизация", form=form)


@flask_login.login_required
def logout():
    flask_login.logout_user()
    return flask.redirect("/")


@flask_login.login_required
def profile():
    user = flask_login.current_user
    db_sess = db_session.create_session()
    orders = db_sess.query(Order).filter(Order.user == user)
    return flask.render_template("profile.html", user=user, orders=orders)


@flask_login.login_required
def bascket():
    user = flask_login.current_user
    db_sess = db_session.create_session()
    items = db_sess.query(Bascket).filter(Bascket.user == user)

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

    return flask.render_template("bascket.html", items=items)
