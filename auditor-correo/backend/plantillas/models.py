from django.db import models
from django.contrib.auth.models import User


# Create your models here.
 
class Emisores(models.Model):
    id = models.AutoField(primary_key=True)
    correo = models.EmailField(max_length=35)
    contraseña = models.CharField(max_length=25)
    smtp = models.CharField(max_length=35)
    puerto = models.CharField(max_length=10)
    propietario = models.ForeignKey(User, on_delete=models.CASCADE)  
    
    def __str__(self):
        return self.correo 

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
    imagen = models.ImageField(upload_to='ruta/para/subir/')
    plantilla = models.TextField()
    script = models.TextField(null=True, blank=True)
    emisor = models.ForeignKey(Emisores, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre