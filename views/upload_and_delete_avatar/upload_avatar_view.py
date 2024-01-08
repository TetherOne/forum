import os

from flask import flash, redirect
from flask_login import current_user

from sqlalchemy import update

from werkzeug.utils import secure_filename


from models import User


def upload_avatar(request, session):
    """

    Функция для загрузки аватарки

    """
    avatar_file = request.files.get('avatar')

    if avatar_file:

        avatar_filename = secure_filename(avatar_file.filename)
        avatar_path = os.path.join('static/', 'avatars', avatar_filename)
        avatar_file.save(avatar_path)

        current_user.avatar = f"avatars/{avatar_filename}"

        user_avatar = (
            update(User).
            where(User.id == current_user.id).
            values(avatar=current_user.avatar)
        )

        session.execute(user_avatar)
        session.commit()
    else:

        return redirect(request.url)

