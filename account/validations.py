from .models import CustomUser
from django.contrib import messages
from django.contrib.messages import constants
import re


def validate_signup_request_data(request):
    data = request.POST
    email = data['email'].strip()
    username = data['username'].strip()
    password = data['password'].strip()
    confirm_password = data['password_confirm'].strip()
    validation_errors = []
    valid_email = "r[1]+@[a-zA-Z0-9.-]+.[a-zA-Z]{2,}$"
    
    if not email:
        validation_errors.append('The E-mail field should not be empty')
    if not re.serach(valid_email, email):
        validation_errors.append('This E-mail is invalid!')
    if not username:
        validation_errors.append('The username field should not be empty')
    if confirm_password != password:
        validation_errors.append("The passwords didn't match")
    if len(password) < 6:
        validation_errors.append('Password too weak, min 6 chacaracters')

    verify_user_exists = CustomUser.objects.filter(email=email)

    if verify_user_exists.exists():
        validation_errors.append('That E-mail is already taken')

    
    if validation_errors:
        return validation_errors