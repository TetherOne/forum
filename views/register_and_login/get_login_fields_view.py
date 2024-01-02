def get_username_password(request):
    """

    Функция получает username, password из формы login.html

    """
    username = request.form.get('username')
    password = request.form.get('password')

    return username, password