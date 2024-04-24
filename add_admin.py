import argparse

from data import db_session
from data.user_models import User


def add_admin(email):
    db_session.global_init("db/db.sqlite")

    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.email == email).first()

    if not user:
        raise ValueError(f"User with email: {email} not found")

    user.is_admin = True
    db_sess.commit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("email", type=str)

    args = parser.parse_args()
    email = args.email

    try:
        add_admin(email)

    except ValueError as err:
        print(err)

    else:
        print(f"User with email: {email} is admin now")
