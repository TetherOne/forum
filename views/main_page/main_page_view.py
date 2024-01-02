from models import Article



def upload_articles_and_categories(session):
    """

    Функция для получения статей и категорий из базы данных

    """
    articles = session.query(Article).all()

    return articles