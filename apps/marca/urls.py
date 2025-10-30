from django.urls import path
from apps.modelo.views import listado_modelo
from . import views

urlpatterns = [
    path('', listado_modelo, name='listado_marca'),
    path('agregar/', views.agregar_marca, name='marca_agregar'),
]