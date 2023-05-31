from django.urls import path
from . import views

urlpatterns = [

        path('plantillas', views.index, name='plantillas'),
        path('plantillas/añadir', views.añadir, name='añadir-plantilla'),
        path('plantillas/editar/<int:id>', views.editar, name='editar-plantilla'),
        path('plantillas/previsualizar-mensaje/<int:id>', views.previsualizar_mensaje, name='previsualizar-mensaje'),
        path('plantillas/previsualizar-plantilla/<int:id>', views.previsualizar_plantilla, name='previsualizar-plantilla'),
    
]