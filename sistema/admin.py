from django.contrib import admin

# Register your models here.

from .models import Empleado, Buque, Inventario, Articulo, Servicio

admin.site.register(Empleado)
admin.site.register(Buque)
admin.site.register(Inventario)
admin.site.register(Articulo)
admin.site.register(Servicio)