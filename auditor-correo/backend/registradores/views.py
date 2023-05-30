from django.shortcuts import render, redirect
from datetime import datetime
import geoip2.database
from user_agents import parse
from django.views.decorators.csrf import csrf_exempt
from django.http import FileResponse, Http404, JsonResponse, HttpResponse
from django.template import Context, Template
from backend.registradores.models import Registro, Estatus_Mail, Estatus_PC, Estatus_Web
from backend.plantillas.models import Plantillas
from backend.smtp.models import Enviados



def mail_status(request, int=None, imagen=None):

    enviado = Enviados.objects.get(id=int)
    data = registrar(request)

    registro = Registro.objects.filter(enviado=enviado).update(
        ip=data["ip"],
        user_agent=data["user_agent"],
        pais=data["pais"],
        agente=request.method,
        parametros=request.GET.dict(),
        sistema_operativo=data["sistema_operativo"],
        dispositivo=data["dispositivo"],
        idioma=data["idioma"],
        fecha=data["fecha"]
    )
    estatus_mail = Estatus_Mail.objects.create(enviado=enviado, registro=registro)


    try:
        plantilla_id = enviado.plantilla.id
        image = Plantillas.objects.get(id=plantilla_id).imagen

    except (Estatus_Mail.DoesNotExist, Plantillas.DoesNotExist):
        raise Http404("No se encontró la imagen")


    return FileResponse(open(image.path, 'rb'))



def web_estatus(request, int=None):

    if request.method == 'POST' and request.POST.get('descarga'):
        plantilla_id = request.POST['plantilla_id']
        archivo = Plantillas.objects.get(id=plantilla_id).archivo
        file_path = archivo.path
        return FileResponse(open(file_path, 'rb'))

    enviado = Enviados.objects.get(id=int)
    data = registrar(request)

    registro = Registro.objects.filter(enviado=enviado).update(
        ip=data["ip"],
        user_agent=data["user_agent"],
        pais=data["pais"],
        agente=request.method,
        parametros=request.GET.dict(),
        sistema_operativo=data["sistema_operativo"],
        dispositivo=data["dispositivo"],
        idioma=data["idioma"],
        fecha=data["fecha"]
    )
    estatus_web = Estatus_Web.objects.create(enviado=enviado, registro=registro)

    plantilla_id = Enviados.objects.get(id=int).plantilla.id
    html_content = Plantillas.objects.get(id=plantilla_id).plantilla
    template = Template(html_content)

    context = Context({

        'id': enviado.id,

    })
    rendered_html = template.render(context)

    return HttpResponse(rendered_html)





@csrf_exempt
def pc_estatus(request, int=None):

    if request.method == 'POST':

        enviado = Enviados.objects.get(id=int)
        data = registrar(request)

        registro = Registro.objects.filter(enviado=enviado).update(
            ip=data["ip"],
            user_agent=data["user_agent"],
            pais=data["pais"],
            agente=request.method,
            parametros=request.GET.dict(),
            sistema_operativo=data["sistema_operativo"],
            dispositivo=data["dispositivo"],
            idioma=data["idioma"],
            fecha=data["fecha"]
        )
        estatus_pc = Estatus_PC.objects.create(enviado=enviado, registro=registro)

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