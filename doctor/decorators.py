from functools import wraps
from django.contrib import messages
from django.contrib.messages import constants
from django.shortcuts import redirect
from django.urls import reverse


def doctor_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.groups.filter(name='Doctor').exists():
            return view_func(request, *args, **kwargs)
        else:
            messages.add_message(request, constants.ERROR, 'Somente médicos podem acessar esta página')
            return redirect(reverse('logout-view'))
        
    return wrapper