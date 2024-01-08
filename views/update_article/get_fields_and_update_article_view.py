def get_fields_and_update_article(session, request, article):
    """

    Функция для получения полей,
    которые необходимы для обновления статьи

    """
    article.name_of_article = request.form['name_of_article']
    article.text_of_article = request.form['text_of_article']
    article.category = request.form['category']
    session.commit()