from django.db import models

# Create your models here.

class Empleado(models.Model):

    ADMIN = 'admin'
    OPERADOR = 'operador'

    ROLES = [
        (ADMIN, 'Administrador'),
        (OPERADOR, 'Operador'),
    ]

    id_empleado = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=25)
    apellido = models.CharField(max_length=25)
    dui = models.CharField(max_length=10, unique=True)
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    contrasenia = models.CharField(max_length=128)
    rol = models.CharField(max_length=15, choices=ROLES)

    def __str__(self):
        return f'{self.nombre} {self.apellido} ({self.rol})'
    
class Buque(models.Model):
    numero_buque = models.AutoField(primary_key=True)
    altura = models.DecimalField(max_digits=10, decimal_places=2)
    ancho = models.DecimalField(max_digits=10, decimal_places=2)
    largo = models.DecimalField(max_digits=10, decimal_places=2)
    cap_max_carga = models.DecimalField(max_digits=12, decimal_places=2)
    cant_trabajadores = models.IntegerField()

    def __str__(self):
        return f'Buque #{self.numero_buque}'

class Inventario(models.Model):
    buque = models.OneToOneField(Buque, on_delete=models.CASCADE, primary_key=True)
    operador = models.ForeignKey(Empleado, on_delete=models.SET_NULL, null=True, limit_choices_to={'rol': 'operador'})
    estado = models.CharField(max_length=25)

    def __str__(self):
        return f"Inventario del buque {self.buque.numero_buque}"

class Articulo(models.Model):
    CATEGORIA_CHOICES = [
        ('PRO', 'Provisiones'),
        ('REP', 'Repuestos'),
        ('LIM', 'Limpieza y Aseo'),
        ('SEG', 'Seguridad'),
        ('SUM', 'Suministros Generales'),
    ]

    id_articulo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    categoria = models.CharField(max_length=3, choices=CATEGORIA_CHOICES)
    cantidad = models.IntegerField()
    fecha_caducidad = models.DateField(null=True, blank=True)
    imagen = models.ImageField(upload_to='articulos/', null=True, blank=True)
    inventario = models.ForeignKey('Inventario', on_delete=models.CASCADE, related_name='articulos')

    def __str__(self):
        return f"{self.nombre} ({self.get_categoria_display()})"


class Servicio(models.Model):
    id_servicio = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_de_realizacion = models.DateField()
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='servicios/', blank=True, null=True)
    # Relaciones
    buque = models.ForeignKey('Buque', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.nombre
    


