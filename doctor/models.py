from django.db import models
from account.models import CustomUser
from datetime import datetime


class Specialty(models.Model):
    specialty = models.CharField(max_length=100)
    icon = models.ImageField(upload_to='icons')

    def __str__(self):
        return self.specialty
    

class Doctor(models.Model):
    medical_reservation_registration = models.CharField(max_length=30)
    doctor_name = models.CharField(max_length=100)
    address_code = models.CharField(max_length=15)
    street = models.CharField(max_length=100)
    neighborhood = models.CharField(max_length=100)
    house_number = models.IntegerField()
    # rg
    medical_identification_card = models.ImageField(upload_to='medical_identification_cards')
    # cim
    medical_identity_card = models.ImageField(upload_to='medical_identity_cards')
    profile_picture = models.ImageField(upload_to='profile_pictures')
    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    specialty = models.ForeignKey(Specialty, on_delete=models.DO_NOTHING)
    consultation_fee = models.FloatField(default=100)

    @property
    def next_date(self):
        next_date = OpenDate.objects.filter(doctor=self.id).filter(scheduled=False
        ).filter(date__gt=datetime.now()).first()

        return next_date
    
    def __str__(self):
        return self.user.username
    
class OpenDate(models.Model):
    date = models.DateTimeField()
    doctor = models.ForeignKey(Doctor, on_delete=models.DO_NOTHING)
    scheduled = models.BooleanField(default=False) 

    def __str__(self):
        return str(self.date)

from patient.models import MedicalAppointment

class Document(models.Model):
    medical_appointment = models.ForeignKey(MedicalAppointment, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=30)
    document = models.FileField(upload_to='documents')

    def __str__(self):
        return self.title