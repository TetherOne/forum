import os

from flask_login import current_user

from models import User



def delete_avatar(request, session):
    """

    Функция для удаления аватарки

    """
    current_user_obj = current_user

    if current_user_obj.avatar:

        avatar_path = os.path.join('static/', current_user_obj.avatar)

        if os.path.exists(avatar_path):

            os.remove(avatar_path)

        current_user_obj.avatar = None

        user_avatar = (
            session.query(User).
            filter(User.id == current_user_obj.id).
            update({"avatar": None})
        )

        session.commit()