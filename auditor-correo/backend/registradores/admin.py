from django.contrib import admin
from backend.registradores.models import Registro, Credenciales, Estatus_Mail, Estatus_PC, Estatus_Web

# Register your models here.
admin.site.register(Registro)
admin.site.register(Credenciales)
admin.site.register(Estatus_Mail)
admin.site.register(Estatus_Web)
admin.site.register(Estatus_PC)