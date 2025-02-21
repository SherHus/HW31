import datetime

import bcrypt

from pkg.repositories import user as user_repository
from schemas.user import UserSchema
from db.models import User


def get_user_by_username(username):
    user = user_repository.get_user_by_username(username)
    return user


def get_user_by_username_and_password(username, password):
    user = user_repository.get_user_by_username(username)  # Получаем пользователя по username

    if user is None:
        return None

    if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return None

    return user


def create_user(user: UserSchema):
    u = User()
    u.full_name = user.full_name
    u.username = user.username
    u.password = hash_password(user.password)
    u.role = "user"
    u.created_at = datetime.datetime.now()

    return user_repository.create_user(u)


# pip install bcrypt
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """ Проверяет соответствие введённого пароля его хешу из БД """
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
