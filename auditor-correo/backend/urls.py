from django.urls import path, include


urlpatterns = [

    path('', include('backend.smtp.urls')),
    path('', include('backend.grupos.urls')),
    path('', include('backend.correos.urls')),
    path('', include('backend.plantillas.urls')),
    path('', include('backend.registradores.urls')),
    path('', include('backend.opciones.urls')),


]