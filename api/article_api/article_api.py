from flask import request
from flask_restful import Resource
from sqlalchemy import desc

from models import Article

from settings import SessionFactory


class ArticleAllResource(Resource):
    """

    GET: для получения всех статей,
    POST: для создания статей

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

        if isinstance(data, list):
            articles = [Article(**article_data) for article_data in data]

            session = SessionFactory()
            session.add_all(articles)
            session.commit()
            session.close()

            return {'message': 'Articles created successfully'}, 201

        else:

            return {'message': 'Invalid data format. Expected a list of articles.'}, 400