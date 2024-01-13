from flask import request
from flask_restful import Resource, reqparse

from sqlalchemy import desc

from models import User

from settings import SessionFactory


class UserAllResource(Resource):
    def get(self):
        session = SessionFactory()
        users = session.query(User).order_by(desc(User.created_at)).all()
        session.close()

        if users:

            users_list = []

            for user in users:

                if user.created_at:
                    users_list.append({
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'avatar': user.avatar,
                        'password': user.password,
                        'created_at': user.created_at.strftime('%Y-%m-%d %H:%M:%S')
                    })

                else:
                    users_list.append({
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'avatar': user.avatar,
                        'password': user.password,
                        'created_at': None
                    })
            return {'users': users_list}
        else:
            return {'message': 'No articles found'}, 404


    def post(self):

        data = request.json

        new_user = User(**data)

        session = SessionFactory()
        session.add(new_user)
        session.commit()
        session.close()

        return {'message': 'User created successfully'}, 201