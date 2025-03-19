from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('plant.urls')),
    path("herb/", include("herb.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
