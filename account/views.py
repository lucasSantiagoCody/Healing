from django.shortcuts import render, redirect
from django.urls import reverse
from .validations import validate_signup_request_data
from django.views.generic import View
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import CustomUser

def signup_view(request):
    
    if request.method == 'GET':   
        return render(request, 'sign_up.html')
    
    elif request.method == 'POST':
        
        validation_errors = validate_signup_request_data(request)
        
        if validation_errors:
            for v_error in validation_errors:
                messages.add_message(request, constants.ERROR, v_error)
            return redirect(reverse('sign-up-view'))
        else:
            try:
                email = request.POST.get('email')
                username = request.POST.get('username')
                password = request.POST.get('password')
                user = CustomUser.objects.create_user(
                    email=email,
                    password=password,
                    username=username
                )
                user.save()
                messages.add_message(request, constants.SUCCESS, 'Successfully created account')
            except Exception as err:
                print(err)
                messages.add_message(request, constants.ERROR, 'Internal error system')

            return redirect(reverse('login-view'))
        
def login_view(request):
    
    if request.method == 'GET':
        return render(request, "login.html")
    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(username=email, password=password)

        if user:
            login(request, user)
            messages.add_message(request, constants.SUCCESS, 'Now, Are you loggedin :)')
        else:
            verify_email_exists = CustomUser.objects.filter(email=email)
            if verify_email_exists:
                messages.add_message(request, constants.ERROR, 'Wrong password!')
            else:
                messages.add_message(request, constants.ERROR, 'This account does not exist!')
        return redirect(reverse('home-view'))

def logout_view(request):
    try:
        logout(request) 
        messages.add_message(request, constants.ERROR, 'Now you are disconnected!')
    except:
        messages.add_message(request, constants.ERROR, 'Internal system error!')
    return redirect(reverse('login-view'))

