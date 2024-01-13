from flask import request
from flask_restful import Resource, reqparse

from models import User
from settings import SessionFactory


class UserResource(Resource):
    def get(self, user_id):
        session = SessionFactory()
        user = session.query(User).filter_by(id=user_id).first()
        session.close()

        if user:
            return {'username': user.username,
                    'email': user.email,
                    'avatar': user.avatar}
        else:
            return {'message': 'User not found'}, 404

