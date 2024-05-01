from .models import Doctor

def is_doctor(user):
    if user.is_authenticated:
        return Doctor.objects.filter(user=user).exists()
    else:
        return None