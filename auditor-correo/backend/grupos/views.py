from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages 
from backend.grupos.models import Grupos


@login_required(login_url='/accounts/login/')
def index(request):


    if request.method == 'GET':
        
        datos = obtener_datos_grupos(request)

        data = {
        
            'datos' : datos,
        }

    elif request.method == 'POST':

        # Crear grupo

        if request.POST['instruccion'] == 'crear-grupo':

            crear_grupo(request)

        # Editar grupo     

        elif request.POST['instruccion'] == 'editar-grupo':

            editar_grupo(request)

        # Eliminar grupo

        elif request.POST['instruccion'] == 'eliminar-grupo':

            eliminar_grupo(request)

        else:
            
            print('ninguna seleccion es correcta')
            messages.add_message(request, messages.ERROR, 'Error en la peticion"')

        datos = obtener_datos_grupos(request)
        data = {
        
            'datos' : datos,
        }

    else:

        print('NO ES UN GET NI UN POST')
        datos = obtener_datos_grupos(request)
        messages.add_message(request, messages.ERROR, 'Error en la peticion"')

        data = {
        
            'datos' : datos,
        }

    return render(request, 'backend/grupos/index.html', data)


# Funcion obtener datos
@login_required(login_url='/accounts/login/')
def obtener_datos_grupos(request):
    usuario = User.get_username(request.user)
    datos = Grupos.objects.filter(propietario__username=usuario)
    print(datos)
    return datos


# Funciones post


@login_required(login_url='/accounts/login/')
def crear_grupo(request):

    usuario = User.get_username(request.user)
    comprabacion = Grupos.objects.filter(nombre=request.POST['nombre'], propietario__username=usuario)
    if comprabacion: 
        messages.add_message(request, messages.ERROR, 'Error al crear el grupo o el grupo ya existe')
    else:
        usuario = User.objects.get(username=usuario)
        Grupos.objects.create(nombre=request.POST['nombre'], propietario=usuario)
        messages.add_message(request, messages.SUCCESS, 'grupo creado correctamente')
    return

@login_required(login_url='/accounts/login/')
def editar_grupo(request):

    try:

        nombre = request.POST['nombre']
        id = request.POST['id']
        usuario = User.get_username(request.user)
        usuario = User.objects.get(username=usuario)
        Grupos.objects.filter(id=id, propietario=usuario).update(nombre=nombre)
        messages.add_message(request, messages.SUCCESS, 'Grupo editado correctamente')

    except: 

        messages.add_message(request, messages.ERROR, 'Error intentando editar el grupo')

    return 

@login_required(login_url='/accounts/login/')
def eliminar_grupo(request):

    if request.POST['eliminar'] == 'eliminar':
        
        try:
            usuario = User.get_username(request.user)
            usuario = User.objects.get(username=usuario)
            dept_obj = Grupos.objects.filter(id=request.POST['id'], propietario=usuario)
            dept_obj.delete()
            messages.add_message(request, messages.SUCCESS, 'Grupo eliminado correctamente')


        except:

            messages.add_message(request, messages.ERROR, 'No se ha podido eliminar el grupo')

    else:

        messages.add_message(request, messages.ERROR, 'Introduce correctamente "delete"')
    return
