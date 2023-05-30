from django.urls import path
from . import views

urlpatterns = [

    # Paginas

    path('auditar/', views.auditar, name='auditar'),

    
]
