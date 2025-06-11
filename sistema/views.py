from django.shortcuts import render
from .models import Articulo, Empleado, Inventario

# Create your views here.

def login_view(request):
    return render(request, 'login.html')
    # Lógica: validar usuario y contraseña, redirigir según rol

def inventario_operador(request):
    # Lógica: mostrar tabla del inventario + botón “extraer artículo”
    # Esto es solo temporal, para simular que el operador con ID 1 está logueado
    operador = Empleado.objects.get(id_empleado=2)

    # Buscamos su buque asignado
    buque = operador.buque_asignado

    # Obtenemos el inventario de ese buque
    try:
        inventario = Inventario.objects.get(buque=buque)
        articulos = Articulo.objects.filter(inventario=inventario)
    except Inventario.DoesNotExist:
        articulos = []

    return render(request, 'inventario_operador.html', {
        'articulos': articulos
    })

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