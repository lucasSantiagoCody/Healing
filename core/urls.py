from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from patient.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('doctor/', include('doctor.urls')),
    path('patient/', include('patient.urls')),
    path('', home, name='home-view')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
