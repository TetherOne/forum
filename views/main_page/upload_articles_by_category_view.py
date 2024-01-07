from sqlalchemy import desc

from models import Article



def upload_articles_by_category(session, category):
    """

    Функция для фильтрации статей по категориям

    """
    articles = session.query(Article).filter(Article.category == category).order_by(desc(Article.created_at)).all()

    return articles
