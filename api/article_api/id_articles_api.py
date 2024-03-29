from flask import request
from flask_restful import Resource
from sqlalchemy import desc

from models import Article
from settings import SessionFactory


class ArticleIDResource(Resource):
    """

    GET: для получения статьи по article_id,
    DELETE: для удаления статьи

    """
    @classmethod
    def get(cls, article_id: int):

        session = SessionFactory()
        article = session.query(Article).filter_by(id=article_id).first()
        session.close()

        if article:

            return {
                'id': article.id,
                'name_of_article': article.name_of_article,
                'text_of_article': article.text_of_article,
                'category': article.category,
                'created_at': article.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'user_id': article.user_id}

        else:

            return {'message': 'Article not found'}, 404



    @classmethod
    def delete(cls, article_id: int):

        session = SessionFactory()
        article = session.query(Article).filter_by(id=article_id).first()

        if article:

            session.delete(article)
            session.commit()
            session.close()

            return {'message': 'Article deleted successfully'}

        else:

            session.close()

            return {'message': 'Article not found'}, 405