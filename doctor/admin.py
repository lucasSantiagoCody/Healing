from django.contrib import admin
from .models import DoctorData, Specialty, OpenDate


admin.site.register(DoctorData)
admin.site.register(Specialty)
admin.site.register(OpenDate)