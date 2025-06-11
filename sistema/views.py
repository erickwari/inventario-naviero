from django.shortcuts import render

# Create your views here.

def inicio(request):
    return render(request, 'inicio.html')

def confirmar_eliminacion(request):
    return render(request, 'confirmar_eliminacion.html')
    # Lógica: alerta de confirmación antes de eliminar artículo