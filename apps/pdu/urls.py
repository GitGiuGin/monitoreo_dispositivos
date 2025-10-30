from django.urls import path
from . import views

urlpatterns = [
    path('ping/<path:ip>/', views.ping_pdu, name='ping_pdu'),
    path('', views.listado_pdu, name='pdu'),
    path('new/', views.agregar_pdu, name='pdu_agregar'),
    path('delete/<int:ubicacion_id>/', views.eliminar_pdu, name='eliminar_pdu'),
    path('edit/<int:pdu_id>/', views.editar_pdu, name='editar_pdu'),
]