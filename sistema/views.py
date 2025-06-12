from django.shortcuts import render, redirect, get_object_or_404
from .models import Articulo, Empleado, Inventario, Buque, Servicio
from datetime import datetime

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

from django.contrib import messages
from django.shortcuts import redirect

def extraer_articulo(request):
    #esta vista es para cuando el operador quiera extraer un artículo
    if request.method == 'POST':
        empleado_id = request.session.get('empleado_id')
        if not empleado_id:
            return redirect('login')

        id_articulo = request.POST.get('id_articulo')
        cantidad = request.POST.get('cantidad')

        try:
            cantidad= int(cantidad)
            if cantidad <= 0:
                raise ValueError
            articulo = Articulo.objects.get(id_articulo=id_articulo)

            if articulo.cantidad >= cantidad:
                articulo.cantidad -= cantidad
                articulo.save()
                messages.success(request, f"Se extrajeron {cantidad} unidades de {articulo.nombre}.")
            else:
                messages.error(request, "No hay suficientes unidades disponibles.")
        except (Articulo.DoesNotExist, ValueError):
            messages.error(request, "Ocurrió un error al procesar la solicitud.")
        except (ValueError, TypeError):
            messages.error(request, "Cantidad inválida. Debe ser un número entero positivo.")
            return redirect('inventario_operador')


        return redirect('inventario_operador')

def panel_admin(request):
    # Lógica:
    # - Mostrar inventario del buque seleccionado
    # - Mostrar servicios si se pulsa “mostrar servicios”
    # - Filtros de búsqueda
    # - Botón “reabastecer”

    empleado_id = request.session.get('empleado_id')
    if not empleado_id:
        return redirect('login')

    empleado = Empleado.objects.get(id_empleado=empleado_id)
    if empleado.rol != 'admin':
        return redirect('login')

    # Obtener el número de buque seleccionado desde GET (por ejemplo: ?buque=2)
    numero_buque = request.GET.get('buque')
    mostrar = request.GET.get('mostrar', 'inventario')
    nombre_filtro = ''
    categoria_filtro = ''
    articulos_sin_stock = ''

    buque = None
    inventario = None
    articulos = []
    servicios = []

    if numero_buque:
        try:
            buque = Buque.objects.get(numero_buque=numero_buque)

            if mostrar == 'inventario':
                inventario = Inventario.objects.get(buque=buque)
                articulos = Articulo.objects.filter(inventario=inventario)
                nombre_filtro = request.GET.get('nombre', '')
                categoria_filtro = request.GET.get('categoria', '')

                if inventario:
                    articulos = Articulo.objects.filter(inventario=inventario)

                    if nombre_filtro:
                        articulos = articulos.filter(nombre__icontains=nombre_filtro)

                    if categoria_filtro:
                        articulos = articulos.filter(categoria=categoria_filtro)

                    articulos_sin_stock = articulos.filter(cantidad=0)


            elif mostrar == 'servicios':
                servicios = Servicio.objects.filter(buque=buque)

        except (Buque.DoesNotExist, Inventario.DoesNotExist):
            articulos = []
            servicios = []

    buques = Buque.objects.all()

    return render(request, 'panel_admin.html', {
        'articulos': articulos,
        'servicios': servicios,
        'buques': buques,
        'numero_buque': numero_buque,
        'mostrar': mostrar,
        'cantidad_buques': buques.count(),
        'nombre_filtro': nombre_filtro,
        'categoria_filtro': categoria_filtro,
        'articulos_sin_stock': articulos_sin_stock,
    })

def reabastecer_articulo(request, id_articulo):
    articulo = get_object_or_404(Articulo, id_articulo=id_articulo)

    if request.method == 'POST':
        try:
            cantidad_agregada = int(request.POST.get('cantidad'))
            if cantidad_agregada <= 0:
                raise ValueError("Cantidad inválida")

            # Aumentar cantidad
            articulo.cantidad += cantidad_agregada

            # Actualizar fecha de caducidad si aplica

            fecha_input = request.POST.get('fecha_caducidad')
            if fecha_input:
                fecha_dt = datetime.strptime(fecha_input, '%Y-%m-%d').date()
                if fecha_dt < datetime.now().date():
                    raise ValueError("La fecha de caducidad no puede ser anterior a hoy.")
                articulo.fecha_caducidad = fecha_dt

            articulo.save()
            messages.success(request, f"Se reabastecieron {cantidad_agregada} unidades de '{articulo.nombre}'.")
            return redirect('panel_admin')

        except:
            messages.error(request, "Datos inválidos. Intente nuevamente.")

    return render(request, 'reabastecer_articulo.html', {
        'articulo': articulo,
        'hoy': datetime.now().date().isoformat()
    })

def registro(request):
    return render(request, 'registro.html')
    # Lógica:
    # - Radio buttons: seleccionar artículo o servicio
    # - Mostrar campos según selección
    # - Validar campos (campos vacíos, fechas, cantidad)
    # - Mostrar alerta de éxito o error

def eliminar_articulo(request, id_articulo):
    articulo = get_object_or_404(Articulo, id_articulo=id_articulo)

    if request.method == 'POST':
        articulo.delete()
        messages.success(request, f"Artículo '{articulo.nombre}' eliminado correctamente.")
        return redirect('panel_admin')

    return render(request, 'confirmar_eliminacion.html', {
        'articulo': articulo
    })