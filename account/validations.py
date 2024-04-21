from .models import CustomUser
from django.contrib import messages
from django.contrib.messages import constants

def validate(data):
    email = data['email'].strip()
    username = data['username'].strip()
    password = data['password'].strip()
    confirm_password = data['password_confirm'].strip()
    exceptions = []


    if not email:
        exceptions.append('The E-mail field should not be empty')
    if not username:
        exceptions.append('The username field should not be empty')
    if confirm_password != password:
        exceptions.append("The passwords didn't match")
    if len(password) < 6:
        exceptions.append('Password too weak, min 6 chacaracters')

    verify_user_exists = CustomUser.objects.filter(email=email)
    if verify_user_exists.exists():
        exceptions.append('That E-mail is already taken')

    exceptions_and_data = {
        'exceptions': exceptions or None,
        'validated_data': data
    }

    return exceptions_and_data