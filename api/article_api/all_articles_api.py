from flask import request
from flask_restful import Resource
from sqlalchemy import desc

from models import Article
from settings import SessionFactory


class ArticleAllResource(Resource):
    """

    GET: получение списка всех статей,
    POST: создание статьи

    """
    @classmethod
    def get(cls):

        session = SessionFactory()
        articles = session.query(Article).order_by(desc(Article.created_at)).all()
        session.close()

        if articles:

            article_list = []

            for article in articles:

                article_list.append({
                    'id': article.id,
                    'name_of_article': article.name_of_article,
                    'text_of_article': article.text_of_article,
                    'category': article.category,
                    'created_at': article.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'user_id': article.user_id
                })

            return {'articles': article_list}

        else:

            return {'message': 'No articles found'}, 404



    @classmethod
    def post(cls):

        data = request.json

        new_article = Article(**data)

        session = SessionFactory()
        session.add(new_article)
        session.commit()
        session.close()

        return {'message': 'Article created successfully'}, 201