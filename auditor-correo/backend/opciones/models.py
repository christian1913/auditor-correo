from django.db import models
from django.contrib.auth.models import User

# Create your models here.
 
class Emisores(models.Model):
    id = models.AutoField(primary_key=True)
    correo = models.EmailField(max_length=35)
    contraseña = models.CharField(max_length=25)
    smtp = models.CharField(max_length=35)
    puerto = models.CharField(max_length=10)
    propietario = models.ForeignKey(User, null=True,on_delete=models.CASCADE)  
    
    def __str__(self):
        return self.correo 