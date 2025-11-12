from django.urls import path
from . import views

app_name = 'clientes'

urlpatterns = [
    path('', views.home, name='home'),
    path('registro/', views.registro, name='registro'),
    path('registrar-factura/', views.registrar_factura, name='registrar_factura'),
    path('mis-puntos/', views.ver_puntos, name='ver_puntos'),
    path('ranking/', views.ranking_mensual, name='ranking'),
    path('panel/', views.panel_admin, name='panel_admin'),
]
