from django.shortcuts import render, redirect
from .models import Articulo, Empleado, Inventario

# Create your views here.

def login_view(request):
    # Lógica: validar usuario y contraseña, redirigir según rol
    if request.method == 'POST':
        dui = request.POST.get('dui')
        contrasenia = request.POST.get('contrasenia')

        try:
            empleado = Empleado.objects.get(dui=dui, contrasenia=contrasenia)
            request.session['empleado_id'] = empleado.id_empleado

            if empleado.rol == 'admin':
                return redirect('panel_admin')
            elif empleado.rol == 'operador':
                return redirect('inventario_operador')
        except Empleado.DoesNotExist:
            return render(request, 'login.html', {'error': 'Credenciales incorrectas'})

    return render(request, 'login.html')

def logout_view(request): 
    #lógica para cerrar sesión
    request.session.flush()
    return redirect('login')


def inventario_operador(request):
    # Lógica: mostrar tabla del inventario + botón “extraer artículo”
    empleado_id = request.session.get('empleado_id')  # Obtener el usuario logueado

    if not empleado_id:
        return redirect('login')  # No está logueado, lo mandamos a login

    operador = Empleado.objects.get(id_empleado=empleado_id)

    if operador.rol != 'operador':
        return redirect('login')  # No tiene el rol correcto, lo bloqueamos

    buque = operador.buque_asignado

    try:
        inventario = Inventario.objects.get(buque=buque)
        articulos = Articulo.objects.filter(inventario=inventario)
    except Inventario.DoesNotExist:
        articulos = []

    return render(request, 'inventario_operador.html', {'articulos': articulos})

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