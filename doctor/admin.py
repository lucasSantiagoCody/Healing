from django.contrib import admin
from .models import Doctor, Specialty, OpenDate


admin.site.register(Doctor)
admin.site.register(Specialty)
admin.site.register(OpenDate)