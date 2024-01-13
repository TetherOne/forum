from flask_restful import Resource

from models import User

from settings import SessionFactory


class UserResource(Resource):
    """

    API для получения пользователя по user_id

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