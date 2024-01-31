from models import Article

from sqlalchemy import desc

from sqlalchemy import or_



def upload_articles_by_search(session, search_query):

    articles = session.query(Article).filter(or_(Article.name_of_article.ilike(f"%{search_query}%"))).order_by(desc(Article.created_at)).all()

    return articles



def upload_articles_and_categories(session):

    articles = session.query(Article).order_by(desc(Article.created_at)).all()

    return articles



def upload_articles_by_category(session, category):

    articles = session.query(Article).filter(Article.category == category).order_by(desc(Article.created_at)).all()

    return articles
