from flask import request

from flask_restful import Resource

from sqlalchemy import desc

from models import User

from settings import SessionFactory



class UserIDResource(Resource):
    """

    API for getting user by user_id.

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
    def get(cls, user_id: int):

        session = SessionFactory()
        user = session.query(User).filter_by(id=user_id).first()
        session.close()

        if user:

            if user.created_at:

                return {'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'avatar': user.avatar,
                        'password': user.password,
                        'created_at': user.created_at.strftime('%Y-%m-%d %H:%M:%S')
                        }

            else:

                return {'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'avatar': user.avatar,
                        'password': user.password,
                        'created_at': None
                        }

        else:

            return {'message': 'User not found'}, 404



