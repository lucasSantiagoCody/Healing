from .models import Doctor

def is_doctor(user):
    if user.is_authenticated:
        return Doctor.objects.filter(user__id=user.id).exists()
    else:
        return None