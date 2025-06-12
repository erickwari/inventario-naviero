from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('operador/', views.inventario_operador, name='inventario_operador'),
    path('panel-admin/', views.panel_admin, name='panel_admin'),
    path('reabastecer/<int:id_articulo>/', views.reabastecer_articulo, name='reabastecer_articulo'),
    path('registro/', views.registro, name='registro'),
    path('eliminar/', views.confirmar_eliminacion, name='confirmar_eliminacion'),
    path('extraer/', views.extraer_articulo, name='extraer_articulo'),
]
