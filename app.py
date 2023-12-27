from flask import Flask, flash, redirect, url_for
from flask import render_template
from flask import request
from flask_login import login_user

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from werkzeug.security import check_password_hash

from models import Base, User

app = Flask(__name__)

engine = create_engine(url='sqlite:///./db.sqlite3')
app.config['SECRET_KEY'] = 'forum'
SessionFactory = sessionmaker(bind=engine)



@app.errorhandler(404)
def page_not_found(error):
    """

    Функция для обработки ошибки, при указании неправильного пути

    """
    return render_template('forum/page_not_found_error.html')


@app.route('/', methods=['GET'])
def main_page():
    """

    Функция для отрисовки главной страницы сайта

    """
    return render_template('forum/main_page.html')



@app.route('/register', methods=['POST', 'GET'])
def register_page():
    """

    Функция для отрисовки страницы регистрации сайта

    """
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if not username or not email or not password:

            return render_template('auth/register.html', error='Заполните все поля')

        new_user = User(username=username, email=email, password=password)

        session = SessionFactory()
        session.add(new_user)
        flash('Вы успешно зарегистрировались!')
        session.commit()

    return render_template('auth/register.html')



@app.route('/login', methods=['POST', 'GET'])
def login_page():
    """

    Функция для отрисовки страницы входа на сайт

    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            return render_template('auth/login.html', error='Заполните все поля')

        session = SessionFactory()

        user = session.query(User).filter_by(username=username, password=password).first()

        if not user or user.password != password:
            flash("Неверный никнейм или пароль.")
            return redirect(url_for('login_page'))
        return redirect(url_for('main_page'))

    return render_template('auth/login.html')



def main():
    Base.metadata.create_all(bind=engine)
    with Session(engine) as session:
        session.commit()



if __name__ == '__main__':
    app.run(debug=True)
    main()
