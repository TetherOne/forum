from flask import abort
from flask import redirect
from flask import url_for
from flask import render_template
from flask import request

from flask_login import logout_user
from flask_login import current_user
from flask_login import LoginManager

from sqlalchemy import desc

from sqlalchemy.orm import Session

from api.article_api.all_articles_api import ArticleIDResource
from api.article_api.article_api import ArticleAllResource

from api.user_api.all_user_api import UserIDResource
from api.user_api.user_api import UserAllResource

from models import Base
from models import User
from models import Article

from settings import SessionFactory
from settings import engine
from settings import app
from settings import api

from views.create_and_check_article.check_form_fields_view import article_check_form_fields
from views.create_and_check_article.save_article_and_category_view import save_article_and_category

from views.delete_article.delete_article_view import delete_article

from views.main_page.article_search_view import upload_articles_by_search
from views.main_page.main_page_view import upload_articles_and_categories
from views.main_page.upload_articles_by_category_view import upload_articles_by_category

from views.register_and_login.get_login_fields_view import get_username_password
from views.register_and_login.get_register_fields_view import get_username_email_password
from views.register_and_login.login_view import login
from views.register_and_login.register_view import register_user

from views.update_article.get_fields_and_update_article_view import get_fields_and_update_article

from views.upload_and_delete_avatar.delete_avatar_view import delete_avatar
from views.upload_and_delete_avatar.upload_avatar_view import upload_avatar



api.add_resource(UserAllResource, '/api/users')
api.add_resource(UserIDResource, '/api/users/<int:user_id>')
api.add_resource(ArticleAllResource, '/api/articles')
api.add_resource(ArticleIDResource, '/api/articles/<int:article_id>')



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

    Функция для отрисовки главной страницы,
    используется функция фильтрации статей по категориям,
    используется шаблон forum/main_page.html

    """
    session = SessionFactory()
    category_filter = request.args.get('category', None)
    search_query = request.args.get('search', None)

    if category_filter:

        articles = upload_articles_by_category(session, category_filter)

    elif search_query:

        articles = upload_articles_by_search(session, search_query)

    else:

        articles = upload_articles_and_categories(session)

    categories = session.query(Article.category).distinct().all()

    return render_template('forum/main_page.html',
                           articles=articles,
                           categories=categories,
                           selected_category=category_filter,
                           search_query=search_query)



@app.route('/article-details/<int:article_id>', methods=['GET'])
def article_details_page(article_id):
    """

    Функция для отрисовки деталей статьи,
    используется шаблон forum/article_details.html

    """
    session = SessionFactory()
    articles = session.query(Article).filter_by(id=article_id).all()
    if articles:

        article = articles[0]

        return render_template('forum/article_details.html', article=article)
    else:

        abort(404)



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



@app.route('/upload_avatar', methods=['POST'])
def upload_avatar_page():
    """

    Функция для загрузки аватарки пользователя,
    используется шаблон forum/your_profile.html

    """
    session = SessionFactory()

    upload_avatar(request, session)

    return redirect(url_for('your_profile_page'))



@app.route('/delete_avatar', methods=['POST'])
def delete_avatar_page():
    """

    Функция для удаления аватарки пользователя,
    используется шаблон forum/your_profile.html

    """
    session = SessionFactory()

    delete_avatar(request, session)

    return redirect(url_for('your_profile_page'))



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

    delete_article(session, id)

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
