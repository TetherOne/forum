def get_username_password(request):

    username = request.form.get('username')
    password = request.form.get('password')

    return username, password