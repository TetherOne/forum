from models import Article


def delete_article(session, id):

    article = session.query(Article).filter_by(id=id).first()
    session.delete(article)
    session.commit()