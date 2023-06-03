from django.db import models
from django.contrib.auth.models import User
from backend.opciones.models import Emisores

# Create your models here.
 

class Plantillas(models.Model):

    OPCIONES = [
        ('phishing', 'phishing'),
        ('script', 'script'),
    ]

    id = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=20, choices=OPCIONES)
    nombre = models.CharField(max_length=50)
    asunto = models.CharField(max_length=100)
    mensaje = models.TextField()
    imagen = models.ImageField(upload_to='imagenes')
    plantilla = models.TextField()
    redireccion = models.CharField(max_length=200, null=True, blank=True)
    script = models.TextField(null=True, blank=True)
    emisor = models.ForeignKey(Emisores, on_delete=models.CASCADE)
    propietario = models.ForeignKey(User, null=True, on_delete=models.CASCADE)  

    def __str__(self):
        return self.nombre