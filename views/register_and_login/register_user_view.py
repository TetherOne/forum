from flask import flash

from models import User


def register_user(session, username, email, password):
    new_user = User(username=username, email=email, password=password)

    session.add(new_user)
    flash('Вы успешно зарегистрировались!')

    session.commit()