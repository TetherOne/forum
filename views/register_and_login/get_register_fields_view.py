def get_username_email_password(request):

    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    return username, email, password