from flask import flash

from models import Article



def save_article_and_category(session, request, current_user):

    name_of_article = request.form.get('name_of_article')
    text_of_article = request.form.get('text_of_article')
    category = request.form.get('category')

    new_article = Article(name_of_article=name_of_article, category=category, text_of_article=text_of_article, user_id=current_user.id)

    session.add(new_article)
    session.commit()

    flash('Статья опубликована!')
