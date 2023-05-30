from django.db import models
from django.contrib.auth.models import User
from backend.grupos.models import Grupos


# Create your models here.

class Correos(models.Model):
    id = models.AutoField(primary_key=True)
    correo = models.EmailField(max_length=35)
    grupo = models.ForeignKey(Grupos, on_delete=models.CASCADE)
    propietario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.correo