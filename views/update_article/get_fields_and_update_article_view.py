def get_fields_and_update_article(session, request, article):

    article.name_of_article = request.form['name_of_article']
    article.text_of_article = request.form['text_of_article']
    article.category = request.form['category']
    session.commit()