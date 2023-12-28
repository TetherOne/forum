from models import Article
from models import Category



def check_form_fields(request):
    """

    Функция проверяет, заполнены ли все поля при создании статьи

    """
    name_of_article = request.form.get('name_of_article')
    text_of_article = request.form.get('text_of_article')
    category = request.form.get('category')

    if not name_of_article or not text_of_article or not category:
        return False
    else:
        return True



def save_article_and_category(session, name_of_article, text_of_article, category, current_user):
    """

    Функция сохраняет статью и ее категорию в базе данных

    """
    new_article = Article(name_of_article=name_of_article, text_of_article=text_of_article, user_id=current_user.id)

    session.add(new_article)
    session.commit()

    new_category = Category(name_of_category=category, article_id=new_article.id)

    session.add(new_category)
    session.commit()