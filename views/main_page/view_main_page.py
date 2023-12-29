from models import Article
from models import Category



def upload_articles_and_categories(session):
    """

    Функция для получения статей и категорий из базы данных

    """
    articles = session.query(Article).all()
    categories = session.query(Category).all()

    return articles, categories