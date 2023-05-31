from django.urls import path
from . import views

urlpatterns = [

        path('opciones', views.index, name='opciones'),
    
]