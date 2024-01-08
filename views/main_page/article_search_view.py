from sqlalchemy import or_, desc

from models import Article



def upload_articles_by_search(session, search_query):
    articles = session.query(Article).filter(or_(Article.name_of_article.ilike(f"%{search_query}%"))).order_by(desc(Article.created_at)).all()
    return articles