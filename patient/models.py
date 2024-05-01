from django.db import models
from doctor.models import OpenDate
from account.models import CustomUser




class MedicalAppointment(models.Model):
    STATUS_CHOICES = (
        ('scheduled', 'Scheduled'),
        ('finished', 'Finished'),
        ('cancelled', 'Cancelled'),
        ('started', 'Started')
    )

    patient = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    open_date = models.ForeignKey(OpenDate, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    link = models.URLField(null=True, blank=True)

    @property
    def get_status_display(self):
        return self.status

    def __str__(self):
        return self.patient.username
