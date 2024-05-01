from django.urls import path
from . import views


urlpatterns = [
    path('register-doctor/', views.register_doctor, name='register-doctor-view'),
    path('open-schedules/', views.open_schedules, name='open-schedules-view'),
    path('doctors-medical-appointments/', views.doctors_medical_appointments, name='doctors-medical-appointments-view'),
    path('medical-appointment-doctor-area/<int:id>/', views.medical_appointment_doctor_area,   
          name='medical-appointment-doctor-area-view'),
    path('add-document/<int:id>/', views.add_document, name='add-document-view'),
    path('finish-medical-appointment/<int:id>/', views.finish_medical_appointment,
         name='finish-medical-appointment-view'),

]