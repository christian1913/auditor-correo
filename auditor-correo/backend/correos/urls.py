from django.urls import path
from . import views

urlpatterns = [

    # Paginas

    path('grupos/<str:id>', views.correos, name='correos'),

    
]
