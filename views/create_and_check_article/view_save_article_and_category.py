from models import Category
from models import Article



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