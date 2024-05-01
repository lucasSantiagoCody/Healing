from django.urls import path
from . import views


urlpatterns = [
    path('choose-time/<int:doctor_id>/', views.choose_time, name='choose-time-view'),
    path('schedule-medical-appointment/<int:id_open_date>/', views.schedule_medical_appointment, name='schedule-medical-appointment-view'),
    path('patient-medical-appointments/', views.patient_medical_appointments, name='patient-medical-appointments-view'),
    path('medical_appointment/<int:id>/', views.medical_appointment, name='medical-appointment-view'),
    path('cancel-medical-appointment/<int:id>/', views.cancel_medical_appointment, name='cancel-medical-appointment-view'),
]