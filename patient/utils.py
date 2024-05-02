

def is_patient(user):
    if user.is_authenticated:
        return user.groups.filter(name='Patient').exists()
    else: 
        return None