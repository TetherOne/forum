from flask import request
from flask_restful import Resource
from sqlalchemy import desc, create_engine
from sqlalchemy.orm import sessionmaker

from models import User
from settings import SessionFactory


class UserAllResource(Resource):
    """

    API for getting all users.

    ---
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: The ID of the user to retrieve.
    responses:
      404:
        description: User not found
    """
    @classmethod
    def get(cls):

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



    @classmethod
    def post(cls):

        data = request.json

        if isinstance(data, list):
            users = [User(**user_data) for user_data in data]

            session = SessionFactory()
            session.add_all(users)
            session.commit()
            session.close()

            return {'message': 'Users registered successfully'}, 201

        else:

            return {'message': 'Invalid data format. Expected a list of users.'}, 400