from flask_restful import Resource

from models import Article

from settings import SessionFactory


class ArticleResource(Resource):
    def get(self, id):
        session = SessionFactory()
        article = session.query(Article).filter_by(id=id).first()
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