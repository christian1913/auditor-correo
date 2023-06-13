from django.db import models
from django.contrib.auth.models import User
from backend.smtp.models import Enviados
from backend.correos.models import Correos

# Create your models here.


class Accesos(models.Model):
    fecha_acceso = models.DateTimeField(auto_now_add=True)
    puerto = models.CharField(max_length=10)
    estatus = models.BooleanField(default=False)
    enviado = models.ForeignKey(Enviados, on_delete=models.CASCADE)
    correo = models.ForeignKey(Correos, on_delete=models.CASCADE)
    propietario = models.ForeignKey(User, on_delete=models.CASCADE)      

    def __str__(self):
        return str(self.id)
    
