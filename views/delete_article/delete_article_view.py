from models import Article


def delete_article(session, id):
    """

    Функция для удаления статьи

    """
    article = session.query(Article).filter_by(id=id).first()
    session.delete(article)
    session.commit()