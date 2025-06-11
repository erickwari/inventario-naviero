from django.shortcuts import render
from .models import Articulo

# Create your views here.

def login_view(request):
    return render(request, 'login.html')
    # Lógica: validar usuario y contraseña, redirigir según rol

def inventario_operador(request):
    articulos = Articulo.objects.all()
    return render(request, 'inventario_operador.html', {'articulos': articulos})
    # Lógica: mostrar tabla del inventario + botón “extraer artículo”

def panel_admin(request):
    return render(request, 'panel_admin.html')
    # Lógica:
    # - Mostrar inventario del buque seleccionado
    # - Mostrar servicios si se pulsa “mostrar servicios”
    # - Filtros de búsqueda
    # - Botón “reabastecer”

def registro(request):
    return render(request, 'registro.html')
    # Lógica:
    # - Radio buttons: seleccionar artículo o servicio
    # - Mostrar campos según selección
    # - Validar campos (campos vacíos, fechas, cantidad)
    # - Mostrar alerta de éxito o error

def confirmar_eliminacion(request):
    return render(request, 'confirmar_eliminacion.html')
    # Lógica: alerta de confirmación antes de eliminar artículo