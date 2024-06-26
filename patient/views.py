from django.shortcuts import render, redirect
from django.urls import reverse
from doctor.models import Doctor, Specialty, OpenDate
from .models import MedicalAppointment
from datetime import datetime
from django.contrib import messages
from django.contrib.messages import constants
from doctor.utils import is_doctor
from django.contrib.auth.decorators import login_required



def home(request):
    return render(request, 'home.html')

    
@login_required
def choose_time(request, doctor_id):
    
    if request.method == 'GET':
        doctor = Doctor.objects.get(id=doctor_id)
        open_schedules = OpenDate.objects.filter(doctor=doctor_id).filter(date__gte=datetime.now()).filter(scheduled=False)
        
        return render(request, 'choose_time.html', {
            'doctor': doctor, 
            'open_schedules': open_schedules,
            'is_doctor': is_doctor(request.user)
            })
        

@login_required
def schedule_medical_appointment(request, id_open_date):
    if request.method == 'GET':

        check_doctor_opened_date = OpenDate.objects.filter(doctor__user__id=request.user.id).values('doctor__user__id').first()

        if check_doctor_opened_date == request.user.id:
            messages.add_message(request, constants.WARNING, 'Doctores não devem agendar as suas próprias consultas')
            return redirect(reverse('home-view'))
        
        try:
            open_date = OpenDate.objects.get(id=id_open_date)
            medical_appointment = MedicalAppointment(patient=request.user, open_date=open_date)
            medical_appointment.status = 'scheduled'
            medical_appointment.save()

            open_date.scheduled = True
            open_date.save()

            messages.add_message(request,  constants.SUCCESS, 'Horário agendado com sucesso.')
        except:
            messages.add_message(request,  constants.ERROR, 'Não foi possível agendar o horário.')
        
            return redirect(reverse('choose_time', kwargs={'doctor_id'}))

        return redirect(reverse('patient-medical-appointments-view'))
    
@login_required
def patient_medical_appointments(request):
    if request.method == 'GET':
        filter_by_specialties = request.GET.get('specialties')
        filter_by_date = request.GET.get('date')

        medical_appointments = MedicalAppointment.objects.filter(patient=request.user)

        if filter_by_date:
            medical_appointments = medical_appointments.filter(open_date__date__date=filter_by_date)

        if filter_by_specialties:
            doctors_id = Doctor.objects.filter(specialty__specialty__icontains=filter_by_specialties
            ).values_list('user__id', flat=True)
            # doctors_id = doctors.values_list('user__id', flat=True)
            medical_appointments = medical_appointments.filter(open_date__doctor__id__in=doctors_id)
            
        
        return render(request, 'patient_medical_appointments.html', {
            'medical_appointments': medical_appointments,
            'is_doctor': is_doctor(request.user)
            })
    
@login_required
def medical_appointment(request, id):
    medical_appointment = MedicalAppointment.objects.get(id=id)
    doctor_data = Doctor.objects.get(id=medical_appointment.open_date.doctor_id)
    
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