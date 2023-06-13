from django.urls import path
from . import views

urlpatterns = [

    # Paginas

    path('ruta/<str:int>', views.web_estatus, name='web-estatus'),
    path('logo/<int:int>', views.mail_status, name='mail-estatus'),

    
]
