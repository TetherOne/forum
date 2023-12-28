from flask import Flask
from flask import flash
from flask import redirect
from flask import url_for
from flask import render_template
from flask import request

from flask_login import login_user
from flask_login import logout_user
from flask_login import current_user
from flask_login import LoginManager

from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session


from models import Base
from models import User
from models import Article



app = Flask(__name__)



engine = create_engine(url='sqlite:///./db.sqlite3')
app.config['SECRET_KEY'] = 'forum'
SessionFactory = sessionmaker(bind=engine)



login_manager = LoginManager(app)
login_manager.init_app(app)



@login_manager.user_loader
def load_user(id):
    """

    Получение объекта пользователя по id из базы данных

    """
    session = SessionFactory()
    return session.query(User).get(int(id))



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
    session = SessionFactory()
    articles = session.query(Article).all()

    return render_template('forum/main_page.html', articles=articles)



@app.route('/your_profile')
def your_profile_page():
    """

    Функция для отображения профиля пользователя

    """
    return render_template('forum/your_profile.html')



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

        login_user(user)

        return redirect(url_for('your_profile_page'))

    return render_template('auth/login.html')



@app.route('/logout', methods=['POST', 'GET'])
def logout_page():
    """

    Функция для выхода из профиля

    """
    logout_user()

    return redirect(url_for('your_profile_page'))



@app.route('/your_profile/create_article', methods=['POST', 'GET'])
def create_article_page():
    """

    Функция для создания статьи

    """
    if request.method == 'POST':

        name_of_article = request.form.get('name_of_article')
        text_of_article = request.form.get('text_of_article')

        if not name_of_article or not text_of_article:
            return render_template('forum/create_article.html', error='Заполните все поля')

        session = SessionFactory()

        new_article = Article(name_of_article=name_of_article, text_of_article=text_of_article, user_id=current_user.id)

        session.add(new_article)

        flash('Статья опубликована!')

        session.commit()

        return redirect(url_for('your_profile_page'))

    return render_template('forum/create_article.html')



def main():
    Base.metadata.create_all(bind=engine)
    with Session(engine) as session:
        session.commit()



if __name__ == '__main__':
    app.run(debug=True)
    main()
