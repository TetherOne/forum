from views.update_article.get_fields_and_update_article_view import get_fields_and_update_article

from views.register_and_login_views.register_and_login import get_username_email_password
from views.register_and_login_views.register_and_login import get_username_password
from views.register_and_login_views.register_and_login import register_user
from views.register_and_login_views.register_and_login import login

from views.main_page_views.main_page_file import upload_articles_and_categories
from views.main_page_views.main_page_file import upload_articles_by_category
from views.main_page_views.main_page_file import upload_articles_by_search

from views.article_views.articles_crud import save_article_and_category
from views.article_views.articles_crud import article_check_form_fields

from views.avatar_views.upload_and_delete import delete_avatar
from views.avatar_views.upload_and_delete import upload_avatar

from api.article_api.id_articles_api import ArticleIDResource
from api.article_api.article_api import ArticleAllResource

from views.article_views.articles_crud import delete_article

from api.user_api.id_user_api import UserIDResource
from api.user_api.user_api import UserAllResource

from flask_login import LoginManager
from flask_login import current_user
from flask_login import logout_user

from settings import SessionFactory
from settings import engine
from settings import cache
from settings import app
from settings import api

from sqlalchemy.orm import Session

from flask import render_template
from flask import redirect
from flask import request
from flask import url_for
from flask import abort

from sqlalchemy import desc

from models import Article
from models import Base
from models import User



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

    return render_template('forum/page_not_found_error.html', user=current_user)



@app.route('/', methods=['GET'])
def main_page():

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

    session = SessionFactory()
    articles = session.query(Article).filter_by(id=article_id).all()
    if articles:

        article = articles[0]

        return render_template('forum/article_details.html', article=article)
    else:

        abort(404)



@app.route('/your_profile')
def your_profile_page():

    if current_user.is_authenticated:

        session = SessionFactory()
        current_user_id = current_user.id

        cache_key = f'articles_{current_user_id}'
        cached_articles = cache.get(cache_key)

        if cached_articles is not None:

            your_articles = cached_articles

        else:
            your_articles = session.query(Article).filter_by(user_id=current_user_id).order_by(desc(Article.created_at)).all()
            cache.set(cache_key, your_articles, timeout=30)

        return render_template('forum/your_profile.html', articles=your_articles)

    return render_template('forum/your_profile.html')



@app.route('/upload_avatar', methods=['POST'])
def upload_avatar_page():

    session = SessionFactory()

    upload_avatar(request, session)

    return redirect(url_for('your_profile_page'))



@app.route('/delete_avatar', methods=['POST'])
def delete_avatar_page():

    session = SessionFactory()

    delete_avatar(request, session)

    return redirect(url_for('your_profile_page'))



@app.route('/register', methods=['POST', 'GET'])
def register_page():

    if request.method == 'POST':

        username, email, password = get_username_email_password(request)

        if not username or not email or not password:

            return render_template('auth/register.html', error='Заполните все поля')

        session = SessionFactory()

        register_user(session, username, email, password)
        login(session, username, password)

        return redirect(url_for('your_profile_page'))

    return render_template('auth/register.html')



@app.route('/login', methods=['POST', 'GET'])
def login_page():

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

    logout_user()

    return redirect(url_for('your_profile_page'))



@app.route('/your_profile/create_article', methods=['POST', 'GET'])
def create_article_page():

    if request.method == 'POST':
        if not article_check_form_fields(request):
            return render_template('forum/create_article.html', error='Заполните все поля')

        session = SessionFactory()

        save_article_and_category(session, request, current_user)

        cache.delete(f'articles_{current_user.id}')

    return render_template('forum/create_article.html')



@app.route('/your_profile/delete_article/<int:id>', methods=['POST', 'GET'])
def delete_article_page(id):

    session = SessionFactory()

    delete_article(session, id)

    cache.delete(f'articles_{current_user.id}')

    return redirect(url_for('your_profile_page'))



@app.route('/your_profile/update_article/<int:id>', methods=['POST', 'GET'])
def update_article_page(id):

    session = SessionFactory()
    article = session.query(Article).filter_by(id=id).first()

    if request.method == 'POST':

        get_fields_and_update_article(session, request, article)

        cache.delete(f'articles_{current_user.id}')

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
