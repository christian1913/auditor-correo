from django.db import models
from django.contrib.auth.models import User
from backend.smtp.models import Enviados


# Create your models here.



class Estatus_Mail(models.Model):
    ip = models.GenericIPAddressField(blank=True, null=True)
    agente = models.TextField(blank=True, null=True)
    pais = models.CharField(max_length=100,blank=True, null=True)
    metodo = models.CharField(max_length=10,blank=True, null=True)
    parametros = models.TextField(blank=True, null=True)
    sistema_operativo = models.CharField(max_length=100,blank=True, null=True)
    dispositivo = models.CharField(max_length=100,blank=True, null=True)
    idioma = models.CharField(max_length=100, blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    enviado = models.ForeignKey(Enviados, on_delete=models.CASCADE)


    def __str__(self):
        return f'LogEntry #{self.id}'

class Estatus_Web(models.Model):
    ip = models.GenericIPAddressField(blank=True, null=True)
    agente = models.TextField(blank=True, null=True)
    pais = models.CharField(max_length=100,blank=True, null=True)
    metodo = models.CharField(max_length=10,blank=True, null=True)
    parametros = models.TextField(blank=True, null=True)
    sistema_operativo = models.CharField(max_length=100,blank=True, null=True)
    dispositivo = models.CharField(max_length=100,blank=True, null=True)
    idioma = models.CharField(max_length=100, blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    enviado = models.ForeignKey(Enviados, on_delete=models.CASCADE)


    def __str__(self):
        return f'LogEntry #{self.id}'
    
    

class Credenciales(models.Model):
    usuario = models.CharField(max_length=25)
    contraseña = models.CharField(max_length=25)
    estatus_web = models.ForeignKey(Estatus_Web, on_delete=models.CASCADE)   

    def __str__(self):
        return str(self.id)