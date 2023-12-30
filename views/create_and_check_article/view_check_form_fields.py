def article_check_form_fields(request):
    """

    Функция проверяет, заполнены ли все поля при создании статьи

    """
    name_of_article = request.form.get('name_of_article')
    text_of_article = request.form.get('text_of_article')
    category = request.form.get('category')

    if not name_of_article or not text_of_article or not category:

        return False
    else:

        return True