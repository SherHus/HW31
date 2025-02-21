import datetime

from sqlalchemy.orm import Session

from db.postgres import engine
from db.models import User


def get_user_by_username(username):
    with Session(bind=engine) as db:
        db_user = db.query(User).filter(User.username == username).first()

        return db_user


def get_user_by_username_and_password(username, password):
    with Session(bind=engine) as db:
        db_user = db.query(User).filter(User.username == username, User.password == password).first()

        return db_user


def create_user(user: User):
    with Session(bind=engine) as db:
        db.add(user)
        db.commit()
        return user.id
