from django.urls import path
from . import views

urlpatterns = [
    path('sign-up/', views.signup_view, name='sign-up-view'),
    path('login/', views.login_view, name='login-view'),
    path('logout/', views.logout_view, name='logout-view'),
    
]