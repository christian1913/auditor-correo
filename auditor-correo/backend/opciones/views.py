from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Emisores
from django.contrib.auth.hashers import check_password
from django.contrib import messages 


##### OPCIONES #####


@login_required(login_url='/accounts/login/')
def index(request):

    if request.method == 'GET':
        
        datos = obtener_datos_opciones(request)

        data = {
            'datos' : datos,
        }

    elif request.method == 'POST':

        # Editar usuario

        if request.POST['instruccion'] == 'editar-usuario':

             editar_usuario(request)
             

        # Editar contraseña     

        elif request.POST['instruccion'] == 'editar-contraseña':

             editar_contraseña(request)

        # Añadir correo emisor

        elif request.POST['instruccion'] == 'añadir-emisor':

             añadir_correo_emisor(request)

        # Editar correo emisor

        elif request.POST['instruccion'] == 'editar-emisor':

             editar_correo_emisor(request)

        # Eliminar correo emisor

        elif request.POST['instruccion'] == 'eliminar-emisor':

             eliminar_correo_emisor(request)

        else:
            pass



        datos = obtener_datos_opciones(request)

        data = {
            'datos' : datos,
        }    

    else:

        print('NO ES UN GET NI UN POST')
        data = obtener_datos_opciones(request)

        data = {
        
            'datos' : datos,
        }

    return render(request, 'backend/opciones/index.html', data)


# Funcion obtener datos

@login_required(login_url='/accounts/login/')
def obtener_datos_opciones(request):
    usuario = User.get_username(request.user)
    datos = {
        'emisores': Emisores.objects.filter(propietario__username=usuario),
        'usuario': usuario
    }
    return datos


# Funciones post

@login_required(login_url='/accounts/login/')
def editar_usuario(request):

    try:

        usuario = User.get_username(request.user)
        usuario = User.objects.get(username=usuario)

        usuario.username = request.POST['usuario']
        usuario.save()

        messages.add_message(request, messages.SUCCESS, 'Usuario editado correctamente')
        request.user = usuario
    except: 

        messages.add_message(request, messages.ERROR, 'Error al editar el usuario')

    return 

@login_required(login_url='/accounts/login/')
def editar_contraseña(request):

    try:
        usuario = User.get_username(request.user)
        usuario = User.objects.get(username=usuario)
        if check_password(request.POST['pass-antigua'], usuario.password) and request.POST['password-nueva-1'] == request.POST['password-nueva-2'] :

            usuario.set_password(request.POST['password-nueva-1'])
            usuario.save()

            messages.add_message(request, messages.SUCCESS, 'Contraseña editada correctamente')
        else:
            messages.add_message(request, messages.ERROR, 'No se han introducido bien las credenciales')

    except: 

        messages.add_message(request, messages.ERROR, 'Error al editar la contraseña')

    return 

@login_required(login_url='/accounts/login/')
def añadir_correo_emisor(request):


    usuario = User.get_username(request.user)
    comprabacion = Emisores.objects.filter(correo=request.POST['correo'], propietario__username=usuario)
    if comprabacion: 
        messages.add_message(request, messages.ERROR, 'Error al crear el correo o el correo ya existe')
    else:
        usuario = User.objects.get(username=usuario)
        Emisores.objects.create(correo=request.POST['correo'], contraseña=request.POST['contraseña'],smtp=request.POST['smtp'], puerto=request.POST['puerto'],propietario=usuario)

        messages.add_message(request, messages.SUCCESS, 'Correo creado correctamente')
    return 


@login_required(login_url='/accounts/login/')
def editar_correo_emisor(request):

    try:

        usuario = User.get_username(request.user)
        usuario = User.objects.get(username=usuario)
        
        id = request.POST['id']
        correo = request.POST['correo']
        contraseña = request.POST['contraseña']
        smtp = request.POST['smtp']
        puerto = request.POST['puerto']

        Emisores.objects.filter(id=id).update(correo=correo, contraseña=contraseña, smtp=smtp, puerto=puerto, propietario=usuario)

        messages.add_message(request, messages.SUCCESS, 'Emisor editado correctamente')

    except: 
        messages.add_message(request, messages.ERROR, 'Error intentando editar el emisor')

    return 

@login_required(login_url='/accounts/login/')
def eliminar_correo_emisor(request):
    if request.POST['eliminar'] == 'eliminar':

        try:
            correoObj = Emisores.objects.filter(id=request.POST['id'])
        
            correoObj.delete()
            messages.add_message(request, messages.SUCCESS, 'Correo eliminado correctamente')

        except:

            messages.add_message(request, messages.ERROR, 'No se ha encontrado el correo')
    else:

        messages.add_message(request, messages.ERROR, 'No se introducido eliminar correctamente. No se eliminará el correo')

    return

