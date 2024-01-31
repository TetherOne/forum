from werkzeug.utils import secure_filename

from flask_login import current_user

from sqlalchemy import update

from flask import redirect

from models import User

import os




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

