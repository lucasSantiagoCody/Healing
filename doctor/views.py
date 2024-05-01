from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Specialty, Doctor, OpenDate, Document
from django.contrib import messages
from django.contrib.messages import constants
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required, permission_required
from patient.models import MedicalAppointment
from .validations import is_doctor, validate_doctor_data
from django.contrib.auth.models import Group
from .decorators import doctor_required


@login_required
def register_doctor(request):
     
    is_doctor = Doctor.objects.filter(user__id=request.user.id).exists
    if is_doctor:
            messages.add_message(request, constants.WARNING, 'Você já está cadastrado como médico.')
            return redirect(reverse('open-schedules-view'))
    
    if request.method == 'GET':
        specialties =  Specialty.objects.all()
        return render(request, 'register_doctor.html',{
            'specialties': specialties,
            'is_doctor': is_doctor(request.user)
        })
    
    elif request.method == "POST":
        validation_erorrs = validate_doctor_data(request)
        if not validation_erorrs:
            medical_reservation_registration = request.POST.get('medical_reservation_registration')
            doctor_name = request.POST.get('doctor_name')
            address_code = request.POST.get('address_code')
            street = request.POST.get('street')
            neighborhood = request.POST.get('neighborhood')
            house_number = request.POST.get('house_number')
            # cim
            medical_identity_card = request.FILES.get('medical_identity_card')
            # rg
            medical_identification_card = request.FILES.get('medical_identification_card')
            profile_picture = request.FILES.get('profile_picture')
            description = request.POST.get('description')
            specialty_id = request.POST.get('specialty')
            consultation_fee = request.POST.get('consultation_fee')

            try:
                doctor = Doctor(
                    medical_reservation_registration=medical_reservation_registration,
                    doctor_name=doctor_name,
                    address_code=address_code,
                    street=street,
                    neighborhood=neighborhood,
                    house_number=house_number,
                    medical_identification_card=medical_identification_card,
                    medical_identity_card=medical_identity_card,
                    profile_picture=profile_picture,
                    user=request.user,
                    description=description,
                    specialty_id=specialty_id,
                    consultation_fee=consultation_fee
                )
                doctor_group, created = Group.objects.get_or_create(name='Doctor')
                user = request.user
                user.groups.add(doctor_group)
                doctor.save()
                messages.add_message(request, constants.SUCCESS, 'Cadastro médico realizado com sucesso.')  
                return redirect(reverse('open-schedules-view'))
            except Exception as err:
                print(err)
                messages.add_message(request, constants.ERROR, 'Não foi possível realizar o cadastro médico.')  
        else:
            # TODO analisar o que pode ser melhorado mais tarde
            if validation_erorrs['required_fields_not_found'] != []:
                messages.add_message(request, constants.ERROR, f"Required fields not found {str(validation_erorrs['required_fields_not_found']).replace("[", '').replace("]", '').replace("'", ' ')}")
            if validation_erorrs['empty_fields'] != []:
                messages.add_message(request, constants.ERROR, f"Empty fields {str(validation_erorrs['empty_fields']).replace("[", '').replace("]", '').replace("'", ' ')}" )
            if validation_erorrs['invalid_file_extension_fields'] != []:
                messages.add_message(request, constants.ERROR, f"Invalid file extension fields{str(validation_erorrs['invalid_file_extension_fields']).replace("[", '').replace("]", '').replace("'", ' ')}")
            
            
        return redirect(reverse('register-doctor-view'))

    
    
@login_required
@doctor_required
def open_schedules(request):
    doctor = Doctor.objects.get(user=request.user)
    if request.method == 'GET':
        doctor_data = Doctor.objects.get(user=request.user)
        open_dates = OpenDate.objects.filter(doctor=doctor)
        return render(request, 'open_schedules.html', {
            'doctor_data': doctor_data, 
            'open_dates': open_dates,
            'is_doctor': is_doctor(request.user)
            })
    
    elif request.method == 'POST':
        date = request.POST.get('date')
        formatted_date = datetime.strptime(date, "%Y-%m-%dT%H:%M")
        
        if formatted_date <= datetime.now():
            messages.add_message(request, constants.ERROR, 'A data deve ser maior ou igual a data atual.')
            return redirect(reverse('open-schedules-view'))
        else:
            
            open_date = OpenDate(
                date=date,
                doctor=doctor
            )
            open_date.save()
            messages.add_message(request, constants.SUCCESS, 'Horário cadastrado com sucesso.')
            return redirect(reverse('open-schedules-view'))
        

@login_required
@doctor_required
def doctors_medical_appointments(request):

    if request.method == 'GET':
        today = datetime.now().date()

        filter_by_specialties = request.GET.get('specialties')
        filter_by_date = request.GET.get('date')

        doctors_medical_appointments_today = MedicalAppointment.objects.filter(open_date__doctor__id=request.user.id
        ).filter(open_date__date__gt=today
        ).filter(open_date__date__lt=today + timedelta(days=1))
        
        remaining_doctors_medical_appointments = MedicalAppointment.objects.exclude(
        id__in=doctors_medical_appointments_today.values('id'))
        
        if filter_by_date:
            doctors_medical_appointments_today = doctors_medical_appointments_today.filter(open_date__date__date=filter_by_date)
            remaining_doctors_medical_appointments = remaining_doctors_medical_appointments.filter(open_date__date__date=filter_by_date)

        # Não faz sentido criar um filter por especialidade sabendo que o proprio medico tem 
        # apenas uma especialidade
        
        return render(request, 'doctors_medical_appointments.html', 
        {
            'doctors_medical_appointments_today': doctors_medical_appointments_today, 
            'remaining_doctors_medical_appointments': remaining_doctors_medical_appointments,
            'is_doctor': is_doctor(request.user)
        })
    
@login_required
@doctor_required
def medical_appointment_doctor_area(request, id):   
    if request.method == 'GET':
        context = {}
        context['medical_appointment'] = MedicalAppointment.objects.get(id=id)
        context['doctor_data'] = Doctor.objects.get(user=request.user)
        context['documents'] = Document.objects.filter(medical_appointment=id)
        context['is_doctor'] = is_doctor(request.user)
        return render(request, 'medical_appointment_doctor_area.html', context)
    
    if request.method == 'POST':

        # Inicializa a consulta + link da chamada
        medical_appointment = MedicalAppointment.objects.get(id=id)
        link = request.POST.get('link')

        if medical_appointment.status == 'cancelled':
            messages.add_message(request, constants.WARNING, 'Essa consulta já foi cancelada, você não pode inicia-la')
        elif medical_appointment.status == "completed":
            messages.add_message(request, constants.WARNING, 'Essa consulta já foi finalizada, você não pode inicia-la')
        else:
            medical_appointment.link = link
            medical_appointment.status = 'started'
            medical_appointment.save()
            messages.add_message(request, constants.SUCCESS, 'Consulta inicializada com sucesso.')

        return redirect(reverse('medical-appointment-doctor-area-view', kwargs={'id':id}))



@login_required
@doctor_required
def add_document(request, id):
    medical_appointment = MedicalAppointment.objects.get(id=id)
    if medical_appointment.open_date.user != request.user:
        messages.add_message(request, constants.ERROR, 'Essa consulta não é sua!')
        return redirect(reverse('medical-appointment-doctor-area-view', kwargs={'id':id}))
    
    title = request.POST.get('title')
    document = request.FILES.get('document')

    if document:
        document = Document(
            medical_appointment=medical_appointment,
            title=title,
            document=document
        )
        document.save()
        messages.add_message(request, constants.SUCCESS, 'Documento enviado com sucesso!')
    else:
        messages.add_message(request, constants.WARNING, 'Adicione o documento.')

    return redirect(reverse('medical-appointment-doctor-area-view', kwargs={'id':id}))

@login_required
@doctor_required
def finish_medical_appointment(request, id):
    medical_appointment = MedicalAppointment.objects.get(id=id)
    if request.user.id != medical_appointment.open_date.doctor.user.id:
        messages.add_message(request, constants.ERROR, 'Essa consulta não é sua')
        return redirect(reverse('open-schedules-view'))
    
    medical_appointment.status = 'completed'
    medical_appointment.save()
    return redirect(reverse('medical-appointment-doctor-area-view', kwargs={'id':id}))