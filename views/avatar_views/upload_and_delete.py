from werkzeug.utils import secure_filename

from flask_login import current_user

from sqlalchemy import update

from flask import redirect

from models import User

import os



def delete_avatar(request, session):

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



def upload_avatar(request, session):

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