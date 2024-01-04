from flask import Flask
from flask import redirect
from flask import url_for
from flask import render_template
from flask import request

from flask_login import logout_user
from flask_login import current_user
from flask_login import LoginManager

from sqlalchemy import create_engine, desc

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

from models import Base
from models import User
from models import Article

from views.create_and_check_article.check_form_fields_view import article_check_form_fields

from views.create_and_check_article.save_article_and_category_view import save_article_and_category

from views.main_page.main_page_view import upload_articles_and_categories

from views.register_and_login.get_login_fields_view import get_username_password

from views.register_and_login.get_register_fields_view import get_username_email_password

from views.register_and_login.login_view import login

from views.register_and_login.register_view import register_user

from views.update_article.get_fields_and_update_article_view import get_fields_and_update_article



app = Flask(__name__)


engine = create_engine(url='sqlite:///./db.sqlite3')
app.config['SECRET_KEY'] = 'forum'
SessionFactory = sessionmaker(bind=engine)



login_manager = LoginManager(app)
login_manager.init_app(app)



@login_manager.user_loader
def load_user(id):
    """

    Получение объекта пользователя по id из базы данных,
    "вспомогательная функция"

    """
    session = SessionFactory()

    return session.query(User).get(int(id))



@app.errorhandler(404)
def page_not_found(error):
    """

    Функция для обработки ошибки, при указании неправильного пути,
    используется шаблон forum/page_not_found_error.html

    """
    return render_template('forum/page_not_found_error.html', user=current_user)



@app.route('/', methods=['GET'])
def main_page():
    """

    Функция для отрисовки главной страницы сайта,
    используется шаблон forum/main_page.html

    """
    session = SessionFactory()
    articles = upload_articles_and_categories(session)

    return render_template('forum/main_page.html', articles=articles)



@app.route('/<int:id>/profile', methods=['GET'])
def user_profile_page(id):
    """

    Функция для просмотра профиля чужого пользователя

    """
    session = SessionFactory()
    user = session.query(User).filter_by(id=id).first()
    user_articles = session.query(Article).filter_by(user_id=id).order_by(desc(Article.created_at)).all()

    return render_template('forum/user_profile.html', user_articles=user_articles, user=user)



@app.route('/your_profile')
def your_profile_page():
    """

    Функция для отображения профиля пользователя,
    используется шаблон forum/your_profile.html

    """
    if current_user.is_authenticated:

        session = SessionFactory()
        current_user_id = current_user.id
        your_articles = session.query(Article).filter_by(user_id=current_user_id).order_by(desc(Article.created_at)).all()

        return render_template('forum/your_profile.html', articles=your_articles)

    return render_template('forum/your_profile.html')



@app.route('/register', methods=['POST', 'GET'])
def register_page():
    """

    Функция для отрисовки страницы регистрации сайта,
    используется шаблон auth/register.html

    """
    if request.method == 'POST':

        username, email, password = get_username_email_password(request)

        if not username or not email or not password:

            return render_template('auth/register.html', error='Заполните все поля')

        session = SessionFactory()

        register_user(session, username, email, password)

    return render_template('auth/register.html')



@app.route('/login', methods=['POST', 'GET'])
def login_page():
    """

    Функция для отрисовки страницы входа на сайт,
    используется шаблон auth/login.html

    """
    if request.method == 'POST':
        username, password = get_username_password(request)

        if not username or not password:

            return render_template('auth/login.html', error='Заполните все поля')

        session = SessionFactory()

        login(session, username, password)

        return redirect(url_for('your_profile_page'))

    return render_template('auth/login.html')



@app.route('/logout', methods=['POST', 'GET'])
def logout_page():
    """

    Функция для выхода из профиля,
    используется шаблон forum/your_profile.html

    """
    logout_user()

    return redirect(url_for('your_profile_page'))



@app.route('/your_profile/create_article', methods=['POST', 'GET'])
def create_article_page():
    """

    Функция для создания статьи,
    используется шаблон forum/create_article.html

    """
    if request.method == 'POST':
        if not article_check_form_fields(request):
            return render_template('forum/create_article.html', error='Заполните все поля')

        session = SessionFactory()

        save_article_and_category(session, request, current_user)

    return render_template('forum/create_article.html')



@app.route('/your_profile/delete_article/<int:id>', methods=['POST', 'GET'])
def delete_article_page(id):
    """

    Функция для удаления статьи,
    используется шаблон forum/your_profile_page.html

    """
    session = SessionFactory()
    article = session.query(Article).filter_by(id=id).first()
    session.delete(article)
    session.commit()

    return redirect(url_for('your_profile_page'))



@app.route('/your_profile/update_article/<int:id>', methods=['POST', 'GET'])
def update_article_page(id):
    """

    Функция для обновления статьи,
    используется шаблон forum/update_article.html

    """
    session = SessionFactory()
    article = session.query(Article).filter_by(id=id).first()

    if request.method == 'POST':

        get_fields_and_update_article(session, request, article)

        return redirect(url_for('your_profile_page'))

    else:

        return render_template('forum/update_article.html', article=article)



def main():
    Base.metadata.create_all(bind=engine)
    with Session(engine) as session:
        session.commit()



if __name__ == '__main__':
    app.run(debug=True)
    main()
