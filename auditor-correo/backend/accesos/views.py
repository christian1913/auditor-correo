
from .connection_manager import ConnectionManager
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from django.shortcuts import get_object_or_404
from backend.accesos.models import Accesos
from backend.smtp.models import Enviados

connection_manager = ConnectionManager()

@login_required(login_url='/accounts/login/')
def index(request, id=None):
    data_list = []

    if id:
        enviado = get_object_or_404(Enviados, id=id)
        acceso = get_object_or_404(Accesos, enviado=enviado)
        puerto = acceso.puerto
        if puerto not in connection_manager.connections:
            connection_manager.start_connection(puerto)

        connection_manager.send_command(puerto, 'ls -la') # comando ls -la
        output = connection_manager.receive_output(puerto)
        lines = output.split("\n")[1:] # Elimina la primera línea que es total 
        for line in lines:
            if line: # Ignora las líneas vacías
                parts = line.split()
                perm = parts[0]
                name = parts[-1]
                if perm[0] == 'd':
                    data_list.append([name, 'dir'])
                else:
                    data_list.append([name, 'file'])

        # Obtener la ruta del directorio actual
        connection_manager.send_command(puerto, 'pwd')
        pwd_output = connection_manager.receive_output(puerto)
        current_path = pwd_output.strip() # Remover los espacios en blanco en los extremos

        if request.method == 'POST':
            if request.POST['instruccion'] == 'acceso-atras':
                connection_manager.send_command(puerto, 'cd ..')
            elif request.POST['instruccion'] == 'acceso-directorio':
                directory = request.POST.get('directorio')
                connection_manager.send_command(puerto, f'cd {directory}')
            elif request.POST['instruccion'] == 'acceso-descarga':
                file = request.POST.get('file')
                connection_manager.send_command(puerto, f'download {file}')
            else:
                print('ninguna selección es correcta')
                messages.add_message(request, messages.ERROR, 'Error en la petición')

    print(data_list)
    return render(request, 'backend/acceso/index.html', {'directorios': data_list, 'enviado': id, 'ruta': current_path})









