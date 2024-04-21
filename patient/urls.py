from django.urls import path
from . import views


urlpatterns = [
    path('choose-time/<int:id_doctor>/', views.choose_time, name='choose-time-view'),
    path('schedule-appointment/<int:id_open_date>/', views.schedule_appointment, name='schedule-appointment-view'),
    path('my-medical-appointments/', views.my_medical_appointments, name='my-medical-appointments-view'),
    path('medical_appointment/<int:id>/', views.medical_appointment, name='medical-appointment-view'),
    path('cancel-medical-appointment/<int:id>/', views.cancel_medical_appointment, name='cancel-medical-appointment-view'),
]