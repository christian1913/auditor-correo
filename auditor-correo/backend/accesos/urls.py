from django.urls import path
from . import views

urlpatterns = [
    path('acceso/<int:id>', views.index, name='acceso'),

]