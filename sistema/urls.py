from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('operador/', views.inventario_operador, name='inventario_operador'),
    path('admin/', views.panel_admin, name='panel_admin'),
    path('registro/', views.registro, name='registro'),
    path('eliminar/', views.confirmar_eliminacion, name='confirmar_eliminacion'),
]
