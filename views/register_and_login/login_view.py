from flask import flash, redirect, url_for
from flask_login import login_user

from models import User


def login(session, username, password):

    user = session.query(User).filter_by(username=username, password=password).first()

    if not user or user.password != password:
        flash("Неверный никнейм или пароль.")
        return redirect(url_for('login_page'))

    login_user(user)

