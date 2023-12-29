

def login_check_form_fields(request):
    """

    Функция проверяет, заполнены ли все поля при входе пользователя

    """
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        return False
    else:
        return True