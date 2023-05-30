from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def enlace_descarga(request):

    ruta_documento = './prueba.pdf.zip'
    with open(ruta_documento, 'rb') as archivo:
        contenido = archivo.read()

    response = HttpResponse(contenido, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="documento.zip"'
    
    return response