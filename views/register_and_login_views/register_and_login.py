from flask_login import login_user

from flask import redirect
from flask import url_for
from flask import flash

from models import User



def get_username_password(request):

    username = request.form.get('username')
    password = request.form.get('password')

    return username, password



def get_username_email_password(request):

    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    return username, email, password



def login(session, username, password):

    user = session.query(User).filter_by(username=username, password=password).first()

    if not user or user.password != password:
        flash("Неверный никнейм или пароль.")
        return redirect(url_for('login_page'))

    login_user(user)



def register_user(session, username, email, password):

    new_user = User(username=username, email=email, password=password)

    session.add(new_user)
    flash('Вы успешно зарегистрировались!')

    session.commit()