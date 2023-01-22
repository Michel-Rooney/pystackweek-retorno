from django.conf.urls.static import static
from django.urls import path, include
from django.contrib import admin
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('apps.usuarios.urls')),
    path('divulgar/', include('apps.divulgar.urls')),
    path('adotar/', include('apps.adotar.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)