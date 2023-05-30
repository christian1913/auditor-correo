from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Grupos(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, null=True, blank=True)
    propietario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre