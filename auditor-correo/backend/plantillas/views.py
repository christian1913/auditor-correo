from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.clickjacking import xframe_options_exempt
from django.contrib import messages 
from .models import Plantillas
from django.http import HttpResponse
from django.template import Template, Context
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from backend.opciones.models import Emisores

##### PLANTILLAS #####


@login_required(login_url='/accounts/login/')
def index(request):


    if request.method == 'GET':
        
        datos = obtener_datos_plantillas(request)
        data = {
            'datos' : datos
        }

    elif request.method == 'POST':

        # Eliminar plantilla

        if request.POST['instruccion'] == 'eliminar-plantilla':

            eliminar_plantilla(request)

        else:
            pass


        datos = obtener_datos_plantillas(request)

        data = {
            'datos' : datos
        }

    else:

        data = obtener_datos_plantillas(request)
        data = {
            'datos' : datos
        }

    return render(request, 'backend/plantillas/index.html', data)


@login_required(login_url='/accounts/login/')
def añadir(request):
    emisores = Emisores.objects.filter(propietario=request.user)

    if request.method == "POST":
        nombre = request.POST['nombre']
        if Plantillas.objects.filter(nombre=nombre, propietario=request.user).exists():
            messages.error(request, 'Ya existe una plantilla con este nombre.')
            return redirect('añadir-plantilla')

        try:
            emisor = Emisores.objects.get(id=request.POST['emisor'], propietario=request.user)
            
            plantilla = Plantillas()
            plantilla.tipo = request.POST['tipo']
            plantilla.nombre = nombre
            plantilla.asunto = request.POST['asunto']
            plantilla.mensaje = request.POST['mensaje']
            if 'imagen' in request.FILES:
                plantilla.imagen = request.FILES['imagen']
            plantilla.plantilla = request.POST['plantilla']
            plantilla.redireccion = request.POST['redireccion']
            plantilla.emisor = emisor
            plantilla.propietario = request.user
            
            plantilla.full_clean()  
            plantilla.save()
                
            messages.success(request, 'Plantilla añadida exitosamente')
            return redirect('plantillas')
            
        except ValidationError as e:

            error_messages = e.message_dict
            for field, errors in error_messages.items():
                for error in errors:
                    messages.error(request, f"Error en {field}: {error}")
        except Exception as e:

            messages.error(request, str(e))
        
    context = {
        'emisores': emisores,
    }

    return render(request, 'backend/plantillas/añadir-plantilla.html', context)






@login_required(login_url='/accounts/login/')
def editar(request, id=None):
    plantilla = Plantillas.objects.get(id=id, propietario=request.user)
    emisores = Emisores.objects.filter(propietario=request.user)

    if request.method == "POST":
        print(request.POST['emisor'])
        try:
            emisor = Emisores.objects.get(id=request.POST['emisor'],propietario=request.user)
            plantilla.tipo = request.POST['tipo']
            plantilla.nombre = request.POST['nombre']
            plantilla.asunto = request.POST['asunto']
            plantilla.mensaje = request.POST['mensaje']

            if 'imagen' in request.FILES:
                plantilla.imagen = request.FILES['imagen']

            plantilla.plantilla = request.POST['plantilla']
            plantilla.redireccion = request.POST['redireccion']
            plantilla.emisor = emisor  # <- Change is here

            plantilla.full_clean()  
            plantilla.save()
                
            messages.success(request, 'Plantilla actualizada exitosamente')
            return redirect('plantillas')
            
        except ValidationError as e:


            error_messages = e.message_dict
            for field, errors in error_messages.items():
                for error in errors:
                    messages.error(request, f"Error en {field}: {error}")
        except Exception as e:

            messages.error(request, str(e))

    context = {
        'plantilla': plantilla,
        'emisores': emisores,
    }

    return render(request, 'backend/plantillas/editar-plantilla.html', context)




# Funcion obtener datos

@login_required(login_url='/accounts/login/')
def obtener_datos_plantillas(request):
    usuario = User.get_username(request.user)
    datos = list(Plantillas.objects.filter(propietario__username=usuario))
    return datos




# Funciones post


@login_required(login_url='/accounts/login/')
def crear_plantilla(request):

    usuario = User.get_username(request.user)
    comprabacion = Plantillas.objects.filter(servicio=request.POST['servicio'], propietario__username=usuario)
    if comprabacion: 
        messages.add_message(request, messages.ERROR, 'Error al crear la plantilla o la plantilla ya existe')
    else:
        usuario = User.objects.get(username=usuario)
        Plantillas.objects.create(
            servicio=request.POST['servicio'],
            asunto=request.POST['asunto'],
            mensaje=request.POST['mensaje'],
            login=request.POST['login'],
            imagenes_login=request.POST['imagenes-login'],
            propietario=usuario)
        messages.add_message(request, messages.SUCCESS, 'Plantilla creada correctamente')
    return 


@login_required(login_url='/accounts/login/')
def eliminar_plantilla(request):

    if request.POST['eliminar'] == 'eliminar':
        try:
            plantilla_obj = Plantillas.objects.filter(id=request.POST['id'])
            plantilla_obj.delete()
            messages.add_message(request, messages.SUCCESS, 'plantilla eliminada correctamente')

        except:
            messages.add_message(request, messages.ERROR, 'No se ha podido borrar la plantilla')
    else:
        messages.add_message(request, messages.ERROR, 'No se ha introducido delete correctamente. La plantilla no se eliminará.')

    return 


@xframe_options_exempt
@login_required
def previsualizar_mensaje(request, id=None):
    plantilla = get_object_or_404(Plantillas, id=id, propietario=request.user)
    html_content = plantilla.mensaje

    try:
        template = Template(html_content)
        context = Context({

            'id': 'None',


        })
        rendered_html = template.render(context)
    except Exception as e:
        return HttpResponse(f"Error al renderizar el mensaje: {e}")

    return HttpResponse(rendered_html)

@xframe_options_exempt
@login_required
def previsualizar_plantilla(request, id=None):
    plantilla = get_object_or_404(Plantillas, id=id, propietario=request.user)
    html_content = plantilla.plantilla

    try:
        template = Template(html_content)
        context = Context({

            'id': 'None',


        })
        rendered_html = template.render(context)
    except Exception as e:
        return HttpResponse(f"Error al renderizar la plantilla: {e}")

    return HttpResponse(rendered_html)