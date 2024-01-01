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

from views.create_and_check_article.view_check_form_fields import article_check_form_fields

from views.create_and_check_article.view_save_article_and_category import save_article_and_category

from views.main_page.view_main_page import upload_articles_and_categories

from views.register_and_login.get_login_fields import get_username_password

from views.register_and_login.get_register_fields import get_username_email_password



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
    articles, categories = upload_articles_and_categories(session)

    return render_template('forum/main_page.html', articles=articles, categories=categories)



@app.route('/your_profile')
def your_profile_page():
    """

    Функция для отображения профиля пользователя

    """
    if current_user.is_authenticated:

        session = SessionFactory()
        current_user_id = current_user.id
        your_articles = session.query(Article).filter_by(user_id=current_user_id).all()

        return render_template('forum/your_profile.html', articles=your_articles)

    return render_template('forum/your_profile.html')



@app.route('/register', methods=['POST', 'GET'])
def register_page():
    """

    Функция для отрисовки страницы регистрации сайта

    """
    if request.method == 'POST':
        username, email, password = get_username_email_password(request)

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
        username, password = get_username_password(request)

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
        if not article_check_form_fields(request):
            return render_template('forum/create_article.html', error='Заполните все поля')

        session = SessionFactory()

        save_article_and_category(session, request.form.get('name_of_article'),
                                  request.form.get('text_of_article'),
                                  request.form.get('category'),
                                  current_user)

        flash('Статья опубликована!')

        return redirect(url_for('your_profile_page'))

    return render_template('forum/create_article.html')



@app.route('/your_profile/delete_article/<int:id>', methods=['POST', 'GET'])
def delete_article_page(id):
    """

    Функция для удаления статьи

    """
    session = SessionFactory()
    article = session.query(Article).filter_by(id=id).first()
    session.delete(article)
    session.commit()

    return redirect(url_for('your_profile_page'))



def main():
    Base.metadata.create_all(bind=engine)
    with Session(engine) as session:
        session.commit()



if __name__ == '__main__':
    app.run(debug=True)
    main()
