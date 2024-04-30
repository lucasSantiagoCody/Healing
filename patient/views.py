from django.shortcuts import render, redirect
from django.urls import reverse
from doctor.models import Doctor, Specialty, OpenDate
from .models import MedicalAppointment
from datetime import datetime
from django.contrib import messages
from django.contrib.messages import constants
from doctor.validations import is_doctor
from django.contrib.auth.decorators import login_required



def home(request):

    if request.method == 'GET':
        doctors = Doctor.objects.all()
        specialties = Specialty.objects.all()
        filter_doctor = request.GET.get('doctor_name')
        filter_specialties = request.GET.getlist('specialty')

        if filter_doctor:
            doctors = doctors.filter(doctor_name__icontains=filter_doctor)

        if filter_specialties:
            doctors = doctors.filter(specialty_id__in=filter_specialties)
            
        return render(request, 'home.html', {
            'doctors': doctors, 
            'specialties': specialties,
            'is_doctor': is_doctor(request.user)
        })
    
@login_required
def choose_time(request, id_doctor):
    
    if request.method == 'GET':
        doctor = Doctor.objects.get(id=id_doctor)
        open_schedules = OpenDate.objects.filter(doctor__id=request.user.id).filter(date__gte=datetime.now()).filter(scheduled=False)
        return render(request, 'choose_time.html', {
            'doctor': doctor, 
            'open_schedules': open_schedules,
            'is_doctor': is_doctor(request.user)
            })
        

@login_required
def schedule_appointment(request, id_open_date):
    if request.method == 'GET':
        open_date = OpenDate.objects.get(id=id_open_date)
        print(open_date)
        
        try:
            schedule_appointment = MedicalAppointment(patient=request.user, open_date=open_date)
            schedule_appointment.save()

            if schedule_appointment:
                open_date.scheduled = True
                open_date.save()

            messages.add_message(request,  constants.SUCCESS, 'Horário agendado com sucesso.')
        except:
            messages.add_message(request,  constants.ERROR, 'Não foi possível agendar o horário.')
        

        return redirect(reverse('my-medical-appointments-view'))
    
@login_required
def patient_medical_appointments(request):
    if request.method == 'GET':
        filter_by_specialties = request.GET.get('specialties')
        filter_by_date = request.GET.get('date')

        medical_appointments = MedicalAppointment.objects.filter(patient=request.user)
        if filter_by_date:
            medical_appointments = medical_appointments.filter(open_date__date__date=filter_by_date)

        if filter_by_specialties:
            doctors = Doctor.objects.filter(specialty__specialty__icontains=filter_by_specialties)
            doctors_usernames = doctors.values_list('user__username', flat=True)
            
            medical_appointments = medical_appointments.filter(open_date__user__username__in=doctors_usernames)
        
        
        return render(request, 'patient_medical_appointments.html', {
            'medical_appointments': medical_appointments,
            'is_doctor': is_doctor(request.user)
            })
    
@login_required
def medical_appointment(request, id):
    medical_appointment = MedicalAppointment.objects.get(id=id)
    doctor_data = Doctor.objects.get(user=medical_appointment.open_date.user)
    
    return render(request, 'medical_appointment.html', {
        'medical_appointment': medical_appointment, 
        'doctor_data': doctor_data,
        'is_doctor': is_doctor(request.user)})

@login_required
def cancel_medical_appointment(request, id):
    medical_appointment = MedicalAppointment.objects.get(id=id)
    medical_appointment.status = 'cancelled'
    medical_appointment.save()
    return redirect(reverse('medical-appointment-view', kwargs={'id':id}))