from django.urls import path
from . import views

urlpatterns = [

    # Paginas

    path('ruta/<str:int>', views.web_estatus, name='web-estatus'),
    path('logo/<int:int>/<str:imagen>', views.mail_status, name='mail-estatus'),
    path('registro-documento/<str:int>', views.pc_estatus, name='pc-estatus'),

    
]
