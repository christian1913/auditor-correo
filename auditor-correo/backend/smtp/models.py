from django.db import models
from django.contrib.auth.models import User
from backend.plantillas.models import Plantillas
from backend.correos.models import Correos

# Create your models here.


class Enviados(models.Model):
    fecha_envio = models.DateTimeField(auto_now_add=True)
    plantilla = models.ForeignKey(Plantillas, on_delete=models.CASCADE)
    correo = models.ForeignKey(Correos, on_delete=models.CASCADE)
    propietario = models.ForeignKey(User, on_delete=models.CASCADE)      

    def __str__(self):
        return str(self.id)
    
