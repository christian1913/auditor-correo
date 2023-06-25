from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.contrib.auth.models import User
from django.contrib import messages 
from backend.registradores.models import Estatus_Mail, Estatus_PC, Estatus_Web
from backend.plantillas.models import Plantillas
from backend.correos.models import Correos
from backend.smtp.models import Enviados
from backend.accesos.models import Accesos
from backend.opciones.models import Emisores
import os
import random

@login_required(login_url='/accounts/login/')
def auditar(request):

    if request.POST['enviar'] == 'enviar':

        usuario = User.get_username(request.user)

        usuario = User.objects.get(username=usuario)
        correo = Correos.objects.get(id=request.POST['id'], propietario=usuario)
        plantilla = Plantillas.objects.get(id=request.POST['plantilla'])

        enviado = Enviados.objects.create(
            plantilla=plantilla,
            correo=correo,
            propietario=usuario
        )
        Accesos.objects.create(
            puerto=get_unique_port(),  
            enviado=enviado,
            correo=correo,
            propietario=usuario,

        )
        Estatus_Mail.objects.create(enviado=enviado)
        Estatus_Web.objects.create(enviado=enviado)
        Estatus_PC.objects.create(enviado=enviado)
        plantilla = Plantillas.objects.get(id=request.POST['plantilla'])


        messages.add_message(request, messages.SUCCESS, 'Correo enviado correctamente')
        # 1689d75e-0a56-463b-aaa1-4c741bdb26d5.clouding.host
        link_mail = 'http://192.168.21.130:8000/logo/'+ str(enviado.id)
        link_web = 'http://192.168.21.130:8000/ruta/' + str(enviado.id)


        asunto = plantilla.asunto
        contenido = plantilla.mensaje
        emisor = plantilla.emisor

        enviar(emisor, correo.correo, asunto, contenido, link_mail, link_web)
    else:
        messages.add_message(request, messages.ERROR, 'Introduce correctamente "enviar"')

    return redirect('correos', correo.grupo.id)


def enviar(emisor, destino, asunto, contenido, link_mail, link_web):
    mail_origen = emisor.correo
    password = emisor.contraseña
    mail_destino = destino

    contenido_mensaje = MIMEMultipart()
    contenido_mensaje['From'] = mail_origen
    contenido_mensaje['To'] = mail_destino
    contenido_mensaje['Subject'] = asunto

    contenido = contenido.replace("[mail.link]", link_mail)
    contenido = contenido.replace("[web.link]", link_web)

    contenido_mensaje.attach(MIMEText(contenido,"html"))
    email_string = contenido_mensaje.as_string()
    s = smtplib.SMTP(str(emisor.smtp),int(emisor.puerto))
    s.starttls()
    s.login(mail_origen, password)
    s.sendmail(mail_origen, mail_destino, email_string)
    s.quit()

    return

def get_unique_port():
    while True:
        puerto = str(random.randint(9000, 9999))
        if not Accesos.objects.filter(puerto=puerto).exists():
            return puerto