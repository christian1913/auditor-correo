from django.urls import path
from . import views

urlpatterns = [

    # Paginas

    path('', views.grupos, name='grupos'),

    
]